"""Real database consent, reminder leases, freshness, delivery and the two-message cap."""

import asyncio
import itertools
import json
import uuid
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from sqlalchemy import func, select, update

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import LeadStatus
from src.db.models import (
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Institution,
    Lead,
    OutboundMessage,
    TelegramBot,
)
from src.outreach import followups
from src.telegram import outbound, service
from src.telegram.adapter import TelegramAPIError, TelegramClient
from src.telegram.callbacks import callback_data
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_staff_operations import HEADERS, inbound, prepare
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration
numbers = itertools.count(7100)


@pytest.fixture
def outreach(journey, monkeypatch):
    monkeypatch.setattr(followups, "get_sessionmaker", lambda: journey["sessions"])
    monkeypatch.setattr(outbound, "get_sessionmaker", lambda: journey["sessions"])
    monkeypatch.setattr(followups, "get_settings", lambda: journey["settings"])
    sent, generated = [], []

    async def completion(messages, response_format=None, **kwargs):
        generated.append(response_format.__name__)
        data = (
            {"text": "Would you like to continue exploring this course?"}
            if response_format.__name__ == "Hook"
            else {"safe": True}
        )
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(data)))]
        )

    async def deliver(self, chat_id, reply):
        sent.append(reply)
        return 1000 + len(sent)

    monkeypatch.setattr(followups, "generate_completion", completion)
    monkeypatch.setattr(TelegramClient, "send", deliver)
    return {**journey, "sent": sent, "generated": generated}


async def seed(outreach):
    return await prepare(outreach, next(numbers))


async def age(outreach, lead_id):
    async with outreach["sessions"]() as db:
        lead = await db.get(Lead, lead_id)
        old = datetime.now(UTC) - timedelta(days=4)
        lead.status = LeadStatus.DISCOVERING
        lead.followup_consent = True
        lead.last_inbound_at = lead.last_outbound_at = old
        lead.followup_due_at = datetime.now(UTC) - timedelta(seconds=1)
        institution = await db.get(Institution, lead.tenant_id)
        institution.business_hours = {
            day: {"start": "00:00", "end": "23:59"}
            for day in ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
        }
        await db.execute(
            update(ConversationReply)
            .where(
                ConversationReply.event_id.in_(
                    select(ConversationEvent.id).where(ConversationEvent.lead_id == lead_id)
                )
            )
            .values(status="sent")
        )
        await db.commit()
        return lead.tenant_id


async def callback(outreach, bot_id, number, data):
    async with outreach["sessions"]() as db:
        telegram_bot_id = (await db.get(TelegramBot, bot_id)).telegram_bot_id
    event_id = await service.accept_update(
        bot_id,
        {
            "update_id": number,
            "callback_query": {
                "id": f"synthetic-{number}",
                "from": {"id": 83},
                "data": data,
                "message": {
                    "message_id": 1,
                    "from": {"id": telegram_bot_id},
                    "chat": {"id": 83, "type": "private"},
                },
            },
        },
    )
    await service.process_event(event_id)
    return event_id


def test_explicit_consent_and_stop_during_staff_takeover(outreach):
    bot_id, lead_id = asyncio.run(seed(outreach))

    async def exercise():
        async with outreach["sessions"]() as db:
            assert not (await db.get(Lead, lead_id)).followup_consent
        await inbound(bot_id, 2, "/followups")
        async with outreach["sessions"]() as db:
            assert not (await db.get(Lead, lead_id)).followup_consent
        await callback(outreach, bot_id, 3, callback_data("reminders", "on", uuid.uuid4(), bot_id))
        async with outreach["sessions"]() as db:
            assert not (await db.get(Lead, lead_id)).followup_consent
        await callback(outreach, bot_id, 4, callback_data("reminders", "on", lead_id, bot_id))
        async with outreach["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            assert lead.followup_consent and lead.followup_due_at > datetime.now(UTC)

    asyncio.run(exercise())
    client = outreach["client"]
    signin(client)
    assert client.post(f"/api/staff/leads/{lead_id}/takeover", headers=HEADERS).status_code == 200
    event_id = asyncio.run(inbound(bot_id, 5, "/stop"))

    async def stopped():
        async with outreach["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            assert not lead.followup_consent and lead.followup_due_at is None and lead.copilot_mode
            assert await db.scalar(
                select(ConversationReply.id).where(ConversationReply.event_id == event_id)
            )

    asyncio.run(stopped())


def test_exactly_two_reminders_then_cold_without_duplicate_delivery(outreach):
    _, lead_id = asyncio.run(seed(outreach))

    async def exercise():
        for expected in (1, 2):
            tenant_id = await age(outreach, lead_id)
            results = await asyncio.gather(
                followups.process_followup(tenant_id, lead_id),
                followups.process_followup(tenant_id, lead_id),
            )
            ids = [value for value in results if value]
            assert len(ids) == 1
            await asyncio.gather(outbound.send_outbound(ids[0]), outbound.send_outbound(ids[0]))
            async with outreach["sessions"]() as db:
                lead = await db.get(Lead, lead_id)
                assert lead.reengagement_attempts == expected
                assert (lead.status == LeadStatus.COLD) == (expected == 2)
                assert (lead.followup_due_at is None) == (expected == 2)
        assert await followups.process_followup(tenant_id, lead_id) is None
        assert len(outreach["sent"]) == 2 and outreach["generated"] == [
            "Hook",
            "Check",
            "Hook",
            "Check",
        ]
        assert all(len(reply.buttons) == 2 and "/stop" in reply.text for reply in outreach["sent"])

    asyncio.run(exercise())


@pytest.mark.parametrize("command", ["/stop", "/human", "/courses"])
def test_new_activity_during_generation_cannot_publish(outreach, monkeypatch, command):
    bot_id, lead_id = asyncio.run(seed(outreach))
    tenant_id = asyncio.run(age(outreach, lead_id))

    async def changed(context, memory):
        await inbound(bot_id, 2, command)
        return "Would you like to continue this inquiry?"

    monkeypatch.setattr(followups, "generate_hook", changed)
    assert asyncio.run(followups.process_followup(tenant_id, lead_id)) is None

    async def count():
        async with outreach["sessions"]() as db:
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.lead_id == lead_id)
                )
                == 0
            )

    asyncio.run(count())


