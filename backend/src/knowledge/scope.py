"""Code-owned course scopes for approved institution references."""

import re
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from src.db.models import Course, Document


class AmbiguousCourseReference(ValueError):
    """More than one active course has the requested name without a selected owner."""


def reference_scope(course_ids: list[uuid.UUID]) -> ColumnElement[bool]:
    tag = Document.metadata_json["course_id"].astext
    return or_(tag.is_(None), tag.in_([str(value) for value in course_ids]))


async def question_courses(
    db: AsyncSession,
    tenant_id: uuid.UUID,
    question: str,
    selected: Course | None,
    *,
    fallback_to_selection: bool = True,
) -> list[uuid.UUID]:
    """Explicit catalog names take precedence over selection; no model invents IDs."""
    candidates = (
        await db.scalars(
            select(Course)
            .where(
                Course.tenant_id == tenant_id,
                Course.is_active.is_(True),
                func.strpos(func.lower(question), func.lower(Course.name)) > 0,
            )
            .order_by(func.length(Course.name).desc(), Course.id)
            .limit(20)
        )
    ).all()
    used: list[tuple[int, int]] = []
    matches = []
    groups: dict[str, list[Course]] = {}
    for course in candidates:
        groups.setdefault(course.name.casefold(), []).append(course)
    for group in groups.values():
        course = group[0]
        spans = [
            match.span()
            for match in re.finditer(rf"(?<!\w){re.escape(course.name)}(?!\w)", question, re.I)
        ]
        if any(not any(start >= a and end <= b for a, b in used) for start, end in spans):
            if len(group) > 1:
                if selected is None or selected.id not in [item.id for item in group]:
                    raise AmbiguousCourseReference("Select the intended course first")
                matches.append(selected.id)
            else:
                matches.append(course.id)
            used.extend(spans)
    return matches or ([selected.id] if selected and fallback_to_selection else [])
