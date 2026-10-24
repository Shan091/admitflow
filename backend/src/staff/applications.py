"""Audited application inspection and deterministic administrative review."""

import json
import uuid
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from src.core.demo_admissions import demo_fee
from src.core.security import decrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import Application, Batch, Course, Lead, PaymentOrder
from src.engine.contracts import Reply
from src.staff.auth import Db, Staff, require_admin, require_browser_write
from src.telegram.outbound import enqueue_outbound

router = APIRouter(prefix="/api/staff/applications", tags=["applications"])


async def owned(db: Db, staff: Staff, application_id: uuid.UUID) -> Application:
    application = await db.scalar(
        select(Application).where(
            Application.tenant_id == staff.tenant_id, Application.id == application_id
        )
    )
    if application is None:
        raise HTTPException(404, "Application not found.")
    return application


@router.get("")
async def applications(
    staff: Staff,
    db: Db,
    offset: int = Query(default=0, ge=0),
    status: ApplicationStatus | None = None,
) -> list[dict[str, Any]]:
    statement = (
        select(Application, Course.name)
        .join(
            Course,
            (Course.id == Application.course_id) & (Course.tenant_id == Application.tenant_id),
        )
        .where(Application.tenant_id == staff.tenant_id)
    )
    if status:
        statement = statement.where(Application.status == status)
    rows = (
        await db.execute(
            statement.order_by(Application.submitted_at.desc(), Application.id)
            .offset(offset)
            .limit(50)
        )
    ).all()
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="staff.applications_viewed"
    )
    await db.commit()
    return [
        {
            "id": str(application.id),
            "lead_id": str(application.lead_id),
            "course": course_name,
            "status": application.status.value,
            "is_demo": application.is_demo,
            "submitted_at": application.submitted_at.isoformat(),
        }
        for application, course_name in rows
    ]


@router.get("/{application_id}")
async def detail(application_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, Any]:
    application = await owned(db, staff, application_id)
    form = (
        json.loads(decrypt_pii(application.form_data_enc))
        if application.form_data_enc
        else {
            "full_name": decrypt_pii(application.full_name_enc),
            "dob": application.dob.isoformat() if application.dob else None,
            "parent_name": decrypt_pii(application.parent_name_enc)
            if application.parent_name_enc
            else None,
            "address": decrypt_pii(application.address_enc) if application.address_enc else None,
            "previous_school": application.previous_school,
        }
    )
    payment_states = (
        await db.scalars(
            select(PaymentOrder.status).where(
                PaymentOrder.tenant_id == staff.tenant_id,
                PaymentOrder.application_id == application.id,
            )
        )
    ).all()
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="staff.application_viewed",
        lead_id=application.lead_id,
        details={"application_id": str(application.id)},
    )
    await db.commit()
    return {
        "id": str(application.id),
        "lead_id": str(application.lead_id),
        "course_id": str(application.course_id),
        "batch_id": str(application.batch_id) if application.batch_id else None,
        "status": application.status.value,
        "is_demo": application.is_demo,
        "form": form,
        "payments": [status.value for status in payment_states],
    }


@router.post("/{application_id}/{decision}", dependencies=[Depends(require_browser_write)])
async def review(
    application_id: uuid.UUID,
    decision: Literal["approve", "waitlist", "reject"],
    staff: Staff,
    db: Db,
) -> dict[str, str]:
    require_admin(staff)
    application = await owned(db, staff, application_id)
    # Lead first, application next, batch last: same serialization order as the engine.
    lead = await db.scalar(
        select(Lead)
        .where(Lead.id == application.lead_id, Lead.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    if lead is None:
        raise HTTPException(404, "Inquiry not found.")
    await db.refresh(application, with_for_update=True)
    destination = {
        "approve": ApplicationStatus.APPROVED,
        "waitlist": ApplicationStatus.WAITLISTED,
        "reject": ApplicationStatus.REJECTED,
    }[decision]
    if application.status == destination:
        return {"status": destination.value}
    if application.status in {ApplicationStatus.APPROVED, ApplicationStatus.REJECTED}:
        raise HTTPException(409, "This application already has a final decision.")
    if decision == "approve":
        course = await db.scalar(
            select(Course).where(
                Course.id == application.course_id,
                Course.tenant_id == staff.tenant_id,
                Course.is_active.is_(True),
            )
        )
        if course is None:
            raise HTTPException(409, "This course is unavailable.")
        if application.is_demo:
            if await demo_fee(db, course) is None or application.batch_id is not None:
                raise HTTPException(
                    409, "Demo approvals require the enabled test-only configuration."
                )
            paid = await db.scalar(
                select(PaymentOrder.id).where(
                    PaymentOrder.tenant_id == staff.tenant_id,
                    PaymentOrder.application_id == application.id,
                    PaymentOrder.lead_id == lead.id,
                    PaymentOrder.course_id == course.id,
                    PaymentOrder.is_demo.is_(True),
                    PaymentOrder.status == PaymentStatus.PAID,
                    PaymentOrder.razorpay_payment_id.is_not(None),
                    PaymentOrder.amount >= 100,
                    PaymentOrder.currency == "INR",
                )
            )
            if paid is None:
                raise HTTPException(
                    409, "A confirmed Razorpay test payment is required before demo approval."
                )
        else:
            if course.is_reference:
                raise HTTPException(
                    409, "This reference programme cannot grant university admission."
                )
            paid = await db.scalar(
                select(PaymentOrder.id).where(
                    PaymentOrder.tenant_id == staff.tenant_id,
                    PaymentOrder.application_id == application.id,
                    PaymentOrder.status.in_([PaymentStatus.PAID, PaymentStatus.WAIVED]),
                    PaymentOrder.is_demo.is_(False),
                )
            )
            if course.application_fee and paid is None:
                raise HTTPException(409, "The configured application fee is not paid.")
            batch = await db.scalar(
                select(Batch)
                .where(
                    Batch.id == application.batch_id,
                    Batch.course_id == course.id,
                    Batch.tenant_id == staff.tenant_id,
                    Batch.is_active.is_(True),
                )
                .with_for_update()
            )
            if batch is None or batch.seats_remaining <= 0:
                raise HTTPException(409, "No available seat in the selected batch.")
            batch.seats_remaining -= 1
        lead.status = LeadStatus.ENROLLED
    else:
        lead.status = LeadStatus.WAITLISTED if decision == "waitlist" else LeadStatus.REJECTED
    application.status = destination
    if application.is_demo:
        await enqueue_outbound(
            db,
            tenant_id=staff.tenant_id,
            lead_id=lead.id,
            kind="demo_application_decision",
            dedup_key=f"demo-decision:{application.id}:{destination.value}",
            reply=Reply(
                text=f"Staff have {destination.value.replace('_', ' ')} your demo application. "
                "This completes a demonstration review; it is not a university admission decision "
                "and no university seat has been allocated."
            ),
        )
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action=f"application.{destination.value}",
        lead_id=lead.id,
        details={"application_id": str(application.id)},
    )
    await db.commit()
    return {"status": destination.value}
