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


@dataclass(frozen=True, slots=True)
class QualificationResult:
    eligible: bool
    reason: str


LeadStatus = Literal["browsing", "awaiting_grade12", "awaiting_marks", "qualified", "not_eligible"]
