"""Contextual choices lower effort without becoming enrollment authorization."""

import pytest

from src.engine.guidance_contracts import GuidanceDecision, GuidanceMemory
from src.engine.guidance_interaction import answer_labels, consume_answer, needs_progress


def test_schooling_alone_cannot_be_used_as_interest_fit_evidence(monkeypatch):
    import uuid

    from src.db.models import Course, Lead, TelegramBot
    from src.engine.guidance_contracts import CourseMatch, Note
    from src.engine.guidance_interaction import compose_reply

    monkeypatch.setattr(
        "src.telegram.callbacks.get_settings",
        lambda: type("Settings", (), {"phone_hash_key": "synthetic-unit-signing-key"})(),
    )

    cid = uuid.uuid4()
    course = Course(id=cid, name="Digital Content", description="Creating graphics")
    state = GuidanceMemory(notes=[Note(topic="background", evidence="Class 12 commerce")])
    plan = GuidanceDecision(
        action="recommend",
        response="This is a good fit for your background.",
        matches=[
            CourseMatch(
                course_id=cid,
                student_evidence="Class 12 commerce",
                course_evidence="Creating graphics",
                reason="Fits your background.",
            )
        ],
        question="Which activities interest you?",
        answer_options=["Making pictures", "Solving problems"],
    )
    reply = compose_reply(
        plan,
        state,
        [(course, "eligible", [])],
        {},
        "Class 12 commerce",
        {},
        Lead(id=uuid.uuid4()),
        TelegramBot(id=uuid.uuid4()),
        complete=True,
    )
    assert not state.recommended_ids and "good fit" not in reply.text
    assert "Making pictures" in [b.text for b in reply.buttons]


def test_contextual_choices_include_uncertainty_and_keep_academic_answers_free_text():
    plan = GuidanceDecision(
        action="ask",
        question="Which part sounds interesting?",
        answer_options=["How it looks", "How it works"],
    )
    assert answer_labels(plan) == ["How it looks", "How it works", "Not sure yet"]
    plan.question_field = "age"
    assert answer_labels(plan) == []
    plan.question_field, plan.action = None, "select"
    assert answer_labels(plan) == []


@pytest.mark.parametrize(
    "question",
    [
        "Can you describe specific coding projects you have worked on?",
        "Can you tell me more about the project you built and the technologies you used?",
        "Which frameworks did you use?",
    ],
)
def test_project_proof_is_not_a_gate_to_ordinary_exploration(question):
    assert needs_progress(GuidanceDecision(action="ask", question=question), GuidanceMemory())


def test_repeated_discovery_is_bounded_but_eligibility_and_real_directions_still_work():
    state = GuidanceMemory(questions_since_direction=2)
    plan = GuidanceDecision(action="ask", question="What would you like to build next?")
    assert needs_progress(plan, state)
    plan.question_field = "marks"
    assert not needs_progress(plan, state)
    plan.question_field, plan.action, plan.outside_interests = (
        None,
        "recommend",
        ["Web development"],
    )
    assert not needs_progress(plan, state)


def test_answer_token_is_single_use_and_old_buttons_cannot_consume_new_choices():
    memory = {"guidance_answers": {"nonce": "current", "options": ["How it looks", "Not sure yet"]}}
    assert consume_answer(memory, "old-0") is None and "guidance_answers" in memory
    assert consume_answer(memory, "current-99") is None
    assert consume_answer(memory, "current-0") == "How it looks"
    assert consume_answer(memory, "current-0") is None


def test_old_guidance_memory_remains_loadable():
    state = GuidanceMemory.model_validate({"version": 1, "turns": 7})
    assert state.questions_since_direction == 0


@pytest.mark.parametrize(
    "label", ["/apply", "Visit https://fake.test", "You are guaranteed admission"]
)
def test_generated_choices_cannot_smuggle_commands_or_claims(label):
    plan = GuidanceDecision(action="ask", question="What interests you?", answer_options=[label])
    assert label not in answer_labels(plan)
