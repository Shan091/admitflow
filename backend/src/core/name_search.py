"""Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only."""

import re
import unicodedata
import uuid

from src.core.security import hash_phone


def words(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    # Preserve combining marks in Malayalam/Hindi instead of ASCII/\w splitting.
    normalized = "".join(c if unicodedata.category(c)[0] in "LMN" else " " for c in normalized)
    return normalized.split()


def token(tenant_id: uuid.UUID, value: str) -> str:
    return hash_phone(f"name-prefix:v1:{tenant_id}:{value}")


def name_tokens(tenant_id: uuid.UUID, name: str) -> list[str]:
    return sorted(
        {token(tenant_id, word[:i]) for word in words(name[:200]) for i in range(2, len(word) + 1)}
    )


def query_tokens(tenant_id: uuid.UUID, query: str) -> list[str]:
    parts = words(query)
    if not parts or any(len(part) < 2 for part in parts):
        raise ValueError(
            "Use at least two characters per name word, or a full phone with country code (+…)."
        )
    return sorted({token(tenant_id, part) for part in parts})


def normalized_phone(value: str) -> str | None:
    compact = re.sub(r"[\s()\-]", "", value)
    return compact if re.fullmatch(r"\+[1-9][0-9]{7,14}", compact) else None
