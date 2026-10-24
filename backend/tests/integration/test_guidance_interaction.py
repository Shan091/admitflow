"""Contextual option taps persist as answers, never hidden course selections."""

import asyncio
import json

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii
from src.db.models import (
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Lead,
    TelegramBot,
)
from src.engine.contracts import Event, Reply
from src.engine.guidance_contracts import GuidanceDecision, GuidanceInterpretation, ProfileUpdate
from src.engine.journey import route
from src.telegram import service
from tests.integration.test_adaptive_guidance import setup_guidance as setup_guidance
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_signed_option_is_saved_as_literal_answer_without_selecting_a_course(
    setup_guidance, monkeypatch
):
    seen = []

    async def interpreted(text, *args, **kwargs):
        seen.append(text)
        return GuidanceInterpretation(
            intent="guidance",
            updates=[ProfileUpdate(topic="interest", evidence=text)] if text else [],
        )

    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            question="Which direction would you like to explore?",
            answer_options=["Data Exploration", "Something creative"],
        )

    monkeypatch.setattr("src.engine.guidance.interpret_turn", interpreted)
    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        _, bid, *_ = setup_guidance["guidance_ids"]
        async with setup_guidance["sessions"]() as db:
            bot = await db.get(TelegramBot, bid)
            telegram_id = bot.telegram_bot_id
        first = await service.accept_update(
            bid,
            {
                "update_id": 1,
                "message": {
                    "message_id": 1,
                    "from": {"id": 9},
                    "chat": {"id": 9, "type": "private"},
                    "text": "/guide",
                },
            },
        )
        await service.process_event(first)
        async with setup_guidance["sessions"]() as db:
            row = await db.scalar(
                select(ConversationReply)
                .options(undefer(ConversationReply.payload_enc))
                .where(ConversationReply.event_id == first)
            )
            reply = Reply.model_validate_json(decrypt_pii(row.payload_enc))
            assert "Not sure yet" in [b.text for b in reply.buttons]
            choice = next(b.data for b in reply.buttons if b.text == "Data Exploration")
        second = await service.accept_update(
            bid,
            {
                "update_id": 2,
                "callback_query": {
                    "id": "synthetic",
                    "from": {"id": 9},
                    "data": choice,
                    "message": {
                        "message_id": 2,
                        "from": {"id": telegram_id},
                        "chat": {"id": 9, "type": "private"},
                    },
                },
            },
        )
        await service.process_event(second)
        await service.process_event(second)
        async with setup_guidance["sessions"]() as db:
            event = await db.scalar(
                select(ConversationEvent)
                .options(undefer(ConversationEvent.payload_enc))
                .where(ConversationEvent.id == second)
            )
            body = Event.model_validate_json(decrypt_pii(event.payload_enc))
            assert body.selected_answer == "Data Exploration"
            lead = await db.get(Lead, event.lead_id)
            assert lead.current_course_id is None and seen[-1] == "Data Exploration"
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(ConversationReply)
                    .where(ConversationReply.event_id == second)
                )
                == 1
            )
            memory = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead.id)
            )
            assert (
                "Data Exploration"
                in json.loads(decrypt_pii(memory.payload_enc))["guidance"]["notes"][0]["evidence"]
            )
            from src.engine.timeline import timeline

            messages, _ = await timeline(db, lead.tenant_id, lead.id, None)
            assert any(m["text"] == "Answered: Data Exploration" for m in messages)
            from src.engine.journey import recent_history

            assert any(m["content"] == "Data Exploration" for m in await recent_history(db, lead))

    asyncio.run(exercise())


def test_interview_probe_is_replaced_without_an_extra_model_request(setup_guidance, monkeypatch):
    calls = []

    async def plan(*args, **kwargs):
        calls.append(1)
        return GuidanceDecision(action="ask", question="Can you describe the project you built?")

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            memory = {"facts": {}}
            reply = await route(
                db,
                lead,
                bot,
                Event(update_id=1, user_id=8, chat_id=8, message_id=1, kind="text", text="some"),
                memory,
            )
            assert calls == [1] and "Can you describe" not in reply.text
            assert [b.text for b in reply.buttons] == [
                "Browse available courses",
                "Explore interests further",
                "Ask admissions staff",
            ]
            assert lead.current_course_id is None

    asyncio.run(exercise())


