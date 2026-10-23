"""Private Telegram identity lookup without storing raw identifiers in indexes."""

import hashlib
import hmac
import uuid
from typing import Literal

from src.core.security import EncryptionKeyNotConfiguredError
from src.core.settings import get_settings


def hash_telegram_identifier(
    tenant_id: uuid.UUID,
    bot_id: int,
    kind: Literal["user", "chat"],
    identifier: int,
) -> str:
    """Hash an identifier in its tenant/bot/type domain using the lookup secret.

    This milestone supports private chats only. Group/channel IDs are rejected.
    Sharing the existing lookup key is safe through explicit domain separation;
    neither usernames nor fabricated E.164 phone numbers are used for identity.
    """
    for value in (bot_id, identifier):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 < value < 2**63:
            raise ValueError("Telegram private identity must be a positive 64-bit integer")
    if kind not in {"user", "chat"}:
        raise ValueError("Unsupported Telegram identifier kind")
    secret = get_settings().phone_hash_key
    if not secret:
        raise EncryptionKeyNotConfiguredError("PHONE_HASH_KEY is required for identity lookup")
    message = f"telegram:{tenant_id.hex}:{bot_id}:{kind}:{identifier}"
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
