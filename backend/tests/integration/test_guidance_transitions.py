"""Guidance interruptions and academic corrections preserve admissions invariants."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from litellm.exceptions import ContextWindowExceededError

from src.db.enums import LeadStatus
from src.db.models import Lead, TelegramBot
from src.engine.contracts import Event, Reply
from src.engine.guidance_contracts import (
    GuidanceDecision,
    GuidanceInterpretation,
    GuidanceMemory,
    Note,
)
from src.engine.journey import route
from tests.integration.test_adaptive_guidance import setup_guidance as setup_guidance
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_guidance_correction_invalidates_an_existing_eligible_result(setup_guidance, monkeypatch):
    async def plan(*args, **kwargs):
        return GuidanceDecision(
            action="ask",
            question="Would you like to explore another direction?",
            facts=[{"key": "age", "value": "17", "evidence": "17"}],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, cid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            lead.current_course_id, lead.current_batch_id = cid, bid
            lead.status = LeadStatus.ADMISSION_READY
            memory = {
                "facts": {"age": 21},
                "eligibility": {"outcome": "eligible", "rules": []},
                "guidance": GuidanceMemory().model_dump(mode="json"),
            }
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=10,
                    user_id=3,
                    chat_id=3,
                    message_id=10,
                    kind="text",
                    text="Actually my age is 17",
                ),
                memory,
            )
            assert "another direction" in reply.text
            assert memory["facts"]["age"] == 17
            assert memory["eligibility"]["outcome"] == "not_eligible"
            assert lead.status != LeadStatus.ADMISSION_READY
            assert lead.current_course_id == cid

    asyncio.run(exercise())


def test_faq_interrupt_does_not_destroy_pending_guidance_or_profile(setup_guidance, monkeypatch):
    monkeypatch.setattr(
        "src.engine.guidance.interpret_turn",
        AsyncMock(return_value=GuidanceInterpretation(intent="faq")),
    )
    monkeypatch.setattr(
        "src.engine.journey.answer_question",
        AsyncMock(return_value=Reply(text="The demo library opens at 9 AM.")),
    )

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            state = GuidanceMemory(
                notes=[Note(topic="interest", evidence="I enjoy drawing")],
                last_question="What have you enjoyed creating?",
            )
            memory = {"facts": {}, "guidance": state.model_dump(mode="json")}
            before = memory["guidance"].copy()
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=11,
                    user_id=3,
                    chat_id=3,
                    message_id=11,
                    kind="text",
                    text="When is the library open?",
                ),
                memory,
            )
            assert "9 AM" in reply.text and memory["guidance"] == before
            assert lead.current_course_id is None

    asyncio.run(exercise())


@pytest.mark.parametrize("context_failure", [False, True])
def test_validated_age_correction_survives_reply_generation_failure(
    setup_guidance, monkeypatch, context_failure
):
    from src.engine.llm_factory import AllProvidersFailedError

    monkeypatch.setattr(
        "src.engine.guidance.interpret_turn",
        AsyncMock(
            return_value=GuidanceInterpretation(
                intent="guidance", facts=[{"key": "age", "value": "17", "evidence": "my age is 17"}]
            )
        ),
    )
    monkeypatch.setattr(
        "src.engine.guidance.request_decision",
        AsyncMock(
            side_effect=(
                ContextWindowExceededError("synthetic", model="synthetic", llm_provider="openai")
                if context_failure
                else AllProvidersFailedError("synthetic")
            )
        ),
    )

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, cid, bid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            lead.current_course_id, lead.current_batch_id = cid, bid
            lead.status = LeadStatus.ADMISSION_READY
            memory = {
                "facts": {"age": 21},
                "eligibility": {"outcome": "eligible"},
                "guidance": GuidanceMemory().model_dump(mode="json"),
            }
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=12,
                    user_id=3,
                    chat_id=3,
                    message_id=12,
                    kind="text",
                    text="Actually my age is 17",
                ),
                memory,
            )
            assert memory["facts"]["age"] == 17
            assert memory["eligibility"]["outcome"] == "not_eligible"
            assert lead.current_course_id == cid and lead.status != LeadStatus.ADMISSION_READY
            assert "saved" in reply.text.lower() and "retry" in reply.text

    asyncio.run(exercise())


def test_catalog_closure_during_model_call_is_respected_before_rendering(
    setup_guidance, monkeypatch
):
    from sqlalchemy import update

    from src.db.models import Course

    _, _, course_id, _, _ = setup_guidance["guidance_ids"]

    async def plan(*args, **kwargs):
        async with setup_guidance["sessions"]() as other_db:
            await other_db.execute(
                update(Course).where(Course.id == course_id).values(is_active=False)
            )
            await other_db.commit()
        return GuidanceDecision(
            action="recommend",
            matches=[
                {
                    "course_id": course_id,
                    "student_evidence": "I enjoy spreadsheets",
                    "course_evidence": "practical data projects",
                    "reason": "A possible direction to explore.",
                }
            ],
        )

    monkeypatch.setattr("src.engine.guidance.request_decision", plan)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            memory = {
                "facts": {"age": 21},
                "guidance": GuidanceMemory(
                    notes=[Note(topic="interest", evidence="I enjoy spreadsheets")]
                ).model_dump(mode="json"),
            }
            reply = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=13,
                    user_id=3,
                    chat_id=3,
                    message_id=13,
                    kind="text",
                    text="Show me that option",
                ),
                memory,
            )
            assert "Data Exploration" not in reply.text
            assert not reply.buttons and lead.current_course_id is None

    asyncio.run(exercise())


def test_failed_depth_change_invalidates_the_previous_course_confirmation(
    setup_guidance, monkeypatch
):
    from src.engine.llm_factory import AllProvidersFailedError
    from src.telegram.callbacks import callback_data

    monkeypatch.setattr(
        "src.engine.guidance.request_decision",
        AsyncMock(side_effect=AllProvidersFailedError("synthetic")),
    )

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lead_id, bot_id, cid, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lead_id), await db.get(TelegramBot, bot_id)
            memory = {
                "facts": {"age": 21},
                "guidance": GuidanceMemory(pending_course=cid).model_dump(mode="json"),
            }
            token = callback_data("guide", "deeper", lead.id, bot.id)
            await route(
                db,
                lead,
                bot,
                Event(
                    update_id=14, user_id=3, chat_id=3, message_id=14, kind="callback", text=token
                ),
                memory,
            )
            assert memory["guidance"]["pending_course"] is None
            await route(
                db,
                lead,
                bot,
                Event(update_id=15, user_id=3, chat_id=3, message_id=15, kind="text", text="yes"),
                memory,
            )
            assert lead.current_course_id is None

    asyncio.run(exercise())
