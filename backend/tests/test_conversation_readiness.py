"""Natural collection and typing are bounded independently of provider availability."""

import asyncio
from unittest.mock import AsyncMock

import pytest

from src.engine.application_profile import Detail, validated_details
from src.engine.guidance import render_decision
from src.engine.guidance_contracts import GuidanceDecision, GuidanceMemory
from src.telegram.adapter import TelegramAPIError, TelegramClient


def test_details_require_literal_evidence_and_do_not_infer_birthdate():
    text = "My name is Anu Nair. My DOB is 2005-03-14."
    result = validated_details(
        [
            Detail(key="full_name", value="Anu Nair", evidence="My name is Anu Nair"),
            Detail(key="dob", value="2005-03-14", evidence="My DOB is 2005-03-14"),
            Detail(key="previous_school", value="Made Up School", evidence="My name is Anu"),
        ],
        text,
    )
    assert result == {"full_name": "Anu Nair", "dob": "2005-03-14"}
    assert (
        validated_details([Detail(key="dob", value="2005-01-01", evidence="I am 21")], "I am 21")
        == {}
    )


@pytest.mark.parametrize("value", ["hi", "hello", "2005-13-01", "tomorrow", "2999-01-01"])
def test_greetings_and_invalid_dates_are_not_saved(value):
    assert validated_details([Detail(key="dob", value=value, evidence=value)], value) == {}
    if value in {"hi", "hello"}:
        assert (
            validated_details([Detail(key="full_name", value=value, evidence=value)], value) == {}
        )


async def test_typing_lifecycle_is_cancelled_on_success_and_failure(monkeypatch):
    client = TelegramClient("synthetic")
    calls = AsyncMock(return_value=True)
    monkeypatch.setattr(client, "call", calls)
    async with client.typing(42, delay=0, interval=0.01):
        await asyncio.sleep(0.025)
    count = calls.call_count
    assert count >= 2
    calls.assert_awaited_with("sendChatAction", {"chat_id": 42, "action": "typing"})
    await asyncio.sleep(0.02)
    assert calls.call_count == count
    with pytest.raises(RuntimeError):
        async with client.typing(42):
            raise RuntimeError("engine failure")


async def test_typing_failure_and_fast_reply_do_not_block_the_reply(monkeypatch):
    client = TelegramClient("synthetic")
    calls = AsyncMock(side_effect=TelegramAPIError(429, retry_after=20))
    monkeypatch.setattr(client, "call", calls)
    async with client.typing(42, delay=0, interval=0.01):
        await asyncio.sleep(0.025)
    assert calls.call_count == 1
    calls.reset_mock()
    async with client.typing(42):
        pass
    calls.assert_not_called()


def test_unverified_reflection_does_not_hide_a_safe_followup():
    decision = GuidanceDecision(
        action="ask",
        response="You meet all eligibility requirements.",
        question="What activities have you enjoyed trying?",
    )
    text, choices = render_decision(decision, GuidanceMemory(), [], complete=True)
    assert text == decision.question and not choices


async def test_explicit_keyed_marks_are_not_reasked_when_model_omits_them(monkeypatch):
    from src.db.models import QualificationRule
    from src.engine.guidance import interpret_turn, merge_evidence
    from src.engine.guidance_contracts import GuidanceInterpretation

    monkeypatch.setattr(
        "src.engine.guidance.decide",
        AsyncMock(side_effect=lambda *args, **kwargs: GuidanceInterpretation(intent="guidance")),
    )
    rules = [QualificationRule(field="age", value=18), QualificationRule(field="marks", value=50)]
    text = "I finished Class 12 commerce, age 19, marks 65. Show me new options."
    interpreted = await interpret_turn(text, GuidanceMemory(), {}, rules, [])
    facts = {}
    merge_evidence(
        GuidanceMemory(), interpreted, text, facts=facts, expected={"age": 18, "marks": 50}
    )
    assert facts == {"age": 19, "marks": 65}
    from src.engine.guidance import academic_number_supported

    assert academic_number_supported("marks", 65.5, "My marks are 65.50.", None)
    assert not academic_number_supported("marks", 65, "My marks are 650.", None)
    for hypothetical in [
        "If my age is 19 and marks 65",
        "My friend has age 19, marks 65",
        "Minimum marks 65",
    ]:
        result = await interpret_turn(hypothetical, GuidanceMemory(), {}, rules, [])
        assert not result.facts


@pytest.mark.parametrize(
    "status,mentioned,expected",
    [("eligible", True, True), ("not_eligible", True, False), ("eligible", False, False)],
)
def test_explicit_named_course_can_be_proposed_without_an_invented_fit_reason(
    status, mentioned, expected
):
    import uuid

    from src.db.models import Course

    course = Course(id=uuid.uuid4(), name="Digital Content Production", description="Media editing")
    plan = GuidanceDecision(action="select", selected_course_id=course.id)
    text, choices = render_decision(
        plan,
        GuidanceMemory(),
        [(course, status, [])],
        complete=True,
        student_text="Please proceed with Digital Content Production" if mentioned else "Hello",
    )
    assert (course.id in choices) is expected
    if expected:
        assert "Would you like to choose Digital Content Production?" in text
