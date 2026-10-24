"""Student evidence and catalog checks constrain adaptive course guidance."""

import uuid
from unittest.mock import AsyncMock

import pytest

from src.db.enums import RuleOperator
from src.db.models import Course, QualificationRule
from src.engine.guidance import (
    catalog_status,
    merge_evidence,
    question_field,
    render_decision,
    request_decision,
)
from src.engine.guidance_contracts import (
    GuidanceDecision,
    GuidanceMemory,
    Note,
    ProfileUpdate,
    StudyFact,
)
from src.engine.llm_factory import AllProvidersFailedError


def decision(**kwargs):
    return GuidanceDecision.model_validate(
        {
            "action": "ask",
            "response": "Let's explore what matters to you.",
            "question": "What have you enjoyed learning recently?",
            "stage": "exploring",
            **kwargs,
        }
    )


def course(name="Data and Reporting", description="Explore spreadsheets and data patterns."):
    return Course(
        id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        name=name,
        description=description,
        is_active=True,
        application_fee=50000,
    )


def test_profile_uses_only_current_explicit_evidence_and_corrections():
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy coding")])
    merge_evidence(
        state,
        decision(
            updates=[
                ProfileUpdate(
                    topic="interest", evidence="I prefer drawing now", replaces=["I enjoy coding"]
                ),
                ProfileUpdate(topic="strength", evidence="excellent at mathematics"),
            ]
        ),
        "Actually, I prefer drawing now",
    )
    assert [(n.topic, n.evidence) for n in state.notes] == [("interest", "I prefer drawing now")]
    assert state.stage == "exploring"


def test_quote_recovery_keeps_original_wording_not_paraphrases():
    state = GuidanceMemory()
    merge_evidence(
        state,
        decision(
            updates=[
                ProfileUpdate(topic="background", evidence="Finished Class 12 commerce."),
                ProfileUpdate(topic="interest", evidence="I love design"),
            ]
        ),
        "I finished Class 12 commerce. I like design.",
    )
    assert [n.evidence for n in state.notes] == ["finished Class 12 commerce"]


def test_partial_correction_preserves_unrelated_background():
    state = GuidanceMemory(
        notes=[
            Note(topic="background", evidence="I finished Class 12"),
            Note(topic="background", evidence="I worked in retail"),
        ]
    )
    merge_evidence(
        state,
        decision(
            updates=[
                ProfileUpdate(
                    topic="background",
                    evidence="I volunteered at a shop",
                    replaces=["I worked in retail"],
                )
            ]
        ),
        "Actually I volunteered at a shop",
    )
    assert [n.evidence for n in state.notes] == ["I finished Class 12", "I volunteered at a shop"]


def test_eligibility_remains_separate_and_unknown_is_not_a_pass():
    c = course()
    rule = QualificationRule(field="age", operator=RuleOperator.GTE, value=18)
    assert catalog_status(c, [rule], {}, True)[0] == "needs_information"
    assert catalog_status(c, [rule], {"age": 17}, True)[0] == "not_eligible"
    assert catalog_status(c, [rule], {"age": 20}, True)[0] == "eligible"
    assert catalog_status(c, [rule], {"age": 20}, False)[0] == "unavailable"
    assert catalog_status(c, [], {"age": 20}, True)[0] == "needs_review"


def test_profile_notes_cannot_create_academic_facts():
    state = GuidanceMemory()
    facts = {}
    merge_evidence(
        state,
        decision(facts=[StudyFact(key="age", value="21", evidence="I like data")]),
        "I like data",
        facts=facts,
        expected={"age": 18},
    )
    assert facts == {}
    merge_evidence(
        state,
        decision(facts=[StudyFact(key="age", value="21", evidence="21")]),
        "I am 21",
        facts=facts,
        expected={"age": 18},
    )
    assert facts == {"age": 21}
    merge_evidence(
        state,
        decision(facts=[StudyFact(key="age", value="22", evidence="22")]),
        "22",
        facts=facts,
        expected={"age": 18},
    )
    assert facts == {"age": 21}  # a bare number has no active academic field


def test_interest_scores_and_unrelated_numbers_cannot_become_marks_or_age():
    state = GuidanceMemory()
    facts = {}
    merge_evidence(
        state,
        decision(
            facts=[
                StudyFact(key="age", value="70", evidence="70"),
                StudyFact(key="marks", value="21", evidence="21"),
            ]
        ),
        "I am 21 and my O*NET interest score is 70",
        facts=facts,
        expected={"age": 18, "marks": 50},
    )
    assert facts == {}


def test_short_answer_field_matches_the_question_the_student_actually_saw():
    assert question_field("How old are you?", "age", {"age": 18}) == "age"
    assert question_field("What percentage did you get?", "marks", {"marks": 50}) == "marks"
    assert question_field("How many photos did you arrange?", "age", {"age": 18}) is None


def test_discussing_a_students_financial_priority_is_not_a_salary_promise():
    result = decision(
        response="It helps to know that salary and affordable tuition matter to you.",
        question="What kind of work would you enjoy doing each day?",
    )
    text, _ = render_decision(result, GuidanceMemory(), [], complete=True)
    assert "salary and affordable tuition" in text


