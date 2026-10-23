"""Staff passwords must be salted, bounded and verified in constant time."""

import pytest

from src.staff.auth import hash_password, verify_password


def test_passwords_are_salted_and_invalid_passwords_fail() -> None:
    first = hash_password("correct synthetic password")
    assert first != hash_password("correct synthetic password")
    assert "correct synthetic password" not in first
    assert verify_password("correct synthetic password", first)
    assert not verify_password("incorrect synthetic password", first)
    assert not verify_password("anything", "broken-storage-format")


@pytest.mark.parametrize("password", ["short", "x" * 1025])
def test_invalid_password_lengths_are_rejected(password: str) -> None:
    with pytest.raises(ValueError):
        hash_password(password)
