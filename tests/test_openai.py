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
    assert "assistant_message" in _DiscoveryPayload.model_json_schema()["required"]
    assert "language_support_preference" in _DiscoveryPayload.model_json_schema()["required"]
    assert "delivery_mode_preference" in _DiscoveryPayload.model_json_schema()["required"]
    assert "retracted_preferences" in _DiscoveryPayload.model_json_schema()["required"]
    adapter = OpenAIAdapter("test-key", "test-model", "test-embedding")
    parsed = _DiscoveryPayload(
        intent="discovery",
        assistant_message=(
            "You enjoy charts and want to study data. Which level are you considering?"
        ),
        course_id="not-in-catalog",
        fields=["tech/data", "medicine"],
        education_level="diploma",
        interests=["data", "unseeded interest"],
        activities=["making charts", "unseeded activity"],
        learning_goals=["analyze data", "unseeded goal"],
        language_support_preference="Malayalam discussion support",
        delivery_mode_preference="online",
        unsure=False,
        correct_previous=False,
        retracted_preferences=[
            {"category": "field", "value": "Tech/Data"},
            {"category": "field", "value": "medicine"},
            {"category": "interest", "value": "unseeded interest"},
            {"category": "activity", "value": "making charts"},
            {"category": "learning_goal", "value": "analyze data"},
            {"category": "language_support", "value": "Malayalam discussion support"},
            {"category": "delivery_mode", "value": "online"},
            {"category": "education_level", "value": "diploma"},
        ],
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
        delivery_modes=("online",),
        prerequisites=("Sample entry requirement",),
    )

    context: dict[str, object] = {
        "recent_conversation": [{"role": "assistant", "content": "What do you enjoy?"}],
        "saved_catalog_preferences": [{"fact": "interest_terms_student", "value": "data"}],
        "guidance_stage": "guidance_signal",
        "response_language": "en",
    }
    result = await adapter.extract_discovery(
        "I enjoy charts and want a diploma in data", [course], context
    )

    assert result.course_id is None
    assert result.fields == ("tech/data",)
    assert result.interests == ("data",)
    assert result.activities == ("making charts",)
    assert result.learning_goals == ("analyze data",)
    assert result.language_support_preference == "Malayalam discussion support"
    assert result.delivery_mode_preference == "online"
    assert result.assistant_message == (
        "You enjoy charts and want to study data. Which level are you considering?"
    )
    assert [(item.category, item.value) for item in result.retracted_preferences] == [
        ("field", "tech/data"),
        ("activity", "making charts"),
        ("learning_goal", "analyze data"),
        ("language_support", "Malayalam discussion support"),
        ("delivery_mode", "online"),
        ("education_level", "diploma"),
    ]
    call = parse.await_args.kwargs
    assert call["store"] is False
    assert call["max_output_tokens"] == 700
    assert call["text_format"] is _DiscoveryPayload
    sent = json.loads(call["input"])
    assert sent["current_user_message"] == "I enjoy charts and want a diploma in data"
    assert sent["conversation_context"] == context
    assert sent["allowed_learning_goals"] == ["analyze data"]
    assert sent["allowed_language_supports"] == ["Malayalam discussion support"]
    assert sent["allowed_delivery_modes"] == ["online"]
    assert "telegram_user_id" not in call["input"]
    assert "transcript" not in call["input"]
    assert "untrusted data" in call["instructions"]
    assert "do not reset the profile" in call["instructions"]
    assert "bounded recent conversation" in call["instructions"]
    assert "never as a FAQ or staff request" in call["instructions"]
    assert "actual reply shown to the learner" in call["instructions"]

    unsupported = parsed.model_copy(
        update={"language_support_preference": "unlisted language coaching"}
    )
    parse.return_value = SimpleNamespace(output_parsed=unsupported, usage=None)
    rejected = await adapter.extract_discovery("I want more language coaching", [course])
    assert rejected.language_support_preference is None
    unsupported_mode = parsed.model_copy(update={"delivery_mode_preference": "remote anytime"})
    parse.return_value = SimpleNamespace(output_parsed=unsupported_mode, usage=None)
    rejected_mode = await adapter.extract_discovery("I need remote classes", [course])
    assert rejected_mode.delivery_mode_preference is None
