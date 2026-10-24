"""Fresh context and natural collection preserve institution-owned records."""

import asyncio
import json
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import event as sql_event
from sqlalchemy import select

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import LeadStatus
from src.db.models import (
    Application,
    ConversationEvent,
    ConversationReply,
    HumanRequest,
    Lead,
    TelegramBot,
)
from src.engine.application_profile import Detail
from src.engine.applications import ApplicationTurn
from src.engine.contracts import Event, Reply
from src.engine.journey import route
from src.telegram import service
from src.telegram.callbacks import callback_data
from tests.integration.test_adaptive_guidance import setup_guidance as setup_guidance
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def event(text, *, callback=False, message_id=20):
    return Event(
        update_id=30,
        user_id=3,
        chat_id=3,
        message_id=message_id,
        kind="callback" if callback else "text",
        text=text,
    )


@pytest.mark.parametrize("submitted,held", [(False, False), (True, False), (False, True)])
def test_reset_needs_confirmation_and_preserves_business_ownership(setup_guidance, submitted, held):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, batch, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            lead.current_course_id, lead.current_batch_id = cid, batch
            lead.followup_consent = True
            lead.name_enc = encrypt_pii("Institution contact name")
            memory = (
                {
                    "facts": {"age": 21},
                    "guidance": {"notes": []},
                    "application_draft": {"values": {"full_name": "Old Name"}},
                    "handoff": {"reason": "staff_review"},
                }
                if held
                else {
                    "facts": {"age": 21},
                    "application_draft": {"values": {"full_name": "Old Name"}},
                }
            )
            if submitted:
                db.add(
                    Application(
                        tenant_id=lead.tenant_id,
                        lead_id=lid,
                        course_id=cid,
                        batch_id=batch,
                        full_name_enc=encrypt_pii("Stored Student"),
                    )
                )
                lead.status = LeadStatus.PAYMENT_PENDING
            if held:
                db.add(HumanRequest(tenant_id=lead.tenant_id, lead_id=lid))
                lead.status, lead.copilot_mode = LeadStatus.HANDED_OFF, True
            await db.flush()
            original_status = lead.status
            prompt = await route(db, lead, bot, event("/reset"), memory)
            assert memory["facts"] == {"age": 21} and "application_draft" in memory
            confirm = next(b.data for b in prompt.buttons if b.text == "Start fresh")
            reply = await route(db, lead, bot, event(confirm, callback=True), memory)
            assert memory["facts"] == {} and "application_draft" not in memory
            assert "history_after" in memory and "guidance" not in memory
            assert lead.followup_consent is True
            assert decrypt_pii(lead.name_enc) == "Institution contact name"
            if submitted or held:
                assert lead.status == original_status and lead.current_course_id == cid
            else:
                assert lead.current_course_id is None and lead.current_batch_id is None
                assert lead.status == LeadStatus.NEW
            if submitted:
                assert await db.scalar(select(Application.id).where(Application.lead_id == lid))
            if held:
                assert lead.copilot_mode and memory["handoff"]["reason"] == "staff_review"
            stale = await route(db, lead, bot, event(confirm, callback=True), memory)
            assert "Start fresh" not in [b.text for b in stale.buttons]
            old_choice = await route(
                db,
                lead,
                bot,
                event(callback_data("course", cid.hex, lid, bid), callback=True, message_id=10),
                memory,
            )
            assert "expired" in old_choice.text
            assert reply.text

    asyncio.run(exercise())


def test_plain_eligibility_answer_needs_no_model_call(setup_guidance, monkeypatch):
    from src.engine.guidance_contracts import GuidanceInterpretation, StudyFact

    calls = []

    async def interpret(*args, **kwargs):
        calls.append("interpretation")
        return GuidanceInterpretation(
            intent="qualification", facts=[StudyFact(key="age", value="21", evidence="21")]
        )

    async def unexpected(*args, **kwargs):
        raise AssertionError("Redundant classifier, extraction or planning request")

    monkeypatch.setattr("src.engine.guidance.interpret_turn", interpret)
    monkeypatch.setattr("src.engine.guidance.request_decision", unexpected)
    monkeypatch.setattr("src.engine.journey.decide", unexpected)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, batch, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            lead.current_course_id, lead.current_batch_id = cid, batch
            memory = {"facts": {}}
            from src.engine.journey import advance_application, qualify

            await advance_application(
                db, lead, bot, memory, await qualify(db, lead, bot, memory, "", [])
            )
            reply = await route(db, lead, bot, event("21"), memory)
            assert calls == [] and memory["facts"]["age"] == 21
            assert "full name" in reply.text and not reply.buttons

    asyncio.run(exercise())


