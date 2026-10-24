"""Adaptive Telegram guidance persists safely through the real encrypted inbox."""

import asyncio
import json
import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import RuleOperator
from src.db.models import (
    Batch,
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Course,
    Lead,
    QualificationRule,
    TelegramBot,
)
from src.engine.contracts import Event
from src.engine.guidance_contracts import (
    GuidanceDecision,
    GuidanceInterpretation,
    GuidanceMemory,
    Note,
)
from src.engine.journey import route
from src.telegram import service
from src.telegram.callbacks import callback_data
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


@pytest.fixture
def setup_guidance(journey, monkeypatch):
    async def interpreted(*args, **kwargs):
        return GuidanceInterpretation(intent="guidance")

    monkeypatch.setattr("src.engine.guidance.interpret_turn", interpreted)
    tenant, foreign = journey["tenants"]

    async def seed():
        async with journey["sessions"]() as db:
            c = Course(
                tenant_id=tenant,
                name="Data Exploration",
                is_active=True,
                description="Spreadsheets and practical data projects.",
                application_fee=5000,
            )
            other = Course(tenant_id=foreign, name="Foreign course", is_active=True)
            bot = TelegramBot(
                tenant_id=tenant,
                telegram_bot_id=uuid.uuid4().int % (2**62) + 1,
                token_enc=encrypt_pii("test"),
            )
            db.add_all([c, other, bot])
            await db.flush()
            batch = Batch(
                tenant_id=tenant, course_id=c.id, name="Evening", capacity=5, seats_remaining=5
            )
            lead = Lead(tenant_id=tenant)
            db.add_all(
                [
                    batch,
                    lead,
                    QualificationRule(
                        tenant_id=tenant,
                        course_id=c.id,
                        field="age",
                        operator=RuleOperator.GTE,
                        value=18,
                    ),
                ]
            )
            await db.commit()
            return lead.id, bot.id, c.id, batch.id, other.id

    journey["guidance_ids"] = asyncio.run(seed())
    return journey


def test_english_start_has_no_language_or_forced_course_menu(setup_guidance):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            memory = {"facts": {}, "language": "hi"}
            reply = await route(
                db,
                lead,
                bot,
                Event(update_id=1, user_id=3, chat_id=3, message_id=1, kind="text", text="/start"),
                memory,
            )
            assert not reply.buttons
            assert "course" in reply.text and "language" not in reply.text.lower()
            assert memory["language"] == "en" and memory["guidance"]["active"]

    asyncio.run(exercise())


def test_profile_and_facts_survive_encryption_without_selecting_a_course(
    setup_guidance, monkeypatch
):
    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            stage="exploring",
            response="Let's build on that.",
            question="What would you enjoy using those skills for?",
            updates=[{"topic": "interest", "evidence": "I enjoy spreadsheets"}],
            facts=[{"key": "age", "value": "21", "evidence": "21"}],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        _, bot_id, *_ = setup_guidance["guidance_ids"]
        event_id = await service.accept_update(
            bot_id,
            {
                "update_id": 1,
                "message": {
                    "message_id": 1,
                    "from": {"id": 35},
                    "chat": {"id": 35, "type": "private"},
                    "text": "I am 21 and I enjoy spreadsheets",
                },
            },
        )
        assert event_id is not None
        await service.process_event(event_id)
        async with setup_guidance["sessions"]() as db:
            event = await db.get(ConversationEvent, event_id)
            assert event.status == "done"
            lead_id = event.lead_id
            lead = await db.get(Lead, lead_id)
            reply = await db.scalar(
                select(ConversationReply)
                .options(undefer(ConversationReply.payload_enc))
                .where(ConversationReply.event_id == event_id)
            )
            assert reply.status == "queued"
            assert "What would you enjoy" in decrypt_pii(reply.payload_enc)
            assert lead.current_course_id is None
            row = await db.scalar(
                select(ConversationMemory)
                .options(undefer(ConversationMemory.payload_enc))
                .where(ConversationMemory.lead_id == lead_id)
            )
            assert "spreadsheets" not in row.payload_enc
            memory = json.loads(decrypt_pii(row.payload_enc))
            assert memory["guidance"]["notes"][0]["evidence"] == "I enjoy spreadsheets"
            assert memory["facts"]["age"] == 21
        return lead_id

    lead_id = asyncio.run(exercise())
    signin(setup_guidance["client"])
    response = setup_guidance["client"].get(f"/api/staff/leads/{lead_id}")
    assert response.status_code == 200
    assert response.json()["memory"]["guidance"]["notes"][0]["evidence"] == "I enjoy spreadsheets"
    signin(setup_guidance["client"], "second")
    assert setup_guidance["client"].get(f"/api/staff/leads/{lead_id}").status_code == 404


