"""Synthetic student-to-staff journey against PostgreSQL, without external API calls."""

import asyncio
import itertools
import json
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from typing import Any

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import undefer

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import LeadStatus, RuleOperator
from src.db.models import (
    Batch,
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Course,
    DocumentChunk,
    HumanRequest,
    KnowledgeUpload,
    Lead,
    QualificationRule,
    TelegramBot,
)
from src.engine.contracts import Reply
from src.knowledge.processing import process_upload
from src.telegram import service
from src.telegram.adapter import TelegramAPIError, TelegramClient
from tests.integration.test_knowledge_workspace import fake_embeddings, send, signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


async def completion(
    messages: list[dict[str, str]], response_format: Any = None, **kwargs: Any
) -> Any:
    text = messages[-1]["content"]
    schema = response_format.__name__
    if schema == "Interpretation":
        result = {"intent": "question" if "?" in text else "qualification"}
    elif schema == "GuidanceInterpretation":
        data = json.loads(text)
        message = data["message"]
        if "?" in message:
            result = {"intent": "faq"}
        else:
            field = "age" if "age" in message.lower() else data["last_field"]
            result = {
                "intent": "qualification",
                "facts": [{"key": field, "value": message.split()[-1], "evidence": message}],
            }
    elif schema == "ApplicationTurn":
        result = {"intent": "faq", "details": []}
    elif schema == "ResolvedQuestion":
        result = {"query": json.loads(text)["question"], "needs_clarification": False}
    elif schema == "PassageRanking":
        result = {"ordered_ids": [row["id"] for row in json.loads(text)["passages"]]}
    elif schema == "Extraction":
        if "age" in text:
            value, key = text.split()[-1], "age"
        else:
            key = "age" if "Active question field: age" in messages[0]["content"] else "marks"
            value = text
        result = {"facts": [{"key": key, "value": value, "evidence": value}], "declined": False}
    else:
        result = {
            "supported": "hostel" in json.loads(text)["question"].lower(),
            "passage": 0,
            "quote": "Hostel accommodation is available on campus.",
        }
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(result)))]
    )


