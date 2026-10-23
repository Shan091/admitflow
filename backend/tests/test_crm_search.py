"""Name lookup retains Indic marks and never stores plaintext search tokens."""

import uuid

import pytest

from src.core import security
from src.core.name_search import name_tokens, normalized_phone, query_tokens
from src.core.settings import Settings


@pytest.fixture(autouse=True)
def keys(monkeypatch):
    monkeypatch.setattr(
        security,
        "get_settings",
        lambda: Settings(_env_file=None, phone_hash_key="synthetic-search-key"),
    )


def test_tenant_scoped_unicode_prefixes():
    tenant = uuid.uuid4()
    tokens = name_tokens(tenant, "  Asha  നായർ कुमार ")
    assert set(query_tokens(tenant, "AS നായർ")) <= set(tokens)
    assert set(query_tokens(tenant, "कु")) <= set(tokens)
    assert not set(query_tokens(uuid.uuid4(), "Asha")) & set(tokens)
    assert "asha" not in str(tokens)
    assert query_tokens(tenant, "ＡＳＨＡ") == query_tokens(tenant, "asha")


@pytest.mark.parametrize("query", ["a", "!?", "अ", "a b"])
def test_too_short_name_query_is_rejected(query):
    with pytest.raises(ValueError):
        query_tokens(uuid.uuid4(), query)


def test_phone_is_explicit_international_and_not_guessed():
    assert normalized_phone("+91 (98765) 43210") == "+919876543210"
    assert normalized_phone("9876543210") is None
    assert normalized_phone("+1 abc 234567890") is None
    assert normalized_phone("+01234567890") is None
