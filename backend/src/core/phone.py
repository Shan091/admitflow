"""E.164 phone-number normalization.

Carry-over prerequisite #3: un-normalized input (``+91 98765…`` vs
``919876…``) defeats the ``(tenant_id, phone_hash)`` unique constraint and
creates duplicate leads. This module is the single normalization point —
call it before ``hash_phone()`` or any phone-keyed lookup.

The normalizer is intentionally *not* a full ITU-T parser: Meta delivers
``wa_id`` as bare digits (no ``+``), Indian numbers as 12 digits, and US
numbers as 11. We strip cosmetic characters, prepend ``+`` if absent, and
validate length against the E.164 spec (7–15 digits after the ``+``).
"""

from __future__ import annotations

import re

# E.164: 1–3 digit country code + subscriber = 7–15 digits total after '+'.
_MIN_DIGITS = 7
_MAX_DIGITS = 15


class InvalidPhoneError(ValueError):
    """Raised when a phone string cannot be normalized to E.164."""


def normalize_e164(raw: str) -> str:
    """Normalize *raw* into canonical E.164 (``+<digits>``).

    Strips whitespace, dashes, parentheses, and dots, then ensures a ``+``
    prefix and validates length.

    Raises:
        InvalidPhoneError: If the result is too short, too long, or contains
            non-digit characters after stripping.
    """
    # Strip cosmetic characters.
    cleaned = re.sub(r"[\s\-\(\)\.]", "", raw)

    # Remove leading '+' for uniform digit-only processing.
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    # Reject anything that isn't pure digits at this point.
    if not cleaned or not cleaned.isdigit():
        raise InvalidPhoneError(f"Phone number contains non-digit characters: {raw!r}")

    if len(cleaned) < _MIN_DIGITS:
        raise InvalidPhoneError(
            f"Phone number too short ({len(cleaned)} digits, min {_MIN_DIGITS}): {raw!r}"
        )

    if len(cleaned) > _MAX_DIGITS:
        raise InvalidPhoneError(
            f"Phone number too long ({len(cleaned)} digits, max {_MAX_DIGITS}): {raw!r}"
        )

    return f"+{cleaned}"