@pytest.fixture
def journey(workspace: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from src.engine import journey as engine

    monkeypatch.setattr(service, "get_sessionmaker", lambda: workspace["sessions"])
    monkeypatch.setattr(engine, "get_settings", lambda: workspace["settings"])
    monkeypatch.setattr("src.telegram.callbacks.get_settings", lambda: workspace["settings"])
    monkeypatch.setattr("src.telegram.identity.get_settings", lambda: workspace["settings"])
    workspace["settings"].phone_hash_key = "synthetic-journey-lookup"
    monkeypatch.setattr(engine, "generate_completion", completion)
    monkeypatch.setattr("src.decision.generate_completion", completion)
    monkeypatch.setattr(engine, "embed_chunks", fake_embeddings)

    async def ack(self: TelegramClient, callback_id: str) -> None:
        return None

    monkeypatch.setattr(TelegramClient, "acknowledge", ack)

    @asynccontextmanager
    async def no_typing(self, chat_id):
        yield

    monkeypatch.setattr(TelegramClient, "typing", no_typing)
    return workspace


def test_complete_journey_corrections_faq_human_and_staff(journey: dict[str, Any]) -> None:
    tenant = journey["tenants"][0]
    client = journey["client"]
    counter = itertools.count(100)

    async def seed() -> tuple[uuid.UUID, uuid.UUID]:
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=123, token_enc=encrypt_pii("synthetic-token")
            )
            course = Course(tenant_id=tenant, name="Synthetic nursing", application_fee=50000)
            db.add_all([bot, course])
            await db.flush()
            db.add(
                Batch(
                    tenant_id=tenant,
                    course_id=course.id,
                    name="Morning",
                    capacity=20,
                    seats_remaining=20,
                )
            )
            db.add_all(
                [
                    QualificationRule(
                        tenant_id=tenant,
                        course_id=course.id,
                        field="age",
                        operator=RuleOperator.GTE,
                        value=18,
                    ),
                    QualificationRule(
                        tenant_id=tenant,
                        course_id=course.id,
                        field="marks",
                        operator=RuleOperator.GTE,
                        value=50,
                    ),
                ]
            )
            await db.commit()
            return bot.id, course.id

    bot_id, course_id = asyncio.run(seed())

    async def turn(text: str, callback: bool = False) -> tuple[Reply, uuid.UUID]:
        update_id = next(counter)
        message = {
            "message_id": update_id,
            "from": {"id": 42},
            "chat": {"id": 42, "type": "private"},
            "text": text,
        }
        raw: dict[str, Any] = {"update_id": update_id, "message": message}
        if callback:
            message["from"] = {"id": 123}
            raw = {
                "update_id": update_id,
                "callback_query": {
                    "id": str(update_id),
                    "from": {"id": 42},
                    "message": message,
                    "data": text,
                },
            }
        event_id = await service.accept_update(bot_id, raw)
        assert event_id is not None
        assert await service.accept_update(bot_id, raw) == event_id
        await asyncio.gather(service.process_event(event_id), service.process_event(event_id))
        async with journey["sessions"]() as db:
            event = await db.get(ConversationEvent, event_id)
            reply = await db.scalar(
                select(ConversationReply)
                .options(undefer(ConversationReply.payload_enc))
                .where(ConversationReply.event_id == event_id)
            )
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(ConversationReply)
                    .where(ConversationReply.event_id == event_id)
                )
                == 1
            )
            return Reply.model_validate_json(decrypt_pii(reply.payload_enc)), event.lead_id

    reply, lead_id = asyncio.run(turn("/start"))
    assert "course" in reply.text.lower() and not reply.buttons
    reply, _ = asyncio.run(turn("/courses"))
    course_button = next(b for b in reply.buttons if b.text == "Synthetic nursing")
    reply, _ = asyncio.run(turn(course_button.data, True))
    reply, _ = asyncio.run(turn(reply.buttons[0].data, True))
    assert "age" in reply.text
    reply, _ = asyncio.run(turn("20"))
    assert "marks" in reply.text
    reply, _ = asyncio.run(turn("70"))
    assert "full name" in reply.text and not reply.buttons
    reply, _ = asyncio.run(turn("Actually my age is 17"))
    assert "do not meet" in reply.text
    reply, _ = asyncio.run(turn("Actually my age is 21"))
    assert "full name" in reply.text

    signin(client)
    uploaded = send(
        client, [("approved/hostel.txt", b"Hostel accommodation is available on campus.")]
    )
    asyncio.run(process_upload(tenant, uuid.UUID(uploaded["accepted"][0]["id"])))
    reply, _ = asyncio.run(turn("Is hostel accommodation available?"))
    assert reply.text == "Hostel accommodation is available on campus."
    assert reply.source is not None
    assert reply.source.relative_path == "approved/hostel.txt"
    assert reply.source.passage == 1
    # turn() reloads the encrypted reply: evidence survives persistence.
    assert reply.source.document_id is not None
    assert reply.source.chunk_id is not None
    reply, _ = asyncio.run(turn("Can I visit the moon?"))
    assert "could not find" in reply.text
    reply, _ = asyncio.run(turn("/human"))
    assert "request is with the admissions team" in reply.text
    reply, _ = asyncio.run(turn("Actually my age is 10"))
    assert "paused" in reply.text

    listing = client.get("/api/staff/leads")
    assert listing.status_code == 200, listing.text
    detail = client.get(f"/api/staff/leads/{lead_id}")
    assert detail.status_code == 200, detail.text
    assert detail.json()["memory"]["facts"] == {"age": 21, "marks": 70}
    assert detail.json()["memory"]["eligibility"]["outcome"] == "eligible"
    assert any(m["text"] == "Actually my age is 17" for m in detail.json()["messages"])
    requests = client.get("/api/staff/human-requests").json()
    request_id = requests[0]["id"]
    for action in ("acknowledge", "resolve", "resume"):
        response = client.post(
            f"/api/staff/human-requests/{request_id}/{action}", headers={"X-AdmitFlow-Request": "1"}
        )
        assert response.status_code == 200, response.text
    reply, _ = asyncio.run(turn("Actually my age is 10"))
    assert "do not meet" in reply.text
    signin(client, "second")
    assert client.get(f"/api/staff/leads/{lead_id}").status_code == 404
    assert client.get("/api/staff/human-requests").json() == []
    assert (
        client.post(
            f"/api/staff/human-requests/{request_id}/resume", headers={"X-AdmitFlow-Request": "1"}
        ).status_code
        == 404
    )

    async def encrypted() -> None:
        async with journey["sessions"]() as db:
            memory = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            assert '"age"' not in memory.payload_enc
            lead = await db.get(Lead, lead_id)
            assert lead.status == LeadStatus.QUALIFYING and lead.phone_enc is None
            await db.execute(HumanRequest.__table__.delete())

    asyncio.run(encrypted())


