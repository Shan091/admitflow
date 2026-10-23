"""Unit tests for application-layer PII protection (encrypt/decrypt + phone hash)."""

from __future__ import annotations

import pytest
from cryptography.fernet import Fernet, InvalidToken

from src.core import security
from src.core.settings import Settings


@pytest.fixture
def configured_keys(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Point ``security.get_settings`` at settings with the crypto keys set."""
    settings = Settings(
        pii_encryption_key=Fernet.generate_key().decode(),
        phone_hash_key="test-phone-hash-pepper",
    )
    monkeypatch.setattr(security, "get_settings", lambda: settings)
    return settings


@pytest.fixture
def unset_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """Point ``security.get_settings`` at settings with no crypto keys."""
    settings = Settings(pii_encryption_key=None, phone_hash_key=None)
    monkeypatch.setattr(security, "get_settings", lambda: settings)


def test_encrypt_decrypt_roundtrip(configured_keys: Settings) -> None:
    plaintext = "+919876543210"
    assert security.decrypt_pii(security.encrypt_pii(plaintext)) == plaintext


def test_roundtrip_preserves_unicode_names(configured_keys: Settings) -> None:
    # A Malayalam name must survive the roundtrip (the product is multilingual).
    name = "അനു മോൾ"
    assert security.decrypt_pii(security.encrypt_pii(name)) == name


def test_ciphertext_differs_from_plaintext(configured_keys: Settings) -> None:
    plaintext = "Priya Nair"
    assert security.encrypt_pii(plaintext) != plaintext


def test_encryption_is_non_deterministic(configured_keys: Settings) -> None:
    # Fernet embeds a random IV, so the same input encrypts differently each call.
    plaintext = "+919876543210"
    assert security.encrypt_pii(plaintext) != security.encrypt_pii(plaintext)


def test_decrypt_rejects_tampered_ciphertext(configured_keys: Settings) -> None:
    token = security.encrypt_pii("+919876543210")
    tampered = ("A" if token[0] != "A" else "B") + token[1:]
    with pytest.raises(InvalidToken):
        security.decrypt_pii(tampered)


def test_decrypt_rejects_token_from_a_different_key(monkeypatch: pytest.MonkeyPatch) -> None:
    # Key isolation: a token encrypted under key A must not decrypt under key B.
    key_a = Settings(pii_encryption_key=Fernet.generate_key().decode())
    monkeypatch.setattr(security, "get_settings", lambda: key_a)
    token = security.encrypt_pii("+919876543210")

    key_b = Settings(pii_encryption_key=Fernet.generate_key().decode())
    monkeypatch.setattr(security, "get_settings", lambda: key_b)
    with pytest.raises(InvalidToken):
        security.decrypt_pii(token)


def test_empty_string_roundtrips(configured_keys: Settings) -> None:
    # Optional PII (e.g. a missing name) must survive as an empty string.
    assert security.decrypt_pii(security.encrypt_pii("")) == ""


def test_encrypt_without_key_raises(unset_keys: None) -> None:
    with pytest.raises(security.EncryptionKeyNotConfiguredError):
        security.encrypt_pii("+919876543210")


def test_decrypt_without_key_raises(unset_keys: None) -> None:
    with pytest.raises(security.EncryptionKeyNotConfiguredError):
        security.decrypt_pii("gAAAAAB-not-reached")


def test_hash_phone_is_deterministic(configured_keys: Settings) -> None:
    phone = "+919876543210"
    assert security.hash_phone(phone) == security.hash_phone(phone)


def test_hash_phone_differs_per_number(configured_keys: Settings) -> None:
    assert security.hash_phone("+919876543210") != security.hash_phone("+919876500000")


def test_hash_phone_differs_per_pepper_key(monkeypatch: pytest.MonkeyPatch) -> None:
    # The pepper is actually mixed in: the same number under two keys differs.
    phone = "+919876543210"
    monkeypatch.setattr(security, "get_settings", lambda: Settings(phone_hash_key="pepper-a"))
    digest_a = security.hash_phone(phone)
    monkeypatch.setattr(security, "get_settings", lambda: Settings(phone_hash_key="pepper-b"))
    digest_b = security.hash_phone(phone)
    assert digest_a != digest_b


def test_hash_phone_is_not_plaintext_and_fits_column(configured_keys: Settings) -> None:
    phone = "+919876543210"
    digest = security.hash_phone(phone)
    assert phone not in digest
    assert len(digest) == 64  # hex SHA-256 == width of leads.phone_hash (String(64))


def test_hash_phone_without_key_raises(unset_keys: None) -> None:
    with pytest.raises(security.EncryptionKeyNotConfiguredError):
        security.hash_phone("+919876543210")
