from dataclasses import replace

import pytest

from admitflow.domain.discovery import has_sufficient_guidance_context, recommend_courses
from admitflow.domain.models import Course
from admitflow.domain.pricing import format_inr_from_paise
from admitflow.domain.qualification import assess_eligibility


def test_eligibility_requires_grade_twelve_even_with_high_marks() -> None:
    result = assess_eligibility(completed_grade12=False, marks_percent=99, minimum_marks_percent=50)
    assert not result.eligible
    assert "Grade 12" in result.reason


def test_eligibility_threshold_is_inclusive() -> None:
    result = assess_eligibility(completed_grade12=True, marks_percent=50, minimum_marks_percent=50)
    assert result.eligible


def test_marks_below_course_threshold_are_ineligible() -> None:
    result = assess_eligibility(
        completed_grade12=True, marks_percent=49.99, minimum_marks_percent=50
    )
    assert not result.eligible


@pytest.mark.parametrize("marks", [-0.1, 100.1])
def test_qualification_rejects_out_of_range_marks(marks: float) -> None:
    with pytest.raises(ValueError):
        assess_eligibility(completed_grade12=True, marks_percent=marks, minimum_marks_percent=50)


def test_fee_formatting_uses_rupees_and_paise() -> None:
    assert format_inr_from_paise(123456) == "₹1,234.56"
    assert format_inr_from_paise(50000) == "₹500"


def test_fee_formatting_rejects_negative_amount() -> None:
    with pytest.raises(ValueError):
        format_inr_from_paise(-1)


@pytest.mark.parametrize(
    ("interests", "activities", "level", "expected"),
    [
        ({"tech/data"}, set(), None, False),
        ({"tech/data"}, {"making charts"}, None, True),
        ({"tech/data"}, set(), "diploma", True),
        (set(), {"making charts"}, None, False),
        (set(), set(), "diploma", False),
        (set(), set(), None, False),
    ],
)
def test_guidance_needs_two_complementary_signals_before_recommendation(
    interests: set[str], activities: set[str], level: str | None, expected: bool
) -> None:
    assert (
        has_sufficient_guidance_context(interests=interests, activities=activities, level=level)
        is expected
    )


def _course(
    course_id: str,
    interests: tuple[str, ...],
    *,
    level: str = "diploma",
    activities: tuple[str, ...] = ("making charts",),
    learning_goals: tuple[str, ...] = (),
) -> Course:
    return Course(
        id=course_id,
        tenant_id="demo",
        name=course_id,
        description="fictional course",
        minimum_marks_percent=0,
        application_fee_paise=100,
        education_level=level,
        field="sample field",
        interests=interests,
        activities=activities,
        prerequisites=("basic reading",),
        medium="English",
        language_support=("Malayalam discussion support",),
        learning_goals=learning_goals,
    )


def test_recommendations_are_explainable_and_match_only_explicit_preferences() -> None:
    courses = [
        _course("data", ("data", "technology")),
        _course("design", ("design",), activities=("making posters",)),
        _course("unrelated", ("hospitality",), activities=("serving guests",)),
    ]

    matches = recommend_courses(
        courses,
        interests={" DATA "},
        activities={"making charts"},
    )

    assert [match.course.id for match in matches] == ["data"]
    assert matches[0].reasons == (
        "Matches your interest in data",
        "Includes activities you chose: making charts",
    )


def test_explicit_study_goal_filters_and_explains_course_matches() -> None:
    courses = [
        _course("data", ("technology",), learning_goals=("analyze data",)),
        _course("design", ("technology",), learning_goals=("create visual work",)),
    ]

    matches = recommend_courses(
        courses,
        interests={"technology"},
        activities={"making charts"},
        learning_goals={"analyze data"},
    )

    assert [match.course.id for match in matches] == ["data"]
    assert "Supports your study goal: analyze data" in matches[0].reasons


def test_explicit_language_support_preference_filters_and_explains_matches() -> None:
    courses = [
        _course("malayalam-support", ("technology",)),
        replace(
            _course("english-support", ("technology",)),
            language_support=("English support sessions",),
        ),
    ]

    matches = recommend_courses(
        courses,
        interests={"technology"},
        activities={"making charts"},
        language_support_preference="Malayalam discussion support",
    )

    assert [match.course.id for match in matches] == ["malayalam-support"]
    assert "Lists language support: Malayalam discussion support" in matches[0].reasons


def test_recommendations_filter_by_level_and_exclude_incomplete_catalog_items() -> None:
    complete = _course("diploma", ("data",))
    postgraduate = _course("masters", ("data",), level="postgraduate")
    incomplete = Course(
        id="missing",
        tenant_id="demo",
        name="Missing",
        description="",
        minimum_marks_percent=0,
        application_fee_paise=100,
    )

    matches = recommend_courses(
        [complete, postgraduate, incomplete],
        interests={"data"},
        activities=set(),
        level="postgraduate",
    )

    assert [match.course.id for match in matches] == ["masters"]
