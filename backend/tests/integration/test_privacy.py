"""Erasure clears linked storage; retention and consequential claims share safe locks."""

import asyncio
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select

from src.core.security import encrypt_pii, hash_phone
from src.db.audit import write_audit_log
from src.db.enums import MessageDirection
from src.db.models import (
    Application,
    AuditLog,
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    HumanRequest,
    Institution,
    IntegrationEvent,
    Lead,
    LeadFact,
    Message,
    NotificationReceipt,
    OutboundMessage,
    PaymentEvent,
    PaymentOrder,
    StaffUser,
    TelegramBot,
    TelegramIdentity,
    WebhookDelivery,
    WebhookEndpoint,
)
from src.engine.contracts import Reply
from src.integrations import delivery
from src.payments import service
from src.payments.provider import RazorpayClient
from src.staff import privacy
from src.telegram.outbound import enqueue_outbound
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_payment_jobs import seed as payment_seed

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


@pytest.fixture(autouse=True)
def privacy_dependencies(workspace, monkeypatch):
    workspace["settings"].phone_hash_key = "synthetic-privacy-key"
    for module in (privacy, delivery, service):
        monkeypatch.setattr(module, "get_sessionmaker", lambda: workspace["sessions"])
    monkeypatch.setattr(service, "get_settings", lambda: workspace["settings"])


async def full_subject(workspace):
    lead_id, application_id = await payment_seed(workspace)
    tenant = workspace["tenants"][0]
    async with workspace["sessions"]() as db:
        lead = await db.get(Lead, lead_id)
        synthetic_phone = f"+999{lead_id.int % 10**9:09d}"
        lead.name_enc, lead.phone_enc = (
            encrypt_pii("Synthetic privacy subject"),
            encrypt_pii(synthetic_phone),
        )
        lead.phone_hash = hash_phone(synthetic_phone)
        bot = TelegramBot(
            tenant_id=tenant,
            telegram_bot_id=uuid.uuid4().int % 1_000_000_000,
            token_enc=encrypt_pii("synthetic-token"),
        )
        db.add(bot)
        await db.flush()
        identity = TelegramIdentity(
            tenant_id=tenant,
            bot_id=bot.id,
            lead_id=lead_id,
            user_hash=uuid.uuid4().hex * 2,
            chat_hash=uuid.uuid4().hex * 2,
            user_id_enc=encrypt_pii("42"),
            chat_id_enc=encrypt_pii("42"),
        )
        db.add(identity)
        await db.flush()
        event = ConversationEvent(
            tenant_id=tenant,
            bot_id=bot.id,
            identity_id=identity.id,
            lead_id=lead_id,
            update_id=1,
            kind="text",
            payload_enc=encrypt_pii("{}"),
            status="done",
        )
        db.add(event)
        await db.flush()
        db.add_all(
            [
                ConversationReply(
                    tenant_id=tenant, event_id=event.id, payload_enc=encrypt_pii("{}")
                ),
                ConversationMemory(
                    tenant_id=tenant,
                    lead_id=lead_id,
                    payload_enc=encrypt_pii('{"facts":{"age":20}}'),
                ),
                HumanRequest(tenant_id=tenant, lead_id=lead_id),
                LeadFact(tenant_id=tenant, lead_id=lead_id, key="age", value=20),
                Message(
                    tenant_id=tenant,
                    lead_id=lead_id,
                    direction=MessageDirection.INBOUND,
                    content=encrypt_pii("Synthetic message"),
                ),
            ]
        )
        order = PaymentOrder(
            tenant_id=tenant,
            lead_id=lead_id,
            application_id=application_id,
            course_id=lead.current_course_id,
            amount=10000,
            creation_state="queued",
        )
        db.add(order)
        await db.flush()
        db.add(
            PaymentEvent(
                tenant_id=tenant,
                payment_order_id=order.id,
                body_digest=uuid.uuid4().hex * 2,
                kind="synthetic",
            )
        )
        outbound_id = await enqueue_outbound(
            db,
            tenant_id=tenant,
            lead_id=lead_id,
            kind="staff_reply",
            dedup_key=uuid.uuid4().hex,
            reply=Reply(text="Synthetic reply"),
        )
        endpoint = await db.scalar(
            select(WebhookEndpoint).where(WebhookEndpoint.tenant_id == tenant)
        )
        if endpoint is None:
            db.add(
                WebhookEndpoint(
                    tenant_id=tenant,
                    url_enc=encrypt_pii("https://example.test/events"),
                    secret_enc=encrypt_pii("synthetic-webhook-secret"),
                    display_host="example.test",
                    enabled=True,
                )
            )
        await db.flush()
        audit = await write_audit_log(
            db,
            tenant_id=tenant,
            lead_id=lead_id,
            actor="synthetic-test",
            action="payment.confirmed",
            details={"application_id": str(application_id)},
        )
        user_id = await db.scalar(
            select(StaffUser.id).where(StaffUser.tenant_id == tenant).limit(1)
        )
        db.add(NotificationReceipt(tenant_id=tenant, user_id=user_id, event_id=audit.id))
        await db.commit()
        return {
            "lead": lead_id,
            "application": application_id,
            "event": event.id,
            "identity": identity.id,
            "order": order.id,
            "outbound": outbound_id,
            "audit": audit.id,
        }