def test_uncertain_delivery_is_not_retried(
    journey: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = 0

    async def timeout(self: TelegramClient, chat_id: int, reply: Reply) -> int:
        nonlocal calls
        calls += 1
        raise TelegramAPIError(0, uncertain=True)

    monkeypatch.setattr(TelegramClient, "send", timeout)

    async def exercise() -> None:
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=journey["tenants"][0],
                telegram_bot_id=124,
                token_enc=encrypt_pii("synthetic-token"),
            )
            db.add(bot)
            await db.flush()
            bot_id = bot.id
            await db.commit()
        event_id = await service.accept_update(
            bot_id,
            {
                "update_id": 1,
                "message": {
                    "message_id": 1,
                    "from": {"id": 43},
                    "chat": {"id": 43, "type": "private"},
                    "text": "/start",
                },
            },
        )
        assert event_id is not None
        await service.process_event(event_id)
        async with journey["sessions"]() as db:
            reply_id = await db.scalar(
                select(ConversationReply.id).where(ConversationReply.event_id == event_id)
            )
        assert reply_id is not None
        await service.send_reply(reply_id)
        await service.send_reply(reply_id)
        async with journey["sessions"]() as db:
            reply = await db.get(ConversationReply, reply_id)
            assert reply.status == "uncertain" and reply.attempts == 1
        assert calls == 1

    asyncio.run(exercise())


def test_missing_rules_closed_batches_and_foreign_course_are_not_approved(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.engine.contracts import Event
    from src.engine.journey import qualify, route
    from src.telegram.callbacks import callback_data

    async def exercise() -> None:
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            course = Course(tenant_id=tenant, name="No configured rules")
            foreign = Course(tenant_id=journey["tenants"][1], name="Foreign course")
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=125, token_enc=encrypt_pii("synthetic-token")
            )
            lead = Lead(tenant_id=tenant)
            db.add_all([course, foreign, bot, lead])
            await db.flush()
            batch = Batch(
                tenant_id=tenant,
                course_id=course.id,
                name="Open batch",
                capacity=10,
                seats_remaining=10,
            )
            db.add(batch)
            await db.flush()
            lead.current_course_id, lead.current_batch_id = course.id, batch.id
            memory: dict[str, Any] = {"facts": {}}
            reply = await qualify(db, lead, bot, memory, "", [])
            assert memory["eligibility"]["outcome"] == "needs_staff_review"
            assert "needs to confirm the entry requirements" in reply.text
            signed = callback_data("course", foreign.id.hex, lead.id, bot.id)
            response = await route(
                db,
                lead,
                bot,
                Event(
                    update_id=1, user_id=42, chat_id=42, message_id=1, kind="callback", text=signed
                ),
                memory,
            )
            assert "expired" in response.text and lead.current_course_id == course.id
            batch.seats_remaining = 0
            await db.flush()
            response = await qualify(db, lead, bot, memory, "", [])
            assert "expired" in response.text
            assert lead.status != LeadStatus.ADMISSION_READY
            batch.seats_remaining = 10
            db.add(
                QualificationRule(
                    tenant_id=tenant,
                    course_id=course.id,
                    field="age",
                    operator=RuleOperator.GTE,
                    value=18,
                )
            )
            await db.flush()

            async def decline(*args: Any, **kwargs: Any) -> Any:
                return SimpleNamespace(
                    choices=[
                        SimpleNamespace(
                            message=SimpleNamespace(content='{"facts":[],"declined":true}')
                        )
                    ]
                )

            monkeypatch.setattr("src.decision.generate_completion", decline)
            memory["question"] = "age"
            response = await qualify(db, lead, bot, memory, "I prefer not to answer", [])
            assert "declined" in response.text.lower()
            assert memory["eligibility"]["outcome"] == "needs_information"
            assert lead.status != LeadStatus.ADMISSION_READY
            await db.rollback()

    asyncio.run(exercise())


def test_replies_wait_for_earlier_pending_reply(
    journey: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    sent: list[int] = []

    async def deliver(self: TelegramClient, chat_id: int, reply: Reply) -> int:
        sent.append(chat_id)
        return len(sent)

    monkeypatch.setattr(TelegramClient, "send", deliver)

    async def exercise() -> None:
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=journey["tenants"][0],
                telegram_bot_id=126,
                token_enc=encrypt_pii("synthetic-token"),
            )
            db.add(bot)
            await db.flush()
            bot_id = bot.id
            await db.commit()
        replies = []
        for number in (1, 2):
            event_id = await service.accept_update(
                bot_id,
                {
                    "update_id": number,
                    "message": {
                        "message_id": number,
                        "from": {"id": 44},
                        "chat": {"id": 44, "type": "private"},
                        "text": "/start",
                    },
                },
            )
            assert event_id is not None
            await service.process_event(event_id)
            async with journey["sessions"]() as db:
                replies.append(
                    await db.scalar(
                        select(ConversationReply.id).where(ConversationReply.event_id == event_id)
                    )
                )
        await service.send_reply(replies[1])
        assert sent == []
        await service.send_reply(replies[0])
        await service.send_reply(replies[1])
        assert sent == [44, 44]

    asyncio.run(exercise())


