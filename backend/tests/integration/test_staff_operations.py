"""Staff takeover pauses bot replies; explicit sends are scoped, durable and idempotent."""

import asyncio
import json
import uuid
from types import SimpleNamespace
from typing import Any

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import undefer

from src.core.security import encrypt_pii
from src.db.models import ConversationEvent, ConversationReply, Lead, OutboundMessage, TelegramBot
from src.telegram import outbound, service
from src.telegram.adapter import TelegramClient
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


async def prepare(journey: dict[str, Any], bot_number: int) -> tuple[uuid.UUID, uuid.UUID]:
    async with journey["sessions"]() as db:
        bot = TelegramBot(
            tenant_id=journey["tenants"][0],
            telegram_bot_id=bot_number,
            token_enc=encrypt_pii("synthetic-token"),
        )
        db.add(bot)
        await db.commit()
        bot_id = bot.id
    event_id = await inbound(bot_id, 1, "/start")
    async with journey["sessions"]() as db:
        event = await db.get(ConversationEvent, event_id)
        return bot_id, event.lead_id


async def inbound(bot_id: uuid.UUID, update_id: int, text: str) -> uuid.UUID:
    event_id = await service.accept_update(
        bot_id,
        {
            "update_id": update_id,
            "message": {
                "message_id": update_id,
                "from": {"id": 83},
                "chat": {"id": 83, "type": "private"},
                "text": text,
            },
        },
    )
    assert event_id
    await service.process_event(event_id)
    return event_id


def test_takeover_manual_delivery_and_resume_preserve_context(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(outbound, "get_sessionmaker", lambda: journey["sessions"])
    sends = []

    async def deliver(self, chat_id, reply):
        sends.append(reply.text)
        return 737

    monkeypatch.setattr(TelegramClient, "send", deliver)
    bot_id, lead_id = asyncio.run(prepare(journey, 8081))
    client = journey["client"]
    base = f"/api/staff/leads/{lead_id}"
    assert client.post(base + "/takeover", headers=HEADERS).status_code == 401
    signin(client, "second")
    assert client.post(base + "/takeover", headers=HEADERS).status_code == 404
    signin(client, email="agent@example.test")
    assert client.post(base + "/takeover").status_code == 403
    body = {"request_id": str(uuid.uuid4()), "text": "I can help with your course question."}
    assert client.post(base + "/messages", json=body, headers=HEADERS).status_code == 409
    assert client.post(base + "/takeover", headers=HEADERS).status_code == 200
    assert client.post(base + "/takeover", headers=HEADERS).status_code == 200
    event_id = asyncio.run(inbound(bot_id, 2, "Please help with the campus"))

    async def paused():
        async with journey["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            assert lead.copilot_mode
            assert (
                await db.scalar(
                    select(ConversationReply.id).where(ConversationReply.event_id == event_id)
                )
                is None
            )
            assert (await db.get(ConversationEvent, event_id)).status == "done"

    asyncio.run(paused())
    first = client.post(base + "/messages", json=body, headers=HEADERS)
    assert first.status_code == 200, first.text
    assert (
        client.post(base + "/messages", json=body, headers=HEADERS).json()["id"]
        == first.json()["id"]
    )
    assert (
        client.post(
            base + "/messages", json={**body, "text": "Different"}, headers=HEADERS
        ).status_code
        == 409
    )
    assert (
        client.post(
            base + "/messages", json={**body, "text": "bad\x00text"}, headers=HEADERS
        ).status_code
        == 422
    )
    assert client.post(base + "/resume", headers=HEADERS).status_code == 409
    asyncio.run(outbound.send_outbound(uuid.UUID(first.json()["id"])))
    assert sends == [body["text"]]
    assert client.post(base + "/resume", headers=HEADERS).status_code == 200
    assert client.get(base).json()["copilot_mode"] is False
    last_event = asyncio.run(inbound(bot_id, 3, "/start"))

    async def resumed():
        from src.engine.journey import recent_history

        async with journey["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            history = await recent_history(db, lead)
            assert any(row["content"] == body["text"] for row in history)
            assert await db.scalar(
                select(ConversationReply.id).where(ConversationReply.event_id == last_event)
            )
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(OutboundMessage)
                    .where(OutboundMessage.lead_id == lead_id)
                )
                == 1
            )

    asyncio.run(resumed())


def test_copilot_requires_review_rejects_stale_and_deduplicates_approval(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.staff import copilot

    calls = 0

    async def draft(messages, **kwargs):
        nonlocal calls
        calls += 1
        assert kwargs["response_format"].__name__ == "DraftContent"
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {"text": "I can help you explore the available courses."}
                        )
                    )
                )
            ]
        )

    monkeypatch.setattr(copilot, "generate_completion", draft)
    bot_id, lead_id = asyncio.run(prepare(journey, 8082))
    client = journey["client"]
    signin(client)
    base = f"/api/staff/leads/{lead_id}"
    nonce = {"request_id": str(uuid.uuid4())}
    assert client.post(base + "/draft", json=nonce, headers=HEADERS).status_code == 409
    client.post(base + "/takeover", headers=HEADERS)
    result = client.post(base + "/draft", json=nonce, headers=HEADERS)
    assert result.status_code == 200, result.text
    first = result.json()
    assert client.post(base + "/draft", json=nonce, headers=HEADERS).json()["id"] == first["id"]
    assert calls == 1

    async def count():
        async with journey["sessions"]() as db:
            return await db.scalar(
                select(func.count())
                .select_from(OutboundMessage)
                .where(OutboundMessage.lead_id == lead_id)
            )

    assert asyncio.run(count()) == 0
    path = base + "/draft/" + first["id"]
    assert client.post(path, json={"decision": "approve"}, headers=HEADERS).status_code == 422
    asyncio.run(inbound(bot_id, 2, "A newer question about the library"))
    assert (
        client.post(
            path, json={"decision": "approve", "reviewed": True}, headers=HEADERS
        ).status_code
        == 409
    )
    second = client.post(
        base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS
    ).json()
    path = base + "/draft/" + second["id"]
    assert client.post(path, json={"decision": "ignore"}, headers=HEADERS).status_code == 200
    assert (
        client.post(
            path, json={"decision": "approve", "reviewed": True}, headers=HEADERS
        ).status_code
        == 409
    )
    third = client.post(
        base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS
    ).json()
    path = base + "/draft/" + third["id"]
    body = {"decision": "approve", "reviewed": True, "text": "Here is my reviewed staff reply."}
    accepted = client.post(path, json=body, headers=HEADERS)
    assert accepted.status_code == 200, accepted.text
    assert client.post(path, json=body, headers=HEADERS).json()["id"] == accepted.json()["id"]
    assert (
        client.post(
            path, json={**body, "text": "Changed after sending"}, headers=HEADERS
        ).status_code
        == 409
    )
    assert asyncio.run(count()) == 1
    signin(client, "second")
    assert client.post(path, json=body, headers=HEADERS).status_code == 404


