"""Compact callback signatures bind catalog/language choices to one conversation."""

import hashlib
import hmac
import uuid

from src.core.settings import get_settings


def callback_data(kind: str, target: str, lead: uuid.UUID, bot: uuid.UUID) -> str:
    key = get_settings().phone_hash_key
    if not key or ":" in target or ":" in kind:
        raise ValueError("Callback signing is not configured")
    payload = f"{kind}:{target}"
    signature = hmac.new(key.encode(), f"{lead}:{bot}:{payload}".encode(), hashlib.sha256)
    value = f"{payload}:{signature.hexdigest()[:16]}"
    if len(value.encode()) > 64:
        raise ValueError("Callback exceeds transport limit")
    return value


def parse_callback(value: str, lead: uuid.UUID, bot: uuid.UUID) -> tuple[str, str]:
    try:
        kind, target, _ = value.split(":")
        expected = callback_data(kind, target, lead, bot)
        if not hmac.compare_digest(expected, value):
            raise ValueError("Invalid callback")
        return kind, target
    except (ValueError, TypeError):
        raise ValueError("Invalid or expired choice") from None