def test_recommendation_requires_student_and_course_evidence():
    c = course()
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy working with numbers")])
    result = decision(
        action="recommend",
        question=None,
        matches=[
            {
                "course_id": str(c.id),
                "student_evidence": "working with numbers",
                "course_evidence": "spreadsheets and data patterns",
                "reason": "This lets you explore the data work you enjoy.",
            }
        ],
    )
    text, choices = render_decision(result, state, [(c, "eligible", [])], complete=True)
    assert c.name in text and choices == [c.id]
    assert "Your shared details meet the entry requirements" in text
    assert "data work you enjoy" in text
    wrong = result.model_copy(deep=True)
    wrong.matches[0].course_id = uuid.uuid4()
    text, choices = render_decision(wrong, state, [(c, "eligible", [])], complete=True)
    assert not choices and "could not verify" in text.lower()


def test_bad_generated_reason_falls_back_to_verified_quotes_not_a_false_claim():
    c = course()
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy data")])
    result = decision(
        action="recommend",
        question=None,
        matches=[
            {
                "course_id": str(c.id),
                "student_evidence": "I enjoy data",
                "course_evidence": "spreadsheets",
                "reason": "You meet the eligibility requirements.",
            }
        ],
    )
    text, choices = render_decision(
        result, state, [(c, "needs_information", ["age"])], complete=True
    )
    assert choices == [c.id]
    assert "You meet" not in text and "Entry details still need checking: age" in text
    assert "I enjoy data" in text and "spreadsheets" in text


def test_course_card_replaces_unverified_model_eligibility_reflection():
    c = course()
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy data")])
    result = decision(
        action="recommend",
        response="Your age and marks meet the criteria.",
        question=None,
        matches=[
            {
                "course_id": str(c.id),
                "student_evidence": "I enjoy data",
                "course_evidence": "spreadsheets",
                "reason": "A possible direction to explore.",
            }
        ],
    )
    text, choices = render_decision(
        result, state, [(c, "needs_information", ["marks"])], complete=True
    )
    assert choices == [c.id] and "meet the criteria" not in text
    assert "Entry details still need checking: marks" in text


@pytest.mark.parametrize("status", ["not_eligible", "unavailable"])
def test_ineligible_and_closed_courses_are_not_recommended(status):
    c = course()
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy data")])
    result = decision(
        action="recommend",
        matches=[
            {
                "course_id": str(c.id),
                "student_evidence": "data",
                "course_evidence": "spreadsheets",
                "reason": "A possible direction to explore.",
            }
        ],
    )
    text, choices = render_decision(result, state, [(c, status, [])], complete=True)
    assert choices == [] and c.name not in text


def test_missing_course_is_honest_without_pushing_a_local_substitute():
    result = decision(
        action="recommend",
        response="You can keep exploring your original interest.",
        question=None,
        outside_interests=["Marine biology"],
    )
    text, choices = render_decision(result, GuidanceMemory(), [], complete=True)
    assert not choices
    assert "could not verify" in text.lower() and "elsewhere" in text
    assert "Marine biology" in text and "not verified" in text
    text, _ = render_decision(result, GuidanceMemory(), [], complete=False)
    assert "incomplete" in text.lower()


@pytest.mark.parametrize(
    "response",
    [
        "You are guaranteed admission.",
        "Tuition is INR 5000.",
        "Your IQ is 120.",
        "You have a 98% match.",
        "Visit https://fake-college.test/pay",
        "You meet the eligibility requirements.",
        "I will select that course for you.",
    ],
)
def test_unsupported_output_never_reaches_the_student(response):
    text, choices = render_decision(
        decision(response=response), GuidanceMemory(), [], complete=True
    )
    assert response not in text and not choices
    assert text == decision().question


async def test_decision_has_bounded_context_and_preserves_refusal_and_unknowns(monkeypatch):
    captured = AsyncMock(return_value=decision())
    monkeypatch.setattr("src.engine.guidance.decide", captured)
    state = GuidanceMemory(
        notes=[Note(topic="constraint", evidence="I prefer not to share a budget")]
    )
    await request_decision(
        "Not sure", state, [], {}, [], [{"role": "user", "content": "x" * 6000}] * 30, complete=True
    )
    messages = captured.call_args.args[1]
    assert len(str(messages)) < 22000
    assert "I prefer not to share a budget" in str(messages)
    assert "not a validated" in messages[0]["content"]


async def test_no_model_response_is_not_silently_treated_as_a_fit(monkeypatch):
    monkeypatch.setattr(
        "src.engine.guidance.decide", AsyncMock(side_effect=AllProvidersFailedError)
    )
    with pytest.raises(AllProvidersFailedError):
        await request_decision("Help me choose", GuidanceMemory(), [], {}, [], [], complete=True)


def test_course_confirmation_is_owned_by_code_not_an_unrelated_model_question():
    c = course()
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I enjoy data")])
    result = decision(
        action="select",
        selected_course_id=c.id,
        question="Would you like staff help?",
        matches=[
            {
                "course_id": c.id,
                "student_evidence": "I enjoy data",
                "course_evidence": "spreadsheets",
                "reason": "A direction to explore.",
            }
        ],
    )
    text, choices = render_decision(result, state, [(c, "eligible", [])], complete=True)
    assert choices == [c.id] and "Would you like staff help?" not in text
    assert f"Would you like to choose {c.name}?" in text