def test_draft_generation_cannot_overwrite_a_concurrent_staff_revision(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.core.security import decrypt_pii
    from src.db.models import ConversationMemory
    from src.staff import copilot

    bot_id, lead_id = asyncio.run(prepare(journey, 8083))

    async def change_then_reply(messages, **kwargs):
        async with journey["sessions"]() as db:
            await db.scalar(select(Lead).where(Lead.id == lead_id).with_for_update())
            saved = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            memory = json.loads(decrypt_pii(saved.payload_enc))
            memory["staff_revision"] = 10
            saved.payload_enc = encrypt_pii(json.dumps(memory))
            await db.commit()
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {"text": "This draft must not replace a newer staff action."}
                        )
                    )
                )
            ]
        )

    monkeypatch.setattr(copilot, "generate_completion", change_then_reply)
    client = journey["client"]
    signin(client)
    base = f"/api/staff/leads/{lead_id}"
    client.post(base + "/takeover", headers=HEADERS)
    result = client.post(base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS)
    assert result.status_code == 409
    assert client.get(base).json()["memory"]["staff_revision"] == 10


def test_clear_escalation_records_request_outside_hours_without_a_model(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.core.security import decrypt_pii
    from src.db.models import HumanRequest, Institution
    from src.engine import journey as engine

    bot_id, lead_id = asyncio.run(prepare(journey, 8084))

    async def unavailable(*args, **kwargs):
        raise AssertionError("Clear support signals must not depend on a model")

    monkeypatch.setattr(engine, "generate_completion", unavailable)

    async def exercise():
        async with journey["sessions"]() as db:
            institution = await db.get(Institution, journey["tenants"][0])
            institution.business_hours = {}
            await db.commit()
        event_id = await inbound(bot_id, 2, "I am really frustrated with this")
        await inbound(bot_id, 3, "/human")
        async with journey["sessions"]() as db:
            reply = await db.scalar(
                select(ConversationReply)
                .where(ConversationReply.event_id == event_id)
                .options(undefer(ConversationReply.payload_enc))
            )
            text = json.loads(decrypt_pii(reply.payload_enc))["text"]
            assert "outside" in text and "not promised" in text
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(HumanRequest)
                    .where(HumanRequest.lead_id == lead_id)
                )
                == 1
            )
            assert not (await db.get(Lead, lead_id)).copilot_mode

    asyncio.run(exercise())


