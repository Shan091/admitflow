"""Translate retrieval queries without weakening the relevance floor."""

from types import SimpleNamespace
from typing import Any

import pytest

from src.knowledge.retrieval import retrieval_query


async def test_english_query_does_not_call_model(monkeypatch: pytest.MonkeyPatch) -> None:
    async def unavailable(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("English queries do not need translation")

    monkeypatch.setattr("src.knowledge.retrieval.generate_completion", unavailable)
    assert await retrieval_query("Where is campus?") == "Where is campus?"


async def test_non_ascii_query_uses_validated_translation(monkeypatch: pytest.MonkeyPatch) -> None:
    async def response(*args: Any, **kwargs: Any) -> Any:
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content='{"query":"Where is the demo campus?"}')
                )
            ]
        )

    monkeypatch.setattr("src.knowledge.retrieval.generate_completion", response)
    assert await retrieval_query("ഡെമോ ക്യാമ്പസ് എവിടെയാണ്?") == "Where is the demo campus?"
