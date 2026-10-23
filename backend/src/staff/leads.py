"""Authenticated, audited lead/conversation access and explicit human-request controls."""

import json
import time
import uuid
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from src.core.security import decrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import LeadStatus
from src.db.models import (
    Batch,
    ConversationEvent,
    ConversationMemory,
    Course,
    HumanRequest,
    Lead,
)
from src.engine.timeline import timeline
from src.staff.auth import Db, Staff, require_browser_write

router = APIRouter(prefix="/api/staff", tags=["staff admissions"])


async def get_lead(db: Db, staff: Staff, lead_id: uuid.UUID, *, lock: bool = False) -> Lead:
    statement = select(Lead).where(Lead.id == lead_id, Lead.tenant_id == staff.tenant_id)
    lead = await db.scalar(
        statement.with_for_update().execution_options(populate_existing=True) if lock else statement
    )
    if lead is None:
        raise HTTPException(404, "Inquiry not found.")
    return lead


@router.get("/courses")
async def course_options(staff: Staff, db: Db) -> list[dict[str, str]]:
    rows = (
        await db.scalars(
            select(Course)
            .where(Course.tenant_id == staff.tenant_id)
            .order_by(Course.name)
            .limit(200)
        )
    ).all()
    return [{"id": str(row.id), "name": row.name} for row in rows]


@router.get("/leads")
async def leads(
    staff: Staff,
    db: Db,
    status: LeadStatus | None = None,
    course_id: uuid.UUID | None = None,
    offset: int = Query(default=0, ge=0),
) -> list[dict[str, Any]]:
    statement = select(Lead, Course.name).outerjoin(
        Course, (Course.id == Lead.current_course_id) & (Course.tenant_id == Lead.tenant_id)
    )
    statement = statement.where(Lead.tenant_id == staff.tenant_id)
    if status:
        statement = statement.where(Lead.status == status)
    if course_id:
        statement = statement.where(Lead.current_course_id == course_id)
    rows = (
        await db.execute(
            statement.order_by(Lead.updated_at.desc(), Lead.id).offset(offset).limit(50)
        )
    ).all()
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="staff.leads_viewed"
    )
    await db.commit()
    return [
        {
            "id": str(lead.id),
            "status": lead.status.value,
            "course": name,
            "course_id": str(lead.current_course_id) if lead.current_course_id else None,
        }
        for lead, name in rows
    ]


@router.get("/leads/{lead_id}")
async def lead_detail(
    lead_id: uuid.UUID,
    staff: Staff,
    db: Db,
    cursor: str | None = Query(default=None, max_length=200),
) -> dict[str, Any]:
    lead = await get_lead(db, staff, lead_id)
    saved = await db.scalar(
        select(ConversationMemory).where(
            ConversationMemory.tenant_id == staff.tenant_id, ConversationMemory.lead_id == lead.id
        )
    )
    memory = json.loads(decrypt_pii(saved.payload_enc)) if saved else {}
    messages, older_cursor = await timeline(db, staff.tenant_id, lead.id, cursor)
    draft = memory.get("staff_draft", {})
    latest_event = (
        await db.scalar(
            select(ConversationEvent.id)
            .where(
                ConversationEvent.tenant_id == staff.tenant_id, ConversationEvent.lead_id == lead.id
            )
            .order_by(ConversationEvent.update_id.desc())
            .limit(1)
        )
        if draft
        else None
    )
    draft_stale = bool(
        draft
        and (
            not lead.copilot_mode
            or draft.get("source_event_id") != str(latest_event)
            or draft.get("expires_at", 0) <= time.time()
            or draft.get("revision", 0) != memory.get("staff_revision", 0)
        )
    )
    batch_name = await db.scalar(
        select(Batch.name).where(
            Batch.id == lead.current_batch_id, Batch.tenant_id == staff.tenant_id
        )
    )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.conversation_viewed",
        lead_id=lead.id,
    )
    await db.commit()
    return {
        "id": str(lead.id),
        "status": lead.status.value,
        "copilot_mode": lead.copilot_mode,
        "draft_stale": draft_stale,
        "memory": memory,
        "course_id": str(lead.current_course_id) if lead.current_course_id else None,
        "batch_id": str(lead.current_batch_id) if lead.current_batch_id else None,
        "batch_name": batch_name,
        "messages": messages,
        "older_cursor": older_cursor,
    }


@router.get("/human-requests")
async def human_requests(
    staff: Staff, db: Db, offset: int = Query(default=0, ge=0)
) -> list[dict[str, str]]:
    rows = (
        await db.scalars(
            select(HumanRequest)
            .where(HumanRequest.tenant_id == staff.tenant_id)
            .order_by(HumanRequest.updated_at.desc(), HumanRequest.id)
            .offset(offset)
            .limit(50)
        )
    ).all()
    return [{"id": str(row.id), "lead_id": str(row.lead_id), "status": row.status} for row in rows]


@router.post("/human-requests/{request_id}/{action}", dependencies=[Depends(require_browser_write)])
async def update_request(
    request_id: uuid.UUID, action: Literal["acknowledge", "resolve", "resume"], staff: Staff, db: Db
) -> dict[str, str]:
    request = await db.scalar(
        select(HumanRequest).where(
            HumanRequest.id == request_id, HumanRequest.tenant_id == staff.tenant_id
        )
    )
    if request is None:
        raise HTTPException(404, "Request not found.")
    # Match engine lock order: lead first, then dependent records.
    lead = await get_lead(db, staff, request.lead_id, lock=True)
    await db.refresh(request, with_for_update=True)
    transitions = {
        "acknowledge": ({"open"}, "acknowledged"),
        "resolve": ({"open", "acknowledged"}, "resolved"),
        "resume": ({"resolved"}, "resumed"),
    }
    allowed, destination = transitions[action]
    if request.status != destination:
        if request.status not in allowed:
            raise HTTPException(409, "This action is not available in the current request state.")
        request.status = destination
        if action == "resume":
            from src.engine.applications import resumed_status
            from src.staff.operations import finish_takeover

            await finish_takeover(db, lead)
            lead.status = await resumed_status(db, lead)
        await write_audit_log(
            db,
            tenant_id=staff.tenant_id,
            actor=str(staff.id),
            action=f"human.{destination}",
            lead_id=lead.id,
            details={"request_id": str(request.id)},
        )
    await db.commit()
    return {"status": request.status}