def test_provider_outage_refusal_and_bad_schema_preserve_facts_and_allow_handoff(
    journey: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    from src.engine.llm_factory import AllProvidersFailedError

    async def exercise() -> None:
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=127, token_enc=encrypt_pii("synthetic-token")
            )
            db.add(bot)
            await db.flush()
            bot_id = bot.id
            await db.commit()

        async def turn(number: int, text: str) -> tuple[Reply, uuid.UUID]:
            event_id = await service.accept_update(
                bot_id,
                {
                    "update_id": number,
                    "message": {
                        "message_id": number,
                        "from": {"id": 45},
                        "chat": {"id": 45, "type": "private"},
                        "text": text,
                    },
                },
            )
            assert event_id is not None
            await service.process_event(event_id)
            async with journey["sessions"]() as db:
                event = await db.get(ConversationEvent, event_id)
                assert event.status == "done"
                reply = await db.scalar(
                    select(ConversationReply)
                    .options(undefer(ConversationReply.payload_enc))
                    .where(ConversationReply.event_id == event_id)
                )
                return Reply.model_validate_json(decrypt_pii(reply.payload_enc)), event.lead_id

        _, lead_id = await turn(1, "/start")
        async with journey["sessions"]() as db:
            memory = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            memory.payload_enc = encrypt_pii(json.dumps({"facts": {"age": 21}}))
            await db.commit()

        for number, mode in enumerate(("outage", "refusal", "invalid_schema"), start=2):

            async def unavailable(*args: Any, failure: str = mode, **kwargs: Any) -> Any:
                if failure == "outage":
                    raise AllProvidersFailedError("Synthetic provider outage")
                content = None if failure == "refusal" else '{"intent":"approve_everyone"}'
                return SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
                )

            monkeypatch.setattr("src.engine.journey.generate_completion", unavailable)
            monkeypatch.setattr("src.decision.generate_completion", unavailable)
            reply, _ = await turn(number, "Am I eligible?")
            assert "couldn't complete" in reply.text
            assert "Synthetic provider" not in reply.text
            async with journey["sessions"]() as db:
                memory = await db.scalar(
                    select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
                )
                assert json.loads(decrypt_pii(memory.payload_enc))["facts"] == {"age": 21}
                lead = await db.get(Lead, lead_id)
                assert lead.status != LeadStatus.ADMISSION_READY

        reply, _ = await turn(5, "/human")
        assert "paused" in reply.text
        async with journey["sessions"]() as db:
            request = await db.scalar(select(HumanRequest).where(HumanRequest.lead_id == lead_id))
            assert request.status == "open"

    asyncio.run(exercise())


def test_multilingual_quote_selection_uses_translated_question(
    journey: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    from src.engine.journey import answer_question

    tenant = journey["tenants"][0]
    signin(journey["client"])
    upload = send(
        journey["client"],
        [
            (
                "language/hostel.txt",
                b"Hostel accommodation is available on campus. Synthetic language check.",
            )
        ],
    )
    asyncio.run(process_upload(tenant, uuid.UUID(upload["accepted"][0]["id"])))

    async def translate(text: str) -> str:
        return "Is hostel accommodation available?"

    async def quote(messages: list[dict[str, str]], **kwargs: Any) -> Any:
        assert (
            json.loads(messages[-1]["content"])["question"] == "Is hostel accommodation available?"
        )
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {
                                "supported": True,
                                "passage": 0,
                                "quote": "Hostel accommodation is available on campus.",
                            }
                        )
                    )
                )
            ]
        )

    monkeypatch.setattr("src.knowledge.retrieval.retrieval_query", translate)
    monkeypatch.setattr("src.engine.journey.generate_completion", quote)

    async def exercise() -> None:
        async with journey["sessions"]() as db:
            reply = await answer_question(
                db, Lead(tenant_id=tenant), {"language": "hi"}, "क्या हॉस्टल की सुविधा उपलब्ध है?"
            )
            assert reply.text == "Hostel accommodation is available on campus."
            assert reply.source is not None
            chunk = await db.get(DocumentChunk, reply.source.chunk_id)
            assert chunk is not None and chunk.tenant_id == tenant
            assert chunk.document_id == reply.source.document_id
            assert reply.text in chunk.content
            assert reply.source.passage == chunk.chunk_index + 1
            path = await db.scalar(
                select(KnowledgeUpload.relative_path).where(
                    KnowledgeUpload.tenant_id == tenant,
                    KnowledgeUpload.document_id == chunk.document_id,
                    KnowledgeUpload.status == "ready",
                )
            )
            assert reply.source.relative_path == path

    asyncio.run(exercise())
