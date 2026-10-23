"""Committed event delivery, signed destination configuration and live staff isolation."""

import asyncio
import json
import uuid
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import delete, select
from starlette.websockets import WebSocketDisconnect

from src.core.security import decrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import LeadStatus
from src.db.models import (
    IntegrationEvent,
    Lead,
    StaffSession,
    WebhookDelivery,
    WebhookEndpoint,
)
from src.integrations import delivery
from src.staff import integrations, notifications
from src.staff.auth import COOKIE, token_hash
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}
ORIGIN = {"Origin": "http://localhost:3000"}


@pytest.fixture(autouse=True)
def event_dependencies(workspace, monkeypatch):
    async def public(_host):
        return "8.8.8.8"

    monkeypatch.setattr(integrations, "resolve_public", public)
    monkeypatch.setattr(delivery, "get_sessionmaker", lambda: workspace["sessions"])
    monkeypatch.setattr(notifications, "get_settings", lambda: workspace["settings"])


def configure(workspace):
    client = workspace["client"]
    signin(client)
    result = client.put(
        "/api/staff/integrations",
        json={"url": "https://hooks.example.test/events?key=synthetic-secret", "enabled": True},
        headers=HEADERS,
    )
    assert result.status_code == 200, result.text
    return result.json()


async def event_for(workspace, *, action="payment.confirmed", tenant=None):
    async with workspace["sessions"]() as db:
        lead = Lead(tenant_id=tenant or workspace["tenants"][0])
        db.add(lead)
        await db.flush()
        audit = await write_audit_log(
            db,
            tenant_id=lead.tenant_id,
            lead_id=lead.id,
            actor="synthetic-worker",
            action=action,
            details={"untrusted": "This value must not reach integrations"},
        )
        await db.commit()
        row = await db.scalar(
            select(WebhookDelivery).where(
                WebhookDelivery.event_id == audit.id, WebhookDelivery.tenant_id == lead.tenant_id
            )
        )
        return lead.id, audit.id, row.id if row else None


def test_configuration_roles_encryption_and_tenant_ownership(workspace):
    client = workspace["client"]
    signin(client, email="agent@example.test")
    assert client.get("/api/staff/integrations").status_code == 403
    assert (
        client.put("/api/staff/integrations", json={"enabled": True}, headers=HEADERS).status_code
        == 403
    )
    saved = configure(workspace)
    assert len(saved["signing_secret"]) >= 32
    result = client.get("/api/staff/integrations")
    assert result.headers["cache-control"] == "no-store"
    assert result.json()["host"] == "hooks.example.test"
    assert "synthetic-secret" not in result.text and saved["signing_secret"] not in result.text
    for url in ("http://example.test/", "https://127.0.0.1/", "https://a:b@example.test/"):
        assert (
            client.put(
                "/api/staff/integrations", json={"url": url, "enabled": True}, headers=HEADERS
            ).status_code
            == 422
        )
    assert client.put("/api/staff/integrations", json={"enabled": True}).status_code == 403
    signin(client, "second")
    assert client.get("/api/staff/integrations").json()["configured"] is False

    async def inspect():
        async with workspace["sessions"]() as db:
            row = await db.scalar(
                select(WebhookEndpoint).where(WebhookEndpoint.tenant_id == workspace["tenants"][0])
            )
            assert "synthetic-secret" not in row.url_enc
            assert decrypt_pii(row.secret_enc) == saved["signing_secret"]

    asyncio.run(inspect())


def test_source_transaction_rolls_back_event_and_outbox(workspace):
    configure(workspace)

    async def exercise():
        async with workspace["sessions"]() as db:
            lead = Lead(tenant_id=workspace["tenants"][0])
            db.add(lead)
            await db.commit()
            lead_id = lead.id
            lead.status = LeadStatus.ADMISSION_READY
            await db.flush()
            event = await db.scalar(
                select(IntegrationEvent).where(IntegrationEvent.lead_id == lead_id)
            )
            assert event.notification == "qualified"
            event_id = event.id
            assert await db.scalar(
                select(WebhookDelivery.id).where(WebhookDelivery.event_id == event_id)
            )
            await db.rollback()
        async with workspace["sessions"]() as db:
            assert await db.get(IntegrationEvent, event_id) is None
            assert (
                await db.scalar(
                    select(WebhookDelivery.id).where(WebhookDelivery.event_id == event_id)
                )
                is None
            )
            assert (await db.get(Lead, lead_id)).status == LeadStatus.NEW

    asyncio.run(exercise())


def test_delivery_claim_retry_and_minimal_payload(workspace, monkeypatch):
    configure(workspace)
    calls = []

    async def post(url, secret, delivery_id, timestamp, body):
        calls.append((delivery_id, body))
        assert "synthetic-secret" in url and len(secret) >= 32
        envelope = json.loads(body)
        assert set(envelope) == {
            "id",
            "type",
            "institution_id",
            "inquiry_id",
            "state",
            "created_at",
        }
        assert "untrusted" not in body.decode()
        await asyncio.sleep(0.02)
        return 503 if len(calls) == 1 else 204

    monkeypatch.setattr(delivery, "post_event", post)

    async def exercise():
        lead_id, event_id, delivery_id = await event_for(workspace)
        tenant = workspace["tenants"][0]
        await delivery.deliver(workspace["tenants"][1], delivery_id)
        assert calls == []
        await asyncio.gather(
            delivery.deliver(tenant, delivery_id), delivery.deliver(tenant, delivery_id)
        )
        assert len(calls) == 1
        async with workspace["sessions"]() as db:
            row = await db.get(WebhookDelivery, delivery_id)
            assert row.status == "queued" and row.attempts == 1 and row.error_code == "http_503"
            row.next_attempt_at = datetime.now(UTC) - timedelta(seconds=1)
            await db.commit()
        await delivery.deliver(tenant, delivery_id)
        await delivery.deliver(tenant, delivery_id)
        assert len(calls) == 2 and calls[0] == calls[1]
        async with workspace["sessions"]() as db:
            row = await db.get(WebhookDelivery, delivery_id)
            assert row.status == "sent" and row.attempts == 2 and row.next_attempt_at is None

    asyncio.run(exercise())


