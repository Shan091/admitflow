"""Application-layer PII protection: symmetric encryption + deterministic hashing.

Applicant PII (phone numbers, names, emails) is encrypted *before* it reaches
Postgres (SPEC §14, security-and-production.md) using a master data-encryption
key held in settings — not left to the provider's at-rest encryption. Lookups
use a separate *keyed hash* so a lead can be found by phone number without
decrypting every candidate row.

The keys are optional in :class:`~src.core.settings.Settings` so the app still
boots without them (health check, Task-1 tests). The moment a helper here is
called while its key is unset it raises :class:`EncryptionKeyNotConfiguredError`
— the same fail-loud contract as
:class:`~src.db.session.DatabaseNotConfiguredError`.
"""

from __future__ import annotations

import hashlib
import hmac

from cryptography.fernet import Fernet

from src.core.settings import get_settings


class EncryptionKeyNotConfiguredError(RuntimeError):
    """Raised when a PII helper is used but its key is unset in settings."""


def _fernet() -> Fernet:
    key = get_settings().pii_encryption_key
    if not key:
        raise EncryptionKeyNotConfiguredError(
            "PII_ENCRYPTION_KEY is not set — configure it before encrypting PII."
        )
    return Fernet(key.encode())


def encrypt_pii(plaintext: str) -> str:
    """Encrypt a PII string, returning a url-safe base64 Fernet token.

    Fernet is authenticated (AES-128-CBC + HMAC) and embeds a random IV, so the
    same input encrypts to different ciphertext each call and tampering is
    detected on decrypt.
    """
    return _fernet().encrypt(plaintext.encode()).decode()


def encrypt_bytes(plaintext: bytes) -> bytes:
    """Encrypt uploaded source bytes before persistence, without lossy text decoding."""
    return _fernet().encrypt(plaintext)


def decrypt_bytes(ciphertext: bytes) -> bytes:
    """Authenticate and decrypt source bytes for an authorized ingestion task."""
    return _fernet().decrypt(ciphertext)


def decrypt_pii(ciphertext: str) -> str:
    """Decrypt a token produced by :func:`encrypt_pii`.

    Raises :class:`cryptography.fernet.InvalidToken` if the ciphertext was
    tampered with or was encrypted under a different key.
    """
    return _fernet().decrypt(ciphertext.encode()).decode()


def hash_phone(phone: str) -> str:
    """Return a deterministic keyed hash of a phone number for lookup/dedup.

    Keyed HMAC-SHA256 rather than a bare digest, so the stored hashes can't be
    reversed with a precomputed rainbow table of phone numbers. Output is 64 hex
    chars — the width of ``leads.phone_hash`` (``String(64)``).

    ``phone`` must already be **E.164-normalized** by the caller (e.g. the
    webhook ingress in Task 5, where Meta delivers the ``wa_id``). The hash is
    byte-exact: ``"+919876543210"`` and ``"919876543210"`` hash differently, so
    an un-normalized input would defeat the ``(tenant_id, phone_hash)`` dedup
    constraint and create duplicate leads. Normalization is deliberately the
    caller's job, not this primitive's.
    """
    key = get_settings().phone_hash_key
    if not key:
        raise EncryptionKeyNotConfiguredError(
            "PHONE_HASH_KEY is not set — configure it before hashing phone numbers."
        )
    return hmac.new(key.encode(), phone.encode(), hashlib.sha256).hexdigest()
