"""Shared bounded CRM filters; search values never belong in URLs or audit details."""

import uuid
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Select, or_, select

from src.core.name_search import normalized_phone, query_tokens
from src.core.security import decrypt_pii, hash_phone
from src.db.enums import LeadStatus
from src.db.models import Course, Lead


class LeadFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(default="", max_length=200, repr=False)
    status: LeadStatus | None = None
    course_id: uuid.UUID | None = None


class LeadSearch(LeadFilters):
    offset: int = Field(default=0, ge=0, le=1_000_000)


def lead_statement(tenant_id: uuid.UUID, filters: LeadFilters) -> Select[Lead, str]:
    statement = (
        select(Lead, Course.name)
        .outerjoin(
            Course, (Course.id == Lead.current_course_id) & (Course.tenant_id == Lead.tenant_id)
        )
        .where(Lead.tenant_id == tenant_id)
    )
    if filters.status:
        statement = statement.where(Lead.status == filters.status)
    if filters.course_id:
        statement = statement.where(Lead.current_course_id == filters.course_id)
    query = filters.query.strip()
    if query:
        phone = normalized_phone(query)
        if phone:
            # Legacy ingress stored wa_id without '+'. Accept either exact representation.
            statement = statement.where(
                or_(Lead.phone_hash == hash_phone(phone), Lead.phone_hash == hash_phone(phone[1:]))
            )
        else:
            try:
                tokens = query_tokens(tenant_id, query)
            except ValueError as error:
                raise HTTPException(422, str(error)) from None
            statement = statement.where(Lead.name_search_tokens.contains(tokens))
    return statement.order_by(Lead.updated_at.desc(), Lead.id)


def lead_summary(lead: Lead, course: str | None) -> dict[str, Any]:
    return {
        "id": str(lead.id),
        "name": decrypt_pii(lead.name_enc) if lead.name_enc else None,
        "status": lead.status.value,
        "course": course,
        "course_id": str(lead.current_course_id) if lead.current_course_id else None,
        "readiness_score": lead.readiness_score,
    }
