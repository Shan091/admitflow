"""Typed domain data used by the demo."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class Course:
    id: str
    tenant_id: str
    name: str
    description: str
    minimum_marks_percent: float
    application_fee_paise: int
    education_level: str = "undergraduate"
    field: str = ""
    interests: tuple[str, ...] = ()
    activities: tuple[str, ...] = ()
    prerequisites: tuple[str, ...] = ()
    medium: str = "English"
    language_support: tuple[str, ...] = ()
    learning_goals: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DiscoveryTurn:
    """Catalog-bounded interpretation of one chat message."""

    intent: Literal[
        "discovery", "course_lookup", "knowledge_question", "staff_request", "out_of_scope", "other"
    ]
    course_id: str | None
    fields: tuple[str, ...]
    education_level: str | None
    interests: tuple[str, ...]
    activities: tuple[str, ...]
    unsure: bool
    correct_previous: bool
    learning_goals: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class QualificationResult:
    eligible: bool
    reason: str


LeadStatus = Literal["browsing", "awaiting_grade12", "awaiting_marks", "qualified", "not_eligible"]
