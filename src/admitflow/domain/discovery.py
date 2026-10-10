"""Explainable catalog-only course matching; this is not an aptitude assessment."""

from dataclasses import dataclass

from admitflow.domain.models import Course


@dataclass(frozen=True, slots=True)
class CourseMatch:
    course: Course
    reasons: tuple[str, ...]


def has_sufficient_guidance_context(
    *,
    interests: set[str],
    activities: set[str],
    level: str | None = None,
    learning_goals: set[str] | None = None,
) -> bool:
    """Require an expressed interest plus one complementary signal to recommend."""
    return bool(
        _normalize(interests)
        and (
            _normalize(activities)
            or (level and level.strip())
            or _normalize(learning_goals or set())
        )
    )


def recommend_courses(
    courses: list[Course],
    *,
    interests: set[str],
    activities: set[str],
    learning_goals: set[str] | None = None,
    level: str | None = None,
    limit: int = 3,
) -> list[CourseMatch]:
    """Rank complete, compatible catalog entries by explicit student-stated interests."""
    if limit < 1:
        raise ValueError("limit must be positive")
    normalized_interests = _normalize(interests)
    normalized_activities = _normalize(activities)
    normalized_goals = _normalize(learning_goals or set())
    matches: list[CourseMatch] = []
    for course in courses:
        if not _is_complete(course) or (level and course.education_level != level):
            continue
        interest_hits = normalized_interests & _normalize(set(course.interests))
        activity_hits = normalized_activities & _normalize(set(course.activities))
        course_goals = _normalize(set(course.learning_goals))
        goal_hits = normalized_goals & course_goals
        field_hit = _normalize({course.field}) & normalized_interests
        if normalized_goals and not goal_hits:
            continue
        if not interest_hits and not activity_hits and not field_hit:
            continue
        reasons = tuple(
            [f"Matches your interest in {item}" for item in sorted(interest_hits)]
            + [f"Matches your interest in {item}" for item in sorted(field_hit)]
            + [f"Includes activities you chose: {item}" for item in sorted(activity_hits)]
            + [f"Supports your study goal: {item}" for item in sorted(goal_hits)]
        )
        matches.append(CourseMatch(course, reasons))
    matches.sort(key=lambda item: (-len(item.reasons), item.course.name.casefold()))
    return matches[:limit]


def _normalize(values: set[str]) -> set[str]:
    return {" ".join(value.casefold().split()) for value in values if value.strip()}


def _is_complete(course: Course) -> bool:
    return bool(
        course.name.strip()
        and course.description.strip()
        and course.education_level.strip()
        and course.field.strip()
        and course.interests
        and course.activities
        and course.prerequisites
        and course.medium.strip()
    )