def test_erasure_roles_confirmation_and_all_linked_storage(workspace):
    data = asyncio.run(full_subject(workspace))
    client = workspace["client"]
    path = f"/api/staff/leads/{data['lead']}"
    body = {"confirm_id": str(data["lead"])}
    signin(client, email="agent@example.test")
    assert client.request("DELETE", path, json=body, headers=HEADERS).status_code == 403
    signin(client, "second")
    assert client.request("DELETE", path, json=body, headers=HEADERS).status_code == 404
    signin(client)
    assert client.request("DELETE", path, json=body).status_code == 403
    assert (
        client.request(
            "DELETE", path, json={"confirm_id": str(uuid.uuid4())}, headers=HEADERS
        ).status_code
        == 422
    )
    result = client.request("DELETE", path, json=body, headers=HEADERS)
    assert result.status_code == 200, result.text
    receipt = result.json()["receipt_id"]

    async def inspect():
        async with workspace["sessions"]() as db:
            assert await db.get(Lead, data["lead"]) is None
            for model in (
                LeadFact,
                Message,
                ConversationMemory,
                HumanRequest,
                Application,
                OutboundMessage,
                PaymentOrder,
                TelegramIdentity,
                ConversationEvent,
                IntegrationEvent,
            ):
                assert not await db.scalar(
                    select(func.count())
                    .select_from(model)
                    .where(
                        model.tenant_id == workspace["tenants"][0], model.lead_id == data["lead"]
                    )
                )
            for model, predicate in [
                (ConversationReply, ConversationReply.event_id == data["event"]),
                (PaymentEvent, PaymentEvent.payment_order_id == data["order"]),
                (WebhookDelivery, WebhookDelivery.event_id == data["audit"]),
                (NotificationReceipt, NotificationReceipt.event_id == data["audit"]),
            ]:
                assert not await db.scalar(select(func.count()).select_from(model).where(predicate))
            audit = await db.get(AuditLog, data["audit"])
            assert audit.lead_id is None and audit.details is None
            saved = await db.get(AuditLog, uuid.UUID(receipt))
            assert (
                saved.action == "privacy.deleted"
                and saved.lead_id is None
                and saved.details == {"reason": "staff_request"}
            )

    asyncio.run(inspect())


def test_active_operations_prevent_erasure(workspace):
    data = asyncio.run(full_subject(workspace))
    signin(workspace["client"])

    async def state(value):
        async with workspace["sessions"]() as db:
            order = await db.get(PaymentOrder, data["order"])
            order.creation_state = value
            await db.commit()

    asyncio.run(state("creating"))
    result = workspace["client"].request(
        "DELETE",
        f"/api/staff/leads/{data['lead']}",
        json={"confirm_id": str(data["lead"])},
        headers=HEADERS,
    )
    assert result.status_code == 409
    asyncio.run(state("queued"))


