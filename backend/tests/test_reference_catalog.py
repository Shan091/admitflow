"""Published programmes can support exploration without inventing admissions readiness."""

import uuid

from src.db.models import Course
from src.engine.guidance import catalog_status, render_decision
from src.engine.guidance_contracts import GuidanceDecision, GuidanceMemory, Note


def test_reference_programme_is_explorable_without_a_fake_intake():
    course = Course(
        id=uuid.uuid4(),
        name="MCA – AI and ML",
        description="Machine learning",
        is_active=True,
        is_reference=True,
    )
    assert catalog_status(course, [], {}, False) == ("needs_review", [])
    state = GuidanceMemory(notes=[Note(topic="interest", evidence="I like machine learning")])
    decision = GuidanceDecision(
        action="recommend",
        matches=[
            {
                "course_id": course.id,
                "student_evidence": "machine learning",
                "course_evidence": "Machine learning",
                "reason": "This relates to your interest.",
            }
        ],
    )
    text, ids = render_decision(decision, state, [(course, "needs_review", [])], complete=True)
    assert ids == [course.id] and "Published programme" in text
    assert "meet the entry requirements" not in text and "by staff" not in text


def test_reference_programme_cannot_grant_eligibility_even_with_a_batch():
    course = Course(is_active=True, is_reference=True)
    assert catalog_status(course, [], {}, True)[0] == "needs_review"
    course.is_active = False
    assert catalog_status(course, [], {}, True)[0] == "unavailable"
