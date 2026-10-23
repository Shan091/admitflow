"""Both Telegram outboxes share the cap, defer durably and honor provider delays."""

import asyncio
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from src.db.models import ConversationEvent, ConversationReply, Institution, OutboundMessage
from src.engine.contracts import Reply
from src.telegram import budget, outbound, service
from src.telegram.adapter import TelegramAPIError, TelegramClient
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_staff_operations import HEADERS, prepare
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_shared_budget_preserves_queues_and_settings_wake_deliveries(journey, monkeypatch):
    monkeypatch.setattr(outbound, "get_sessionmaker", lambda: journey["sessions"])
    calls = []

    async def send(self, chat_id, reply):
        calls.append(reply.text)
        return 900 + len(calls)

    monkeypatch.setattr(TelegramClient, "send", send)
    _, lead_id = asyncio.run(prepare(journey, 6200))
    client = journey["client"]
    assert client.get("/api/staff/delivery-budget").status_code == 401
    signin(client)
    config = client.get("/api/staff/settings").json()
    assert config["telegram_daily_send_limit"] == 1000

    def limit(value):
        result = client.put(
            "/api/staff/settings",
            json={**config, "telegram_daily_send_limit": value},
            headers=HEADERS,
        )
        assert result.status_code == 200, result.text

    limit(0)

    async def first():
        async with journey["sessions"]() as db:
            return await db.scalar(
                select(ConversationReply.id).where(
                    ConversationReply.tenant_id == journey["tenants"][0]
                )
            )

    reply_id = asyncio.run(first())
    asyncio.run(service.send_reply(reply_id))
    assert not calls
    stats = client.get("/api/staff/delivery-budget").json()
    assert stats["warning"] and stats["deferred"] == 1 and stats["attempts"] == 0

    async def state():
        async with journey["sessions"]() as db:
            row = await db.get(ConversationReply, reply_id)
            assert row.status == "queued" and row.attempts == 0
            assert row.next_attempt_at > datetime.now(UTC)

    asyncio.run(state())
    limit(1)

    async def send_reply():
        await asyncio.gather(service.send_reply(reply_id), service.send_reply(reply_id))

    asyncio.run(send_reply())
    assert len(calls) == 1

    async def second():
        async with journey["sessions"]() as db:
            message_id = await outbound.enqueue_outbound(
                db,
                tenant_id=journey["tenants"][0],
                lead_id=lead_id,
                kind="staff_reply",
                dedup_key="budget:staff",
                reply=Reply(text="A reviewed staff reply"),
            )
            await db.commit()
        await outbound.send_outbound(message_id)
        async with journey["sessions"]() as db:
            row = await db.get(OutboundMessage, message_id)
            assert (
                row.status == "queued"
                and row.attempts == 0
                and row.error_code == "daily_send_budget"
            )
        return message_id

    message_id = asyncio.run(second())
    stats = client.get("/api/staff/delivery-budget").json()
    assert stats["attempts"] == stats["confirmed_sent"] == 1 and stats["deferred"] == 1
    signin(client, "second")
    assert client.get("/api/staff/delivery-budget").json()["deferred"] == 0
    signin(client)
    limit(2)

    async def statistics_unavailable(*args):
        pass  # A confirmed send must still appear if its Redis stats update is lost.

    monkeypatch.setattr(budget, "record_sent", statistics_unavailable)

    async def finish():
        await asyncio.gather(outbound.send_outbound(message_id), outbound.send_outbound(message_id))

    asyncio.run(finish())
    assert len(calls) == 2
    stats = client.get("/api/staff/delivery-budget").json()
    assert stats["attempts"] == stats["confirmed_sent"] == 2 and stats["deferred"] == 0
    older = dict(config)
    older.pop("telegram_daily_send_limit")
    assert (
        client.put("/api/staff/settings", json=older, headers=HEADERS).json()[
            "telegram_daily_send_limit"
        ]
        == 2
    )
    assert (
        client.put(
            "/api/staff/settings", json={**config, "telegram_daily_send_limit": -1}, headers=HEADERS
        ).status_code
        == 422
    )
    signin(client, email="agent@example.test")
    assert client.put("/api/staff/settings", json=config, headers=HEADERS).status_code == 403


@pytest.mark.parametrize("standalone", [False, True])
def test_provider_retry_delay_is_not_shortened(journey, monkeypatch, standalone):
    monkeypatch.setattr(outbound, "get_sessionmaker", lambda: journey["sessions"])

    rejected_at = []

    async def limited(*args, **kwargs):
        rejected_at.append(datetime.now(UTC))
        raise TelegramAPIError(429, retry_after=3600)

    monkeypatch.setattr(TelegramClient, "send", limited)
    _, lead_id = asyncio.run(prepare(journey, 6202 if standalone else 6201))

    async def exercise():
        async with journey["sessions"]() as db:
            response = await db.scalar(
                select(ConversationReply)
                .join_from(ConversationReply, ConversationEvent)
                .where(ConversationEvent.lead_id == lead_id)
            )
            if standalone:
                response.status = "sent"
                row_id = await outbound.enqueue_outbound(
                    db,
                    tenant_id=journey["tenants"][0],
                    lead_id=lead_id,
                    kind="staff_reply",
                    dedup_key="budget:429",
                    reply=Reply(text="Synthetic rate delay"),
                )
                await db.commit()
            else:
                row_id = response.id
            delivery = await db.get(OutboundMessage if standalone else ConversationReply, row_id)
            delivery.attempts = 3
            await db.commit()
        async with journey["sessions"]() as db:
            institution = await db.get(Institution, journey["tenants"][0])
            institution.telegram_daily_send_limit = 1000
            await db.commit()
        before = datetime.now(UTC)
        await (outbound.send_outbound(row_id) if standalone else service.send_reply(row_id))
        async with journey["sessions"]() as db:
            row = await db.get(OutboundMessage if standalone else ConversationReply, row_id)
            assert row.status == "queued" and row.attempts == 4
            assert row.next_attempt_at >= before + timedelta(seconds=3599)
            assert row.next_attempt_at >= rejected_at[-1] + timedelta(seconds=3600)

    asyncio.run(exercise())


def test_budget_migration_preserves_existing_institution(journey):
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import text
    from sqlalchemy.exc import IntegrityError

    institution_id = journey["tenants"][0]
    command.downgrade(Config("alembic.ini"), "f129a064c5e8")

    async def before():
        async with journey["sessions"]() as db:
            return await db.scalar(
                text("SELECT name FROM institutions WHERE id=:id"), {"id": institution_id}
            )

    name = asyncio.run(before())
    command.upgrade(Config("alembic.ini"), "head")

    async def after():
        async with journey["sessions"]() as db:
            institution = await db.get(Institution, institution_id)
            assert institution.name == name and institution.telegram_daily_send_limit == 1000
            with pytest.raises(IntegrityError):
                institution.telegram_daily_send_limit = -1
                await db.commit()
            await db.rollback()

    asyncio.run(after())
