"""Reference demo applications require test payment and never allocate university seats."""

import asyncio
import json
from typing import Any

import pytest
from sqlalchemy import func, select

from src.core import demo_admissions
from src.core.security import encrypt_pii
from src.db.enums import LeadStatus, PaymentStatus
from src.db.models import (
    Application,
    Batch,
    Course,
    Institution,
    Lead,
    OutboundMessage,
    PaymentOrder,
    TelegramBot,
)
from src.engine.applications import application_action
from src.engine.journey import select_course
from src.payments.service import PaymentRequestError, fee_details, request_payment
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


@pytest.fixture
def demo(workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    settings = workspace["settings"]
    monkeypatch.setattr(settings, "demo_admissions_enabled", True)
    monkeypatch.setattr(settings, "phone_hash_key", "synthetic-callback-key")
    monkeypatch.setattr(settings, "telegram_institution_code", "first")
    monkeypatch.setattr(demo_admissions, "get_settings", lambda: settings)
    monkeypatch.setattr("src.telegram.callbacks.get_settings", lambda: settings)
    return workspace


async def configure(db: Any, tenant: Any) -> None:
    institution = await db.get(Institution, tenant)
    institution.razorpay_credentials_enc = encrypt_pii(
        json.dumps(
            {
                "key_id": "rzp_test_synthetic",
                "key_secret": "synthetic-secret",
                "webhook_secret": "synthetic-webhook-secret",
            }
        )
    )


def test_every_reference_course_enters_reviewable_demo_without_fake_eligibility(
    demo: dict[str, Any],
) -> None:
    async def exercise() -> None:
        tenant = demo["tenants"][0]
        async with demo["sessions"]() as db:
            await configure(db, tenant)
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=770, token_enc=encrypt_pii("synthetic-token")
            )
            db.add(bot)
            for i in range(64):
                course = Course(
                    tenant_id=tenant,
                    name=f"Reference {i}",
                    is_reference=True,
                    demo_application_fee=300000,
                )
                lead = Lead(tenant_id=tenant)
                db.add_all([course, lead])
                await db.flush()
                memory: dict[str, Any] = {}
                reply = await select_course(db, lead, bot, memory, course.id)
                assert "demo" in reply.text.lower() and "full name" in reply.text.lower()
                assert "Compare programmes" not in [b.text for b in reply.buttons]
                assert lead.current_course_id == course.id and lead.current_batch_id is None
                assert memory["application_draft"]["is_demo"] is True
                assert memory.get("eligibility", {}).get("outcome") != "eligible"
                assert course.application_fee == 0 and course.is_reference
            assert await db.scalar(select(func.count()).select_from(Application)) == 0
            assert await db.scalar(select(func.count()).select_from(Batch)) == 0

    asyncio.run(exercise())


@pytest.mark.parametrize("guard", ["disabled", "prod", "live", "tenant", "key", "fee"])
def test_demo_guards_keep_reference_exploration(
    demo: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    guard: str,
) -> None:
    settings = demo["settings"]
    if guard == "disabled":
        monkeypatch.setattr(settings, "demo_admissions_enabled", False)
    if guard == "prod":
        monkeypatch.setattr(settings, "app_env", "prod")
    if guard == "live":
        monkeypatch.setattr(settings, "payments_live_enabled", True)
    if guard == "tenant":
        monkeypatch.setattr(settings, "telegram_institution_code", "second")

    async def exercise() -> None:
        tenant = demo["tenants"][0]
        async with demo["sessions"]() as db:
            await configure(db, tenant)
            if guard == "key":
                institution = await db.get(Institution, tenant)
                institution.razorpay_credentials_enc = encrypt_pii(
                    json.dumps(
                        {
                            "key_id": "rzp_live_synthetic",
                            "key_secret": "synthetic-secret",
                            "webhook_secret": "synthetic-webhook-secret",
                        }
                    )
                )
            course = Course(
                tenant_id=tenant,
                name="Reference guarded",
                is_reference=True,
                demo_application_fee=None if guard == "fee" else 300000,
            )
            lead = Lead(tenant_id=tenant)
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=771, token_enc=encrypt_pii("synthetic-token")
            )
            db.add_all([course, lead, bot])
            await db.flush()
            memory: dict[str, Any] = {}
            reply = await select_course(db, lead, bot, memory, course.id)
            assert "Compare programmes" in [b.text for b in reply.buttons]
            assert "application_draft" not in memory

    asyncio.run(exercise())


