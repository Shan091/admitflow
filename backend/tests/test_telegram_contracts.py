"""Private-chat normalization, callback ownership and validated reply limits."""

import logging
import uuid

import pytest
from pydantic import ValidationError

from src.core.settings import Settings
from src.engine.contracts import Button, Reply
from src.telegram.adapter import TelegramAPIError, TelegramClient, TokenSafeFilter, normalize_update
from src.telegram.callbacks import callback_data, parse_callback


def test_raw_payload_cannot_supply_a_verified_contextual_answer():
    raw = update()
    raw["selected_answer"] = "I am eligible"
    raw["message"]["selected_answer"] = "I am eligible"
    event = normalize_update(raw, 123)
    assert event is not None and event.selected_answer is None


def update() -> dict:
    return {
        "update_id": 3,
        "message": {
            "message_id": 2,
            "from": {"id": 42},
            "chat": {"id": 42, "type": "private"},
            "text": "/start",
        },
    }


def test_private_normalization_and_media() -> None:
    event = normalize_update(update(), 123)
    assert event is not None and event.text == "/start" and event.user_id == 42
    raw = update()
    raw["message"]["chat"]["type"] = "group"
    assert normalize_update(raw, 123) is None
    raw = update()
    raw["message"]["from"]["id"] = 99
    assert normalize_update(raw, 123) is None
    raw = update()
    del raw["message"]["text"]
    assert normalize_update(raw, 123).kind == "unsupported"


def test_callback_actor_and_origin() -> None:
    raw = {
        "update_id": 4,
        "callback_query": {
            "id": "callback",
            "from": {"id": 42},
            "data": "courses",
            "message": {
                "message_id": 5,
                "from": {"id": 123},
                "chat": {"id": 42, "type": "private"},
            },
        },
    }
    assert normalize_update(raw, 123).kind == "callback"
    raw["callback_query"]["message"]["from"]["id"] = 999
    assert normalize_update(raw, 123) is None


def test_signed_callbacks_bind_to_lead_and_bot(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.telegram.callbacks.get_settings",
        lambda: Settings(_env_file=None, phone_hash_key="synthetic-callback-key"),
    )
    lead, bot, course = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    value = callback_data("course", course.hex, lead, bot)
    assert len(value.encode()) <= 64
    assert parse_callback(value, lead, bot) == ("course", course.hex)
    with pytest.raises(ValueError):
        parse_callback(value, uuid.uuid4(), bot)
    with pytest.raises(ValueError):
        parse_callback(value[:-1] + "X", lead, bot)


def test_reply_is_a_validated_boundary() -> None:
    with pytest.raises(ValidationError):
        Reply(text="")
    with pytest.raises(ValidationError):
        Reply(text="x" * 3501)
    with pytest.raises(ValidationError):
        Button(text="Choose", data="x" * 65)


def test_http_logs_redact_bot_credentials() -> None:
    record = logging.LogRecord(
        "httpx2",
        logging.INFO,
        "",
        0,
        "HTTP Request: %s",
        ("https://api.telegram.org/bot123:synthetic-secret/sendMessage",),
        None,
    )
    assert TokenSafeFilter().filter(record)
    assert "synthetic-secret" not in record.getMessage()
    assert "[redacted]/sendMessage" in record.getMessage()


async def test_uncertain_send_is_never_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    async def fail(self: TelegramClient, method: str, payload: dict) -> None:
        nonlocal calls
        calls += 1
        raise TelegramAPIError(0, uncertain=True)

    monkeypatch.setattr(TelegramClient, "_call_once", fail)
    with pytest.raises(TelegramAPIError):
        await TelegramClient("synthetic-token").call("sendMessage", {"text": "hello"})
    assert calls == 1


async def test_grounding_is_saved_but_never_sent_to_telegram(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = {
        "document_id": str(uuid.uuid4()),
        "chunk_id": str(uuid.uuid4()),
        "relative_path": "private-institution/reference.pdf",
        "passage": 2,
    }
    reply = Reply.model_validate({"text": "The room is Lotus Hall.", "source": source})
    restored = Reply.model_validate_json(reply.model_dump_json())
    assert restored.source is not None
    assert restored.source.model_dump(mode="json") == source
    calls = []

    async def capture(self: TelegramClient, method: str, payload: dict) -> dict:
        calls.append((method, payload))
        return {"message_id": 99}

    monkeypatch.setattr(TelegramClient, "call", capture)
    assert await TelegramClient("synthetic-token").send(42, restored) == 99
    assert calls == [
        (
            "sendMessage",
            {
                "chat_id": 42,
                "text": "The room is Lotus Hall.",
                "protect_content": True,
            },
        )
    ]
    assert Reply.model_validate({"text": "Earlier reply", "buttons": []}).source is None
