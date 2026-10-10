"""Reviewed expected-match matrix for the fictional course catalog."""

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.domain.discovery import recommend_courses


@pytest.mark.parametrize(
    ("field", "level", "expected_ids"),
    [
        (
            "tech/data",
            "vocational_certificate",
            {
                "digital-literacy-certificate",
                "digital-security-certificate",
                "it-support-certificate",
            },
        ),
        ("tech/data", "diploma", {"data-analytics-diploma", "web-development-diploma"}),
        (
            "tech/data",
            "undergraduate",
            {
                "foundations-computing",
                "software-systems-bachelors",
                "information-systems-bachelors",
            },
        ),
        ("tech/data", "postgraduate", {"data-science-masters", "applied-data-systems-masters"}),
        (
            "business/accounting",
            "vocational_certificate",
            {
                "business-analytics",
                "bookkeeping-certificate",
                "entrepreneurship-certificate",
                "project-coordination-certificate",
            },
        ),
        (
            "business/accounting",
            "diploma",
            {"marketing-sales-diploma", "small-enterprise-finance-diploma"},
        ),
        (
            "business/accounting",
            "undergraduate",
            {"business-management-bachelors", "business-operations-bachelors"},
        ),
        (
            "business/accounting",
            "postgraduate",
            {"business-strategy-masters", "enterprise-operations-masters"},
        ),
        (
            "design/media",
            "vocational_certificate",
            {
                "digital-media-certificate",
                "visual-storytelling-certificate",
                "visual-communication-certificate",
            },
        ),
        (
            "design/media",
            "diploma",
            {"digital-design-diploma", "user-experience-design-diploma", "motion-design-diploma"},
        ),
        (
            "design/media",
            "undergraduate",
            {"digital-product-design-bachelors", "digital-media-production-bachelors"},
        ),
        (
            "design/media",
            "postgraduate",
            {"design-media-masters", "accessible-communication-design-masters"},
        ),
        (
            "hospitality/tourism",
            "vocational_certificate",
            {"guest-services-certificate", "sustainable-tourism-certificate"},
        ),
        (
            "hospitality/tourism",
            "diploma",
            {"hospitality-diploma", "event-operations-diploma", "heritage-tourism-diploma"},
        ),
        (
            "hospitality/tourism",
            "undergraduate",
            {
                "tourism-undergraduate",
                "hospitality-management-bachelors",
                "hospitality-events-bachelors",
            },
        ),
        (
            "hospitality/tourism",
            "postgraduate",
            {"tourism-planning-masters", "hospitality-strategy-masters"},
        ),
        (
            "vocational-skills",
            "vocational_certificate",
            {
                "food-service-skills",
                "office-administration-certificate",
                "retail-customer-service-certificate",
                "textile-craft-certificate",
                "customer-service-practice-certificate",
                "repair-reuse-certificate",
            },
        ),
        (
            "vocational-skills",
            "diploma",
            {
                "event-setup-diploma",
                "retail-merchandising-diploma",
                "event-operations-diploma-advanced",
                "inventory-operations-diploma",
            },
        ),
        ("vocational-skills", "undergraduate", set()),
        ("vocational-skills", "postgraduate", set()),
    ],
)
def test_field_level_matrix_returns_only_reviewed_complete_offerings(
    tmp_path, field: str, level: str, expected_ids: set[str]
) -> None:
    repository = Repository(tmp_path / "catalog.sqlite3")
    repository.initialize()
    repository.seed_catalog()

    matches = recommend_courses(
        repository.list_courses(repository.tenant_id),
        interests={field},
        activities=set(),
        level=level,
        limit=100,
    )

    assert {match.course.id for match in matches} == expected_ids
    assert all(match.course.field == field for match in matches)
    assert all(match.course.education_level == level for match in matches)
    assert all(
        any("Matches your interest in" in reason for reason in match.reasons) for match in matches
    )


def test_mixed_field_interests_keep_all_catalog_grounded_alternatives(tmp_path) -> None:
    repository = Repository(tmp_path / "catalog.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    courses = repository.list_courses(repository.tenant_id)

    matches = recommend_courses(
        courses,
        interests={"tech/data", "design/media"},
        activities=set(),
        limit=100,
    )

    assert matches
    assert {match.course.field for match in matches} == {"tech/data", "design/media"}
    assert all(match.reasons for match in matches)


@pytest.mark.parametrize(
    ("interests", "learning_goals"),
    [
        ({"aerospace medicine"}, set()),
        ({"tech/data"}, {"manage small enterprise finances"}),
    ],
)
def test_unsupported_or_conflicting_catalog_preferences_abstain(
    tmp_path, interests: set[str], learning_goals: set[str]
) -> None:
    repository = Repository(tmp_path / "catalog.sqlite3")
    repository.initialize()
    repository.seed_catalog()

    matches = recommend_courses(
        repository.list_courses(repository.tenant_id),
        interests=interests,
        activities=set(),
        learning_goals=learning_goals,
        limit=100,
    )

    assert matches == []