def test_real_eligibility_question_does_not_offer_suggested_ages(setup_guidance, monkeypatch):
    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            question="How old are you?",
            question_field="age",
            answer_options=["18", "21"],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            memory = {"facts": {}, "guidance": {"questions_since_direction": 3}}
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=1, user_id=8, chat_id=8, message_id=1, kind="text", text="I like data"
                ),
                memory,
            )
            assert reply.text == "How old are you?" and not reply.buttons
            assert memory["facts"] == {}

    asyncio.run(exercise())


def test_new_background_information_keeps_useful_discovery_open(setup_guidance, monkeypatch):
    async def interpreted(*args, **kwargs):
        return GuidanceInterpretation(
            intent="guidance",
            updates=[ProfileUpdate(topic="background", evidence="I finished Class 12 commerce")],
        )

    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            question="What matters most to you in your next course?",
            answer_options=["Learning something I enjoy", "Preparing for work"],
        )

    monkeypatch.setattr("src.engine.guidance.interpret_turn", interpreted)
    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            memory = {"facts": {}, "guidance": {"questions_since_direction": 2}}
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=1,
                    user_id=8,
                    chat_id=8,
                    message_id=1,
                    kind="text",
                    text="I finished Class 12 commerce",
                ),
                memory,
            )
            assert "What matters most" in reply.text
            assert "Preparing for work" in [b.text for b in reply.buttons]
            assert lead.current_course_id is None and memory["facts"] == {}

    asyncio.run(exercise())


@pytest.mark.parametrize("changed_context", ["text", "course", "reset"])
def test_previous_answer_expires_when_context_changes(setup_guidance, monkeypatch, changed_context):
    from src.telegram.callbacks import callback_data

    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            question="What matters most to you?",
            answer_options=["Creativity", "Helping people"],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            memory = {"facts": {}}

            def event(text, *, callback=False, mid=20):
                return Event(
                    update_id=mid,
                    user_id=8,
                    chat_id=8,
                    message_id=mid,
                    kind="callback" if callback else "text",
                    text=text,
                )

            initial = await route(db, lead, bot, event("/guide"), memory)
            answer = initial.buttons[0].data
            if changed_context == "course":
                await route(
                    db,
                    lead,
                    bot,
                    event(callback_data("course", cid.hex, lid, bid), callback=True),
                    memory,
                )
            elif changed_context == "reset":
                prompt = await route(db, lead, bot, event("/reset"), memory)
                await route(db, lead, bot, event(prompt.buttons[0].data, callback=True), memory)
            else:
                await route(db, lead, bot, event("I enjoy art"), memory)
            current_offer = memory.get("guidance_answers")
            stale_event = event(answer, callback=True, mid=10)
            result = await route(db, lead, bot, stale_event, memory)
            assert stale_event.selected_answer is None
            assert memory.get("guidance_answers") == current_offer
            assert "out of date" in result.text.lower() or "expired" in result.text.lower()

    asyncio.run(exercise())


def test_unanswered_prerequisite_is_not_repeated_as_an_interrogation(setup_guidance, monkeypatch):
    async def plan(*args, **kwargs):
        return GuidanceDecision(action="ask", question="What is your age?", question_field="age")

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            memory = {
                "facts": {},
                "guidance": {"last_field": "age", "last_question": "What is your age?"},
            }
            reply = await route(
                db,
                lead,
                bot,
                Event(update_id=1, user_id=8, chat_id=8, message_id=1, kind="text", text="some"),
                memory,
            )
            assert "What is your age?" not in reply.text
            assert "Keep exploring" in [b.text for b in reply.buttons]
            assert not memory["facts"] and memory["guidance"]["last_field"] is None

    asyncio.run(exercise())