def test_model_history_excludes_pre_reset_context_in_one_scoped_query(setup_guidance):
    from src.engine.model_history import model_history

    async def exercise():
        lid, bid, *_ = setup_guidance["guidance_ids"]
        ids = []
        for i, text in enumerate(["My old preference is nursing", "I now enjoy design"], start=1):
            ids.append(
                await service.accept_update(
                    bid,
                    {
                        "update_id": i,
                        "message": {
                            "message_id": i,
                            "from": {"id": 800},
                            "chat": {"id": 800, "type": "private"},
                            "text": text,
                        },
                    },
                )
            )
        boundary = datetime.now(UTC)
        async with setup_guidance["sessions"]() as db:
            for i, eid in enumerate(ids):
                row = await db.get(ConversationEvent, eid)
                row.status = "done"
                row.created_at = boundary + timedelta(seconds=-10 if i == 0 else 1)
                if i == 1:
                    lid = row.lead_id
                    db.add(
                        ConversationReply(
                            tenant_id=row.tenant_id,
                            event_id=eid,
                            payload_enc=encrypt_pii(
                                Reply(text="Tell me about your design interests.").model_dump_json()
                            ),
                            status="sent",
                            created_at=boundary + timedelta(seconds=2),
                        )
                    )
            await db.commit()
            lead = await db.get(Lead, lid)
            statements = []

            def capture(*args):
                statements.append(args[2])

            engine = db.bind.sync_engine
            sql_event.listen(engine, "before_cursor_execute", capture)
            try:
                context = await model_history(db, lead, {"history_after": boundary.isoformat()})
            finally:
                sql_event.remove(engine, "before_cursor_execute", capture)
            assert len(statements) == 1
            assert [x["content"] for x in context] == [
                "I now enjoy design",
                "Tell me about your design interests.",
            ]
            assert "nursing" not in json.dumps(context)
            assert (
                await model_history(db, await db.get(Lead, setup_guidance["guidance_ids"][0]), {})
                == []
            )
            bot = await db.get(TelegramBot, bid)
            callback = await service.accept_update(
                bid,
                {
                    "update_id": 3,
                    "callback_query": {
                        "id": "synthetic",
                        "from": {"id": 800},
                        "message": {
                            "message_id": 50,
                            "from": {"id": bot.telegram_bot_id},
                            "chat": {"id": 800, "type": "private"},
                        },
                        "data": callback_data(
                            "batch", setup_guidance["guidance_ids"][3].hex, lid, bid
                        ),
                    },
                },
            )
            row = await db.get(ConversationEvent, callback)
            row.status, row.created_at = "done", boundary + timedelta(seconds=3)
            await db.commit()
            statements.clear()
            sql_event.listen(engine, "before_cursor_execute", capture)
            try:
                with_choice = await model_history(db, lead, {"history_after": boundary.isoformat()})
            finally:
                sql_event.remove(engine, "before_cursor_execute", capture)
            assert len(statements) == 2
            assert with_choice[-1]["content"] == "Selected batch: Evening"

    asyncio.run(exercise())


def test_multiple_details_and_corrections_fill_only_evidenced_fields(setup_guidance, monkeypatch):
    async def interpret(*args, **kwargs):
        return ApplicationTurn(
            intent="answer",
            details=[
                Detail(key="full_name", value="Anu Menon", evidence="my name is Anu Menon"),
                Detail(key="dob", value="2005-03-14", evidence="DOB is 2005-03-14"),
                Detail(key="address", value="Invented address", evidence="my name is Anu Menon"),
            ],
        )

    monkeypatch.setattr("src.engine.applications.decide", interpret)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, batch, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            lead.current_course_id, lead.current_batch_id = cid, batch
            memory = {"facts": {"age": 21}, "application_details": {"full_name": "Anu Nair"}}
            await route(db, lead, bot, event("/apply"), memory)
            reply = await route(
                db,
                lead,
                bot,
                event("Actually my name is Anu Menon and my DOB is 2005-03-14"),
                memory,
            )
            assert memory["application_draft"]["values"] == {
                "full_name": "Anu Menon",
                "dob": "2005-03-14",
            }
            assert "parent or guardian" in reply.text and "encrypted" not in reply.text
            assert await db.scalar(select(Application.id).where(Application.lead_id == lid)) is None

    asyncio.run(exercise())


def test_confirmed_intake_moves_to_missing_details_without_application_menu(setup_guidance):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, batch, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            lead.current_course_id = cid
            memory = {"facts": {"age": 21}, "application_details": {"full_name": "Anu Nair"}}
            reply = await route(
                db,
                lead,
                bot,
                event(callback_data("batch", batch.hex, lid, bid), callback=True),
                memory,
            )
            assert "date of birth" in reply.text and "full name" not in reply.text
            assert memory["application_draft"]["values"]["full_name"] == "Anu Nair"
            assert not reply.buttons and "encrypted" not in reply.text
            assert await db.scalar(select(Application.id).where(Application.lead_id == lid)) is None

    asyncio.run(exercise())


def test_greeting_question_pause_and_resume_do_not_become_form_values(setup_guidance, monkeypatch):
    async def faq(*args, **kwargs):
        return Reply(text="The counselling room is Lotus Hall.")

    monkeypatch.setattr("src.engine.journey.answer_question", faq)

    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, batch, *_ = setup_guidance["guidance_ids"]
            lead, bot = await db.get(Lead, lid), await db.get(TelegramBot, bid)
            lead.current_course_id, lead.current_batch_id = cid, batch
            memory = {"facts": {"age": 21}}
            await route(db, lead, bot, event("/apply"), memory)
            greeting = await route(db, lead, bot, event("hi"), memory)
            assert "application" in greeting.text.lower()
            assert memory["application_draft"]["values"] == {}
            answer = await route(db, lead, bot, event("Where is the counselling room?"), memory)
            assert "Lotus Hall" in answer.text and memory["application_draft"]["values"] == {}
            await route(db, lead, bot, event("Anu Nair"), memory)
            await route(db, lead, bot, event("/pause"), memory)
            assert memory["application_draft"]["values"] == {"full_name": "Anu Nair"}
            resumed = await route(db, lead, bot, event("/apply"), memory)
            assert "date of birth" in resumed.text
            assert memory["application_draft"]["values"] == {"full_name": "Anu Nair"}

    asyncio.run(exercise())
