"""Tests for E.164 phone normalization (carry-over prerequisite #3).

The normalizer must collapse all cosmetic variants of a phone number into
a single canonical E.164 form so ``hash_phone`` produces deterministic dedup.
"""

from __future__ import annotations

import pytest

from src.core.phone import InvalidPhoneError, normalize_e164


class TestNormalizeE164:
    """normalize_e164 → canonical E.164 string."""

    # -- happy path: cosmetic variants all collapse to the same output --------

    def test_already_e164(self) -> None:
        assert normalize_e164("+919876543210") == "+919876543210"

    def test_strips_spaces(self) -> None:
        assert normalize_e164("+91 9876 543210") == "+919876543210"

    def test_strips_dashes(self) -> None:
        assert normalize_e164("+91-9876-543210") == "+919876543210"

    def test_strips_parens(self) -> None:
        assert normalize_e164("+(91) 9876543210") == "+919876543210"

    def test_no_plus_prefix_passthrough(self) -> None:
        """Meta's ``wa_id`` format: digits-only, no ``+``."""
        assert normalize_e164("919876543210") == "+919876543210"

    def test_us_number(self) -> None:
        assert normalize_e164("+14155552671") == "+14155552671"

    def test_us_number_no_plus(self) -> None:
        assert normalize_e164("14155552671") == "+14155552671"

    # -- edge cases -----------------------------------------------------------

    def test_strips_mixed_whitespace(self) -> None:
        assert normalize_e164("  +91\t9876\n543210  ") == "+919876543210"

    # -- invalid inputs -------------------------------------------------------

    def test_too_short_raises(self) -> None:
        with pytest.raises(InvalidPhoneError):
            normalize_e164("+1234")

    def test_too_long_raises(self) -> None:
        with pytest.raises(InvalidPhoneError):
            normalize_e164("+1234567890123456")  # 16 digits

    def test_empty_string_raises(self) -> None:
        with pytest.raises(InvalidPhoneError):
            normalize_e164("")

    def test_non_digit_body_raises(self) -> None:
        with pytest.raises(InvalidPhoneError):
            normalize_e164("+91abc1234567")

    def test_letters_only_raises(self) -> None:
        with pytest.raises(InvalidPhoneError):
            normalize_e164("hello")