def test_expired_lease_recovery_cap_and_configuration_cancellation(workspace, monkeypatch):
    configure(workspace)
    from src.tasks.integrations import send_webhook

    queued = []

    async def enqueue(*args):
        queued.append(args)

    monkeypatch.setattr(send_webhook, "kiq", enqueue)
    network_calls = []

    async def forbidden(*args):
        network_calls.append(args)
        raise AssertionError("No network delivery expected")

    monkeypatch.setattr(delivery, "post_event", forbidden)

    async def exercise():
        _, _, delivery_id = await event_for(workspace)
        async with workspace["sessions"]() as db:
            row = await db.get(WebhookDelivery, delivery_id)
            row.status, row.attempts, row.lease_id = "sending", 6, uuid.uuid4()
            row.next_attempt_at = datetime.now(UTC) - timedelta(seconds=1)
            await db.commit()
        await delivery.dispatch_pending()
        assert (str(workspace["tenants"][0]), str(delivery_id)) in queued
        await delivery.deliver(workspace["tenants"][0], delivery_id)
        assert network_calls == []
        async with workspace["sessions"]() as db:
            assert (await db.get(WebhookDelivery, delivery_id)).status == "dead"
        return (await event_for(workspace))[2]

    pending = asyncio.run(exercise())
    signin(workspace["client"])
    result = workspace["client"].put(
        "/api/staff/integrations", json={"enabled": False, "rotate_secret": True}, headers=HEADERS
    )
    assert result.status_code == 200 and result.json()["signing_secret"]

    async def inspect():
        async with workspace["sessions"]() as db:
            assert (await db.get(WebhookDelivery, pending)).status == "cancelled"

    asyncio.run(inspect())


def test_live_notifications_origins_tenants_receipts_and_revocation(workspace):
    client = workspace["client"]
    client.cookies.clear()
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/api/staff/notifications/ws", headers=ORIGIN):
            pass
    signin(client)
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            "/api/staff/notifications/ws", headers={"Origin": "https://attacker.test"}
        ):
            pass
    lead_id, event_id, _ = asyncio.run(event_for(workspace))
    _, foreign_id, _ = asyncio.run(event_for(workspace, tenant=workspace["tenants"][1]))
    with client.websocket_connect("/api/staff/notifications/ws", headers=ORIGIN) as socket:
        snapshot = socket.receive_json()
        ids = {item["id"] for item in snapshot["items"]}
        assert str(event_id) in ids and str(foreign_id) not in ids
        socket.send_json({"action": "acknowledge", "ids": [str(event_id), str(foreign_id)]})
        refreshed = socket.receive_json()
        assert (
            next(item for item in refreshed["items"] if item["id"] == str(event_id))["unread"]
            is False
        )
        assert refreshed["unread_count"] == snapshot["unread_count"] - 1
        _, live_id, _ = asyncio.run(event_for(workspace, action="staff.draft_generated"))
        update_snapshot = socket.receive_json()
        assert any(
            item["id"] == str(live_id) and item["kind"] == "draft"
            for item in update_snapshot["items"]
        )
        saved_token = client.cookies.get(COOKIE)

        async def revoke():
            async with workspace["sessions"]() as db:
                await db.execute(
                    delete(StaffSession).where(StaffSession.token_hash == token_hash(saved_token))
                )
                await db.commit()

        asyncio.run(revoke())
        with pytest.raises(WebSocketDisconnect):
            socket.receive_json()
    signin(client, email="agent@example.test")
    snapshot = client.get("/api/staff/notifications").json()
    assert next(item for item in snapshot["items"] if item["id"] == str(event_id))["unread"] is True
    signin(client, "second")
    assert client.get("/api/staff/notifications").json()["unread_count"] == 1
    assert (
        client.post(
            "/api/staff/notifications/read", json={"ids": [str(event_id)]}, headers=HEADERS
        ).status_code
        == 200
    )
    assert client.get("/api/staff/notifications").json()["unread_count"] == 1


def test_more_than_one_page_of_unread_events_remains_accessible(workspace):
    client = workspace["client"]
    signin(client, "second")
    baseline = client.get("/api/staff/notifications").json()["unread_count"]

    async def seed():
        for _ in range(55):
            await event_for(workspace, tenant=workspace["tenants"][1])

    asyncio.run(seed())
    first = client.get("/api/staff/notifications").json()
    assert first["unread_count"] == baseline + 55 and len(first["items"]) == 50
    client.post(
        "/api/staff/notifications/read",
        json={"ids": [item["id"] for item in first["items"]]},
        headers=HEADERS,
    )
    next_page = client.get("/api/staff/notifications").json()
    assert next_page["unread_count"] == baseline + 5
    assert sum(item["unread"] for item in next_page["items"]) == baseline + 5