def test_demo_submit_fee_replay_and_paid_only_staff_approval(
    demo: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def exercise() -> tuple[Any, Any]:
        tenant = demo["tenants"][0]
        async with demo["sessions"]() as db:
            await configure(db, tenant)
            course = Course(
                tenant_id=tenant, name="Demo choice", is_reference=True, demo_application_fee=300000
            )
            lead = Lead(tenant_id=tenant)
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=772, token_enc=encrypt_pii("synthetic-token")
            )
            db.add_all([course, lead, bot])
            await db.flush()
            memory: dict[str, Any] = {
                "application_details": {
                    "full_name": "Synthetic Student",
                    "dob": "2000-01-01",
                    "parent_name": "Synthetic Parent",
                    "address": "Synthetic address",
                    "previous_school": "Synthetic School",
                }
            }
            await select_course(db, lead, bot, memory, course.id)
            draft = memory["application_draft"]
            reply = await application_action(db, lead, bot, memory, f"submit-{draft['nonce']}")
            assert "3000.00" in reply.text and "test" in reply.text.lower()
            application = await db.scalar(select(Application).where(Application.lead_id == lead.id))
            assert application.is_demo and application.batch_id is None
            assert lead.status == LeadStatus.PAYMENT_PENDING
            await application_action(db, lead, bot, memory, f"submit-{draft['nonce']}")
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(Application)
                    .where(Application.lead_id == lead.id)
                )
                == 1
            )
            with pytest.raises(PaymentRequestError):
                await fee_details(db, lead, application.id, "WAIVE")
            order = await request_payment(db, lead, application.id)
            await db.flush()
            assert order.is_demo and order.amount == 300000
            assert (await request_payment(db, lead, application.id)).id == order.id
            await db.commit()
            return application.id, order.id

    application_id, order_id = asyncio.run(exercise())
    from src.payments import service
    from src.payments.provider import PaymentLink, RazorpayClient

    monkeypatch.setattr(service, "get_sessionmaker", lambda: demo["sessions"])
    monkeypatch.setattr(service, "get_settings", lambda: demo["settings"])

    async def create(self: Any, reference: str, amount: int, *, demo: bool = False) -> PaymentLink:
        assert demo and amount == 300000 and reference == order_id.hex
        return PaymentLink(
            id="plink_demo",
            reference_id=reference,
            amount=amount,
            currency="INR",
            status="created",
            short_url="https://rzp.io/synthetic",
        )

    monkeypatch.setattr(RazorpayClient, "create_link", create)
    assert asyncio.run(service.process_payment(order_id)) is not None
    client = demo["client"]
    signin(client)
    headers = {"X-AdmitFlow-Request": "1"}
    path = f"/api/staff/applications/{application_id}/approve"
    assert client.get(f"/api/staff/applications/{application_id}").json()["is_demo"] is True
    assert client.post(path, headers=headers).status_code == 409

    async def pay(status: PaymentStatus) -> None:
        async with demo["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            order.status = status
            order.razorpay_payment_id = "pay_synthetic" if status == PaymentStatus.PAID else None
            await db.commit()

    asyncio.run(pay(PaymentStatus.WAIVED))
    assert client.post(path, headers=headers).status_code == 409
    # Read-only provider confirmation uses the same settlement and replay guard as webhooks.
    from src.payments import demo as demo_payments
    from src.payments.confirmation import PaidEvent

    monkeypatch.setattr(demo_payments, "get_sessionmaker", lambda: demo["sessions"])
    monkeypatch.setattr(demo_payments, "get_settings", lambda: demo["settings"])
    event = PaidEvent.model_validate(
        {
            "event": "payment_link.paid",
            "payload": {
                "payment_link": {
                    "entity": {
                        "id": "plink_demo",
                        "reference_id": order_id.hex,
                        "amount": 300000,
                        "amount_paid": 300000,
                        "currency": "INR",
                        "status": "paid",
                    }
                },
                "payment": {
                    "entity": {
                        "id": "pay_demo",
                        "amount": 300000,
                        "currency": "INR",
                        "status": "captured",
                    }
                },
            },
        }
    )

    async def confirm(self: Any, link_id: str, reference: str, amount: int) -> PaidEvent:
        assert link_id == "plink_demo" and reference == order_id.hex and amount == 300000
        return event

    monkeypatch.setattr(RazorpayClient, "confirm_test_link", confirm)

    async def settle() -> None:
        await pay(PaymentStatus.CREATED)
        async with demo["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            order.razorpay_payment_link_id = "plink_demo"
            order.creation_state = "created"
            await db.commit()
        monkeypatch.setattr(demo["settings"], "demo_admissions_enabled", False)
        response = client.post(f"/api/staff/payments/{order_id}/reconcile", headers=headers)
        assert response.status_code == 409
        monkeypatch.setattr(demo["settings"], "demo_admissions_enabled", True)
        assert await demo_payments.check_demo_payments() == 1
        assert await demo_payments.check_demo_payment(order_id) is False
        async with demo["sessions"]() as db:
            order = await db.get(PaymentOrder, order_id)
            assert order.status == PaymentStatus.PAID
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.dedup_key == f"payment-paid:{order_id}")
                )
                == 1
            )
            assert await db.scalar(select(func.count()).select_from(Batch)) == 0

    asyncio.run(settle())
    assert client.post(path, headers=headers).status_code == 200
    assert client.post(path, headers=headers).status_code == 200
    signin(client, "second")
    assert client.post(path, headers=headers).status_code == 404