def test_recommend_confirm_text_then_batch_and_eligibility(setup_guidance, monkeypatch):
    lead_id, bot_id, course_id, batch_id, _ = setup_guidance["guidance_ids"]

    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="select",
            stage="decided",
            response="Here is one option.",
            selected_course_id=course_id,
            matches=[
                {
                    "course_id": course_id,
                    "student_evidence": "spreadsheets",
                    "course_evidence": "practical data projects",
                    "reason": "You can explore the data tasks you enjoy.",
                }
            ],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy spreadsheets")])
            memory = {"facts": {"age": 21}, "guidance": state.model_dump(mode="json")}

            async def turn(text):
                return await route(
                    db,
                    lead,
                    bot,
                    Event(update_id=3, user_id=3, chat_id=3, message_id=3, kind="text", text=text),
                    memory,
                )

            reply = await turn("Can we look at that course?")
            assert "Data Exploration" in reply.text and lead.current_course_id is None
            reply = await turn("yes")
            assert lead.current_course_id == course_id and lead.current_batch_id is None
            assert "Evening" in [b.text for b in reply.buttons]
            reply = await turn("Evening")
            assert lead.current_batch_id == batch_id and "full name" in reply.text

    asyncio.run(exercise())


def test_foreign_or_changed_availability_cannot_be_selected(setup_guidance):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, course_id, batch_id, foreign_id = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            memory = {"facts": {"age": 21}}
            token = callback_data("course", foreign_id.hex, lead.id, bot.id)
            await route(
                db,
                lead,
                bot,
                Event(update_id=4, user_id=3, chat_id=3, message_id=4, kind="callback", text=token),
                memory,
            )
            assert lead.current_course_id is None
            batch = await db.get(Batch, batch_id)
            batch.seats_remaining = 0
            await db.flush()
            token = callback_data("course", course_id.hex, lead.id, bot.id)
            await route(
                db,
                lead,
                bot,
                Event(update_id=5, user_id=3, chat_id=3, message_id=5, kind="callback", text=token),
                memory,
            )
            assert lead.current_course_id is None

    asyncio.run(exercise())


def test_known_failed_rule_cannot_be_bypassed_by_a_direct_name(setup_guidance):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, course_id, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            memory = {"facts": {"age": 17}}
            text = callback_data("course", course_id.hex, lead.id, bot.id)
            reply = await route(
                db,
                lead,
                bot,
                Event(update_id=8, user_id=3, chat_id=3, message_id=8, kind="callback", text=text),
                memory,
            )
            assert "do not meet" in reply.text and lead.current_course_id is None
            assert not reply.buttons

    asyncio.run(exercise())


def test_optional_exploration_and_failure_do_not_erase_profile(setup_guidance, monkeypatch):
    from src.engine.llm_factory import AllProvidersFailedError

    async def fail(*args, **kwargs):
        raise AllProvidersFailedError("synthetic")

    monkeypatch.setattr("src.engine.guidance.request_decision", fail)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            state = GuidanceMemory(notes=[Note(topic="constraint", evidence="I cannot relocate")])
            memory = {"facts": {}, "guidance": state.model_dump(mode="json")}

            async def turn(text):
                return await route(
                    db,
                    lead,
                    bot,
                    Event(update_id=6, user_id=3, chat_id=3, message_id=6, kind="text", text=text),
                    memory,
                )

            reply = await turn("/assessment")
            assert "optional" in reply.text.lower() and "not a" in reply.text.lower()
            assert "onetcenter.org" in reply.text and "I cannot relocate" in str(memory)
            reply = await turn("Help me choose")
            assert "retry" in reply.text and "I cannot relocate" in str(memory)

    asyncio.run(exercise())
