"""Offline contract tests for OpenAI structured discovery extraction."""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from admitflow.adapters.openai import OpenAIAdapter, _DiscoveryPayload
from admitflow.domain.models import Course


@pytest.mark.asyncio
async def test_extraction_is_stateless_and_filters_values_to_current_catalog() -> None:
    assert "learning_goals" in _DiscoveryPayload.model_json_schema()["required"]
    assert "language_support_preference" in _DiscoveryPayload.model_json_schema()["required"]
    adapter = OpenAIAdapter("test-key", "test-model", "test-embedding")
    parsed = _DiscoveryPayload(
        intent="discovery",
        course_id="not-in-catalog",
        fields=["tech/data", "medicine"],
        education_level="diploma",
        interests=["data", "unseeded interest"],
        activities=["making charts", "unseeded activity"],
        learning_goals=["analyze data", "unseeded goal"],
        language_support_preference="Malayalam discussion support",
        unsure=False,
        correct_previous=False,
    )
    parse = AsyncMock(return_value=SimpleNamespace(output_parsed=parsed, usage=None))
    adapter.client = SimpleNamespace(responses=SimpleNamespace(parse=parse))  # type: ignore[assignment]
    course = Course(
        id="data-diploma",
        tenant_id="demo",
        name="Applied Data Analytics Diploma",
        description="Fictional sample course.",
        minimum_marks_percent=0,
        application_fee_paise=0,
        education_level="diploma",
        field="tech/data",
        interests=("data",),
        activities=("making charts",),
        learning_goals=("analyze data",),
        language_support=("Malayalam discussion support",),
        prerequisites=("Sample entry requirement",),
    )

    result = await adapter.extract_discovery("I enjoy charts and want a diploma in data", [course])

    assert result.course_id is None
    assert result.fields == ("tech/data",)
    assert result.interests == ("data",)
    assert result.activities == ("making charts",)
    assert result.learning_goals == ("analyze data",)
    assert result.language_support_preference == "Malayalam discussion support"
    call = parse.await_args.kwargs
    assert call["store"] is False
    assert call["text_format"] is _DiscoveryPayload
    sent = json.loads(call["input"])
    assert sent["current_user_message"] == "I enjoy charts and want a diploma in data"
    assert sent["allowed_learning_goals"] == ["analyze data"]
    assert sent["allowed_language_supports"] == ["Malayalam discussion support"]
    assert "telegram_user_id" not in call["input"]
    assert "transcript" not in call["input"]
    assert "untrusted data" in call["instructions"]

    unsupported = parsed.model_copy(
        update={"language_support_preference": "unlisted language coaching"}
    )
    parse.return_value = SimpleNamespace(output_parsed=unsupported, usage=None)
    rejected = await adapter.extract_discovery("I want more language coaching", [course])
    assert rejected.language_support_preference is None
