"""Strict private-chat normalization and token-safe Telegram HTTP transport."""

import asyncio
import logging
import re
from typing import Any

import httpx2 as httpx
from pydantic import ValidationError

from src.engine.contracts import Event, Reply


class TelegramAPIError(RuntimeError):
    def __init__(self, code: int, *, uncertain: bool = False, retry_after: int = 0) -> None:
        super().__init__(f"Telegram operation failed ({code})")
        self.code, self.uncertain, self.retry_after = code, uncertain, retry_after


class TokenSafeFilter(logging.Filter):
    """TaskIQ changes log levels; redact before either HTTP client or root handlers emit."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = re.sub(
            r"(https://api\.telegram\.org/bot)[^/\s]+", r"\1[redacted]", record.getMessage()
        )
        record.args = ()
        return True


def protect_logs() -> None:
    for logger in [logging.getLogger(name) for name in ("httpx2", "httpx", "httpcore")]:
        if not any(isinstance(item, TokenSafeFilter) for item in logger.filters):
            logger.addFilter(TokenSafeFilter())
        logger.setLevel(logging.WARNING)
    for handler in logging.getLogger().handlers:
        if not any(isinstance(item, TokenSafeFilter) for item in handler.filters):
            handler.addFilter(TokenSafeFilter())


def normalize_update(raw: dict[str, Any], bot_id: int) -> Event | None:
    try:
        callback = raw.get("callback_query")
        message = callback.get("message", {}) if callback else raw.get("message", {})
        actor = callback.get("from", {}) if callback else message.get("from", {})
        chat = message.get("chat", {})
        if chat.get("type") != "private" or actor.get("id") != chat.get("id"):
            return None
        if actor.get("is_bot") or (callback and message.get("from", {}).get("id") != bot_id):
            return None
        value = callback.get("data", "") if callback else message.get("text", "")
        if not isinstance(value, str):
            return None
        return Event(
            update_id=raw["update_id"],
            user_id=actor["id"],
            chat_id=chat["id"],
            message_id=message["message_id"],
            kind="callback" if callback else ("text" if message.get("text") else "unsupported"),
            text=value,
            callback_id=callback.get("id") if callback else None,
        )
    except (KeyError, TypeError, AttributeError, ValidationError):
        return None


class TelegramClient:
    def __init__(self, token: str) -> None:
        self._token = token

    async def call(self, method: str, payload: dict[str, Any]) -> Any:
        protect_logs()
        safe_retry = method in {"getMe", "getWebhookInfo", "getUpdates", "answerCallbackQuery"}
        for attempt in range(3):
            try:
                return await self._call_once(method, payload)
            except TelegramAPIError as error:
                if not safe_retry or attempt == 2 or (error.code != 0 and error.code < 500):
                    raise
                await asyncio.sleep(attempt + 1)
        raise TelegramAPIError(0, uncertain=True)

    async def _call_once(self, method: str, payload: dict[str, Any]) -> Any:
        try:
            async with httpx.AsyncClient(timeout=40, follow_redirects=False) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{self._token}/{method}", json=payload
                )
                data = response.json()
        except Exception:
            raise TelegramAPIError(0, uncertain=True) from None
        if not data.get("ok"):
            code = int(data.get("error_code", response.status_code))
            raise TelegramAPIError(
                code,
                uncertain=code >= 500,
                retry_after=int(data.get("parameters", {}).get("retry_after", 0)),
            )
        return data["result"]

    async def send(self, chat_id: int, reply: Reply) -> int:
        payload: dict[str, Any] = {"chat_id": chat_id, "text": reply.text, "protect_content": True}
        if reply.buttons:
            payload["reply_markup"] = {
                "inline_keyboard": [
                    [{"text": button.text, "callback_data": button.data}]
                    for button in reply.buttons
                ]
            }
        result = await self.call("sendMessage", payload)
        return int(result["message_id"])

    async def acknowledge(self, callback_id: str) -> None:
        await self.call("answerCallbackQuery", {"callback_query_id": callback_id})
