"""Telegram identities must be independent of phone numbers and tenant-bound."""

import uuid

import pytest
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint

from src.db.models import Institution, Lead, TelegramBot, TelegramIdentity
from src.telegram.identity import hash_telegram_identifier


def test_telegram_students_do_not_require_fabricated_phone_numbers() -> None:
    assert Institution.__table__.c.whatsapp_phone_number_id.nullable
    assert Lead.__table__.c.phone_hash.nullable
    assert Lead.__table__.c.phone_enc.nullable


def test_bot_and_student_links_enforce_the_same_tenant() -> None:
    foreign_keys = {
        (tuple(c.columns.keys()), tuple(e.target_fullname for e in c.elements))
        for c in TelegramIdentity.__table__.constraints
        if isinstance(c, ForeignKeyConstraint)
    }
    assert (("tenant_id", "bot_id"), ("telegram_bots.tenant_id", "telegram_bots.id")) in (
        foreign_keys
    )
    assert (("tenant_id", "lead_id"), ("leads.tenant_id", "leads.id")) in foreign_keys


def test_identity_lookup_and_chat_routing_are_unique_per_tenant_and_bot() -> None:
    unique = {
        tuple(c.columns.keys())
        for c in TelegramIdentity.__table__.constraints
        if isinstance(c, UniqueConstraint)
    }
    assert ("tenant_id", "bot_id", "user_hash") in unique
    assert ("tenant_id", "bot_id", "chat_hash") in unique
    assert not TelegramBot.__table__.c.token_enc.nullable


def test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.core.settings import Settings

    monkeypatch.setattr(
        "src.telegram.identity.get_settings",
        lambda: Settings(_env_file=None, phone_hash_key="synthetic-identity-pepper"),
    )
    tenant = uuid.uuid4()
    digest = hash_telegram_identifier(tenant, 42, "user", 123456789)
    assert digest == hash_telegram_identifier(tenant, 42, "user", 123456789)
    assert len(digest) == 64
    assert "123456789" not in digest
    assert digest != hash_telegram_identifier(uuid.uuid4(), 42, "user", 123456789)
    assert digest != hash_telegram_identifier(tenant, 43, "user", 123456789)
    assert digest != hash_telegram_identifier(tenant, 42, "chat", 123456789)


@pytest.mark.parametrize("value", [0, -1, True, 2**63])
def test_private_chat_identity_rejects_invalid_identifiers(value: int) -> None:
    with pytest.raises(ValueError, match="positive 64-bit integer"):
        hash_telegram_identifier(uuid.uuid4(), 42, "user", value)


def test_lookup_requires_a_configured_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.core.security import EncryptionKeyNotConfiguredError
    from src.core.settings import Settings

    monkeypatch.setattr(
        "src.telegram.identity.get_settings",
        lambda: Settings(_env_file=None, phone_hash_key=None),
    )
    with pytest.raises(EncryptionKeyNotConfiguredError):
        hash_telegram_identifier(uuid.uuid4(), 42, "user", 123456789)
