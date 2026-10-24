"""Bounded exploratory guidance; evidence notes are not psychometric measurements."""

import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Topic = Literal[
    "background", "interest", "strength", "value", "constraint", "goal", "avoid", "decision"
]
Stage = Literal["exploring", "comparing", "decided"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Note(StrictModel):
    topic: Topic
    evidence: str = Field(min_length=1, max_length=300)


class ProfileUpdate(Note):
    replaces: list[str] = Field(
        default_factory=list,
        max_length=3,
        description="Full prior note quotations explicitly corrected by this update. "
        "Do not clear a whole topic. Keep unrelated education, experience and preferences.",
    )


class InterestTheme(StrictModel):
    theme: Literal[
        "practical", "investigative", "creative", "helping", "enterprising", "organizing"
    ]
    evidence: str = Field(min_length=1, max_length=300)


class StudyFact(StrictModel):
    key: str = Field(min_length=1, max_length=64)
    value: str = Field(min_length=1, max_length=200)
    evidence: str = Field(min_length=1, max_length=300)


class GuidanceInterpretation(StrictModel):
    intent: Literal["guidance", "faq", "qualification", "handoff", "browse"]
    updates: list[ProfileUpdate] = Field(default_factory=list, max_length=6)
    facts: list[StudyFact] = Field(default_factory=list, max_length=12)


class CourseMatch(StrictModel):
    course_id: uuid.UUID
    student_evidence: str = Field(min_length=3, max_length=300)
    course_evidence: str = Field(min_length=3, max_length=300)
    reason: str = Field(
        min_length=1,
        max_length=240,
        description="Interest-fit explanation in second person, grounded in both quotes. "
        "No academic eligibility, requirements, fees, admission or selection-action claims.",
    )


class GuidanceMemory(StrictModel):
    version: Literal[1] = 1
    active: bool = True
    deeper: bool = False
    stage: Stage = "exploring"
    notes: list[Note] = Field(default_factory=list, max_length=40)
    themes: list[InterestTheme] = Field(default_factory=list, max_length=3)
    last_question: str | None = Field(default=None, max_length=250)
    last_field: str | None = Field(default=None, max_length=64)
    pending_course: uuid.UUID | None = None
    recommended_ids: list[uuid.UUID] = Field(default_factory=list, max_length=3)
    turns: int = Field(default=0, ge=0)


class GuidanceDecision(StrictModel):
    action: Literal["ask", "recommend", "select"]
    response: str = Field(
        default="",
        max_length=500,
        description="One brief declarative acknowledgment. "
        "No question, eligibility claim or action claim.",
    )
    question: str | None = Field(default=None, min_length=1, max_length=250)
    question_field: str | None = Field(default=None, max_length=64)
    stage: Stage = "exploring"
    updates: list[ProfileUpdate] = Field(default_factory=list, max_length=6)
    facts: list[StudyFact] = Field(default_factory=list, max_length=12)
    themes: list[InterestTheme] = Field(default_factory=list, max_length=3)
    matches: list[CourseMatch] = Field(default_factory=list, max_length=3)
    outside_interests: list[str] = Field(
        default_factory=list,
        max_length=2,
        description="General study/career areas outside this catalog, e.g. marine biology. "
        "Never profile field names such as age, marks, background or budget. Empty if unnecessary.",
    )
    selected_course_id: uuid.UUID | None = None