def test_hours_and_opt_out_are_checked_again_before_the_network(outreach):
    _, lead_id = asyncio.run(seed(outreach))

    async def exercise():
        tenant_id = await age(outreach, lead_id)
        message_id = await followups.process_followup(tenant_id, lead_id)
        assert message_id
        async with outreach["sessions"]() as db:
            (await db.get(Institution, tenant_id)).business_hours = {}
            await db.commit()
        await outbound.send_outbound(message_id)
        async with outreach["sessions"]() as db:
            message = await db.get(OutboundMessage, message_id)
            assert (
                message.status == "queued"
                and message.attempts == 0
                and message.error_code == "followup_outside_hours"
            )
            message.next_attempt_at = None
            (await db.get(Lead, lead_id)).followup_consent = False
            await db.commit()
        await outbound.send_outbound(message_id)
        async with outreach["sessions"]() as db:
            assert (await db.get(OutboundMessage, message_id)).status == "failed"
            assert (await db.get(Lead, lead_id)).reengagement_attempts == 0
        assert not outreach["sent"]

    asyncio.run(exercise())


def test_uncertain_delivery_does_not_schedule_more_outreach(outreach, monkeypatch):
    _, lead_id = asyncio.run(seed(outreach))
    calls = []

    async def uncertain(*args, **kwargs):
        calls.append(1)
        raise TelegramAPIError(0, uncertain=True)

    monkeypatch.setattr(TelegramClient, "send", uncertain)

    async def exercise():
        tenant_id = await age(outreach, lead_id)
        message_id = await followups.process_followup(tenant_id, lead_id)
        await outbound.send_outbound(message_id)
        await outbound.send_outbound(message_id)
        async with outreach["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            assert lead.reengagement_attempts == 1 and lead.followup_due_at is None
            assert (await db.get(OutboundMessage, message_id)).status == "uncertain"
        assert await followups.process_followup(tenant_id, lead_id) is None and len(calls) == 1

    asyncio.run(exercise())


def test_scheduler_and_expired_lease_keep_tenant_boundaries(outreach, monkeypatch):
    from src.tasks.followups import send_followup

    _, lead_id = asyncio.run(seed(outreach))
    queued = []

    async def enqueue(*ids):
        queued.append(ids)

    monkeypatch.setattr(send_followup, "kiq", enqueue)

    async def exercise():
        tenant_id = await age(outreach, lead_id)
        assert await followups.process_followup(outreach["tenants"][1], lead_id) is None
        assert await followups.dispatch_due() >= 1
        assert (str(tenant_id), str(lead_id)) in queued and all(len(ids) == 2 for ids in queued)
        async with outreach["sessions"]() as db:
            row = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            memory = json.loads(decrypt_pii(row.payload_enc))
            memory["followup_claim"] = {"id": "expired", "status": "generating"}
            row.payload_enc = encrypt_pii(json.dumps(memory))
            await db.commit()
        assert await followups.process_followup(tenant_id, lead_id)
        async with outreach["sessions"]() as db:
            row = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            assert json.loads(decrypt_pii(row.payload_enc))["followup_claim"]["id"] != "expired"

    asyncio.run(exercise())


@pytest.mark.parametrize("cause", ["unprocessed_message", "staff_takeover", "disabled"])
def test_pending_inbound_and_takeover_cancel_a_queued_reminder(outreach, cause, monkeypatch):
    bot_id, lead_id = asyncio.run(seed(outreach))
    tenant_id = asyncio.run(age(outreach, lead_id))
    message_id = asyncio.run(followups.process_followup(tenant_id, lead_id))
    if cause == "staff_takeover":
        client = outreach["client"]
        signin(client)
        assert (
            client.post(f"/api/staff/leads/{lead_id}/takeover", headers=HEADERS).status_code == 200
        )
    elif cause == "disabled":
        monkeypatch.setattr(outreach["settings"], "followups_enabled", False)
    else:
        asyncio.run(
            service.accept_update(
                bot_id,
                {
                    "update_id": 2,
                    "message": {
                        "message_id": 2,
                        "from": {"id": 83},
                        "chat": {"id": 83, "type": "private"},
                        "text": "I have a new question",
                    },
                },
            )
        )
    asyncio.run(outbound.send_outbound(message_id))

    async def check():
        async with outreach["sessions"]() as db:
            assert (await db.get(OutboundMessage, message_id)).status == "failed"
            assert (await db.get(Lead, lead_id)).reengagement_attempts == 0
        assert not outreach["sent"]

    asyncio.run(check())


def test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(outreach):
    bot_id, lead_id = asyncio.run(seed(outreach))

    async def exercise():
        tenant_id = await age(outreach, lead_id)
        message_id = await followups.process_followup(tenant_id, lead_id)
        async with outreach["sessions"]() as db:
            (await db.get(Institution, tenant_id)).telegram_daily_send_limit = 0
            await db.commit()
        await outbound.send_outbound(message_id)
        async with outreach["sessions"]() as db:
            message = await db.get(OutboundMessage, message_id)
            assert (
                message.status == "queued"
                and message.error_code == "daily_send_budget"
                and message.attempts == 0
            )
            assert (await db.get(Lead, lead_id)).reengagement_attempts == 0
        await inbound(bot_id, 2, "/stop")
        async with outreach["sessions"]() as db:
            assert (await db.get(OutboundMessage, message_id)).status == "failed"
            (await db.get(Institution, tenant_id)).telegram_daily_send_limit = 1000
            await db.commit()
        assert not outreach["sent"]

    asyncio.run(exercise())


def test_existing_inquiries_upgrade_without_invented_consent(outreach):
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import text

    _, lead_id = asyncio.run(seed(outreach))
    tenant_id = asyncio.run(age(outreach, lead_id))
    reminder_id = asyncio.run(followups.process_followup(tenant_id, lead_id))
    assert reminder_id

    async def in_flight():
        async with outreach["sessions"]() as db:
            message = OutboundMessage(
                tenant_id=tenant_id,
                lead_id=lead_id,
                kind="followup",
                dedup_key="followup:rollback-flight",
                payload_enc=encrypt_pii('{"text":"Synthetic reminder"}'),
                status="sending",
                attempts=1,
            )
            db.add(message)
            await db.commit()
            return message.id

    uncertain_id = asyncio.run(in_flight())
    command.downgrade(Config("alembic.ini"), "9c5027e2d614")

    async def old():
        async with outreach["sessions"]() as db:
            delivery = (
                await db.execute(
                    text("SELECT status,error_code FROM outbound_messages WHERE id=:id"),
                    {"id": reminder_id},
                )
            ).first()
            assert delivery.status == "failed" and delivery.error_code == "followup_rollback"
            uncertain = await db.scalar(
                text("SELECT status FROM outbound_messages WHERE id=:id"), {"id": uncertain_id}
            )
            assert uncertain == "uncertain"
            return await db.scalar(text("SELECT status FROM leads WHERE id=:id"), {"id": lead_id})

    status = asyncio.run(old())
    command.upgrade(Config("alembic.ini"), "head")

    async def check():
        async with outreach["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            assert lead.status.name == status
            assert (
                not lead.followup_consent
                and lead.followup_due_at is None
                and lead.followup_consent_updated_at is None
            )

    asyncio.run(check())


@pytest.mark.parametrize("blocker", ["unknown_hours", "closed_hours", "inactive_course"])
def test_no_generation_without_a_valid_office_window_and_course(outreach, blocker):
    from src.db.models import Course

    _, lead_id = asyncio.run(seed(outreach))

    async def exercise():
        tenant_id = await age(outreach, lead_id)
        async with outreach["sessions"]() as db:
            if blocker == "inactive_course":
                course = Course(
                    tenant_id=tenant_id, name="Archived course", application_fee=0, is_active=False
                )
                db.add(course)
                await db.flush()
                (await db.get(Lead, lead_id)).current_course_id = course.id
            else:
                (await db.get(Institution, tenant_id)).business_hours = (
                    None if blocker == "unknown_hours" else {}
                )
            await db.commit()
        assert await followups.process_followup(tenant_id, lead_id) is None
        assert not outreach["generated"] and not outreach["sent"]

    asyncio.run(exercise())