def test_retention_uses_communication_age_and_tenant_policy(workspace):
    now = datetime.now(UTC)
    signin(workspace["client"])
    settings = workspace["client"].get("/api/staff/settings").json()
    settings["retention_days"] = 10
    assert (
        workspace["client"].put("/api/staff/settings", json=settings, headers=HEADERS).status_code
        == 200
    )

    async def exercise():
        async with workspace["sessions"]() as db:
            first = await db.get(Institution, workspace["tenants"][0])
            rows = [
                Lead(tenant_id=first.id, created_at=now - timedelta(days=30)),
                Lead(
                    tenant_id=first.id,
                    created_at=now - timedelta(days=30),
                    last_inbound_at=now - timedelta(days=1),
                ),
                Lead(
                    tenant_id=first.id,
                    created_at=now - timedelta(days=30),
                    last_outbound_at=now - timedelta(days=1),
                ),
                Lead(tenant_id=first.id, created_at=now - timedelta(days=10)),
                Lead(tenant_id=workspace["tenants"][1], created_at=now - timedelta(days=30)),
            ]
            db.add_all(rows)
            await db.commit()
            ids = [row.id for row in rows]
        assert await privacy.purge_retained(now=now) == 1
        assert await privacy.purge_retained(now=now) == 0
        async with workspace["sessions"]() as db:
            assert await db.get(Lead, ids[0]) is not None
            for lead_id in ids[1:]:
                assert await db.get(Lead, lead_id) is not None

    asyncio.run(exercise())


def test_automatic_retention_expires_dialogue_and_preserves_financial_records(workspace):
    data = asyncio.run(full_subject(workspace))
    now = datetime.now(UTC)

    async def exercise():
        async with workspace["sessions"]() as db:
            lead = await db.get(Lead, data["lead"])
            lead.created_at = now - timedelta(days=30)
            tenant = await db.get(Institution, lead.tenant_id)
            tenant.retention_days = 10
            await db.commit()
        assert await privacy.purge_retained(now=now) >= 1
        async with workspace["sessions"]() as db:
            assert (await db.get(Lead, data["lead"])).conversation_purged_at == now
            assert await db.get(Application, data["application"]) is not None
            assert await db.get(PaymentOrder, data["order"]) is not None
            assert (await db.get(PaymentOrder, data["order"])).creation_state == "failed"
            assert await db.get(IntegrationEvent, data["audit"]) is not None
            assert await db.get(TelegramIdentity, data["identity"]) is not None
            for model in (
                ConversationEvent,
                ConversationMemory,
                LeadFact,
                Message,
                OutboundMessage,
            ):
                assert not await db.scalar(
                    select(func.count()).select_from(model).where(model.lead_id == data["lead"])
                )
        assert await privacy.purge_retained(now=now) == 0

    asyncio.run(exercise())


def test_payment_and_webhook_claims_wait_for_erasure_lock(workspace, monkeypatch):
    data = asyncio.run(full_subject(workspace))
    calls = []

    async def provider(*args):
        calls.append(args)
        raise AssertionError("No request expected")

    monkeypatch.setattr(RazorpayClient, "create_link", provider)
    monkeypatch.setattr(delivery, "post_event", provider)

    async def exercise():
        async with workspace["sessions"]() as db:
            lead = await db.scalar(select(Lead).where(Lead.id == data["lead"]).with_for_update())
            webhook = await db.scalar(
                select(WebhookDelivery.id).where(WebhookDelivery.event_id == data["audit"])
            )
            payment_task = asyncio.create_task(service.process_payment(data["order"]))
            webhook_task = asyncio.create_task(delivery.deliver(lead.tenant_id, webhook))
            await asyncio.sleep(0.05)
            assert not payment_task.done() and not webhook_task.done() and calls == []
            await privacy.erase(db, lead, actor="synthetic-test", reason="staff_request")
            await db.commit()
        assert await asyncio.wait_for(payment_task, 3) is None
        await asyncio.wait_for(webhook_task, 3)
        assert calls == []

    asyncio.run(exercise())