def test_copilot_provider_failure_never_queues_a_message(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.staff import copilot

    async def unavailable(*args, **kwargs):
        raise ConnectionError("synthetic provider failure")

    monkeypatch.setattr(copilot, "generate_completion", unavailable)
    _, lead_id = asyncio.run(prepare(journey, 8085))
    client = journey["client"]
    signin(client)
    base = f"/api/staff/leads/{lead_id}"
    client.post(base + "/takeover", headers=HEADERS)
    result = client.post(base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS)
    assert result.status_code == 503 and "synthetic provider failure" not in result.text
    assert client.get(base).json()["memory"]["staff_draft"]["status"] == "failed"

    async def count():
        async with journey["sessions"]() as db:
            return await db.scalar(
                select(func.count())
                .select_from(OutboundMessage)
                .where(OutboundMessage.lead_id == lead_id)
            )

    assert asyncio.run(count()) == 0


def test_expired_draft_and_disabled_channel_cannot_queue_staff_replies(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.core.security import decrypt_pii
    from src.db.models import ConversationMemory
    from src.staff import copilot

    bot_id, lead_id = asyncio.run(prepare(journey, 8086))

    async def generated(messages, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps({"text": "A reply requiring current staff review."})
                    )
                )
            ]
        )

    monkeypatch.setattr(copilot, "generate_completion", generated)
    client = journey["client"]
    signin(client)
    base = f"/api/staff/leads/{lead_id}"
    client.post(base + "/takeover", headers=HEADERS)
    draft = client.post(
        base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS
    ).json()

    async def expire():
        async with journey["sessions"]() as db:
            saved = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            memory = json.loads(decrypt_pii(saved.payload_enc))
            memory["staff_draft"]["expires_at"] = 0
            saved.payload_enc = encrypt_pii(json.dumps(memory))
            await db.commit()

    asyncio.run(expire())
    assert client.get(base).json()["draft_stale"]
    path = base + "/draft/" + draft["id"]
    assert (
        client.post(
            path, json={"decision": "approve", "reviewed": True}, headers=HEADERS
        ).status_code
        == 409
    )
    assert client.post(path, json={"decision": "ignore"}, headers=HEADERS).status_code == 200
    assert (
        client.post(base + "/draft", json={"request_id": draft["id"]}, headers=HEADERS).status_code
        == 409
    )

    async def disable():
        async with journey["sessions"]() as db:
            bot = await db.get(TelegramBot, bot_id)
            bot.is_active = False
            await db.commit()

    asyncio.run(disable())
    result = client.post(
        base + "/messages",
        json={"request_id": str(uuid.uuid4()), "text": "Cannot deliver"},
        headers=HEADERS,
    )
    assert result.status_code == 409


@pytest.mark.parametrize("provider_fails", [True, False])
def test_provider_completion_does_not_overwrite_a_resumed_draft(
    journey: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    provider_fails: bool,
) -> None:
    from src.core.security import decrypt_pii
    from src.db.models import ConversationMemory, HumanRequest
    from src.staff import copilot

    _, lead_id = asyncio.run(prepare(journey, 8087 if provider_fails else 8088))

    async def cancel_then_fail(messages, **kwargs):
        async with journey["sessions"]() as db:
            lead = await db.scalar(select(Lead).where(Lead.id == lead_id).with_for_update())
            lead.copilot_mode = False
            request = await db.scalar(select(HumanRequest).where(HumanRequest.lead_id == lead_id))
            request.status = "resumed"
            saved = await db.scalar(
                select(ConversationMemory).where(ConversationMemory.lead_id == lead_id)
            )
            memory = json.loads(decrypt_pii(saved.payload_enc))
            memory["staff_draft"]["status"] = "ignored"
            saved.payload_enc = encrypt_pii(json.dumps(memory))
            await db.commit()
        if provider_fails:
            raise ConnectionError("Synthetic cancelled provider request")
        # Staff may start a new takeover before the old provider request completes.
        async with journey["sessions"]() as db:
            lead = await db.get(Lead, lead_id)
            lead.copilot_mode = True
            request = await db.scalar(select(HumanRequest).where(HumanRequest.lead_id == lead_id))
            request.status = "acknowledged"
            await db.commit()
        return SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content=json.dumps({"text": "Old draft"})))
            ]
        )

    monkeypatch.setattr(copilot, "generate_completion", cancel_then_fail)
    client = journey["client"]
    signin(client)
    base = f"/api/staff/leads/{lead_id}"
    client.post(base + "/takeover", headers=HEADERS)
    assert client.post(
        base + "/draft", json={"request_id": str(uuid.uuid4())}, headers=HEADERS
    ).status_code == (503 if provider_fails else 409)
    assert client.get(base).json()["memory"]["staff_draft"]["status"] == "ignored"
