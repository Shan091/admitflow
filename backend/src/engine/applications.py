"""Explicit, encrypted, deterministic application collection in a private conversation."""

import json
import uuid
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import encrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import Application, Course, Lead, PaymentOrder, TelegramBot
from src.engine.contracts import Button, Reply
from src.telegram.callbacks import callback_data

FIELDS = ["full_name", "dob", "parent_name", "address", "previous_school"]
LABELS = [
    "full name",
    "date of birth (YYYY-MM-DD)",
    "parent or guardian name",
    "address",
    "previous school",
]


async def resumed_status(db: AsyncSession, lead: Lead) -> LeadStatus:
    application = await db.scalar(
        select(Application)
        .where(Application.tenant_id == lead.tenant_id, Application.lead_id == lead.id)
        .order_by(Application.submitted_at.desc(), Application.id)
        .limit(1)
    )
    if application is None:
        return LeadStatus.QUALIFYING if lead.current_batch_id else LeadStatus.DISCOVERING
    final = {
        ApplicationStatus.APPROVED: LeadStatus.ENROLLED,
        ApplicationStatus.REJECTED: LeadStatus.REJECTED,
        ApplicationStatus.WAITLISTED: LeadStatus.WAITLISTED,
        ApplicationStatus.UNDER_REVIEW: LeadStatus.UNDER_REVIEW,
    }
    if application.status in final:
        return final[application.status]
    paid = await db.scalar(
        select(PaymentOrder.id)
        .where(
            PaymentOrder.tenant_id == lead.tenant_id,
            PaymentOrder.application_id == application.id,
            PaymentOrder.status.in_([PaymentStatus.PAID, PaymentStatus.WAIVED]),
        )
        .limit(1)
    )
    course = await db.scalar(
        select(Course).where(Course.tenant_id == lead.tenant_id, Course.id == application.course_id)
    )
    return (
        LeadStatus.UNDER_REVIEW
        if paid or (course and course.application_fee == 0)
        else LeadStatus.PAYMENT_PENDING
    )


def action(label: str, target: str, lead: Lead, bot: TelegramBot) -> Button:
    return Button(text=label, data=callback_data("apply", target, lead.id, bot.id))


def prompt(draft: dict[str, Any], lead: Lead, bot: TelegramBot) -> Reply:
    missing = next((i for i, key in enumerate(FIELDS) if key not in draft["values"]), None)
    if missing is not None:
        return Reply(
            text=f"Please provide your {LABELS[missing]}. "
            "The institution can review your submitted information; it is encrypted in storage. "
            "Use /cancel to stop or /human for staff help.",
            buttons=[action("Cancel application", "cancel", lead, bot)],
        )
    summary = "\n".join(
        f"{label.capitalize()}: {draft['values'][key]}"
        for key, label in zip(FIELDS, LABELS, strict=True)
    )
    return Reply(
        text=f"Review your application:\n{summary}\n\nSubmit only if these details are correct. "
        "Submission is not admission or a seat reservation.",
        buttons=[
            action("Submit application", f"submit-{draft['nonce']}", lead, bot),
            action("Cancel application", "cancel", lead, bot),
        ],
    )


async def application_action(
    db: AsyncSession, lead: Lead, bot: TelegramBot, memory: dict[str, Any], target: str
) -> Reply:
    from src.engine.journey import qualify

    if target == "cancel":
        if not memory.get("application_draft"):
            return Reply(text="This application step has already ended.")
        memory.pop("application_draft", None)
        return await qualify(db, lead, bot, memory, "", [])
    if target == "start":
        existing = await db.scalar(
            select(Application).where(
                Application.tenant_id == lead.tenant_id,
                Application.lead_id == lead.id,
                Application.course_id == lead.current_course_id,
            )
        )
        if existing:
            return Reply(
                text="An application for this course is already submitted. "
                "Request staff review for changes."
            )
        outcome = await qualify(db, lead, bot, memory, "", [])
        if memory.get("eligibility", {}).get("outcome") != "eligible":
            return outcome
        memory["application_draft"] = {
            "course_id": str(lead.current_course_id),
            "batch_id": str(lead.current_batch_id),
            "nonce": uuid.uuid4().hex[:12],
            "values": {},
        }
        lead.status = LeadStatus.FORM_COLLECTING
        return prompt(memory["application_draft"], lead, bot)
    draft = memory.get("application_draft")
    if not draft:
        return Reply(
            text="This application step is already complete or has expired. "
            "Use /apply to check your application."
        )
    if (draft["course_id"], draft["batch_id"]) != (
        str(lead.current_course_id),
        str(lead.current_batch_id),
    ):
        memory.pop("application_draft", None)
        return Reply(
            text="Your course or batch changed. "
            "Start a new application after confirming eligibility."
        )
    if target != f"submit-{draft['nonce']}" or any(key not in draft["values"] for key in FIELDS):
        return prompt(draft, lead, bot)
    outcome = await qualify(db, lead, bot, memory, "", [])
    if memory.get("eligibility", {}).get("outcome") != "eligible":
        return outcome
    course = await db.scalar(
        select(Course).where(
            Course.id == lead.current_course_id, Course.tenant_id == lead.tenant_id
        )
    )
    if course is None:
        return Reply(text="This course is unavailable. Request staff review.")
    values = draft["values"]
    application = Application(
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        course_id=course.id,
        batch_id=lead.current_batch_id,
        full_name_enc=encrypt_pii(values["full_name"]),
        form_data_enc=encrypt_pii(json.dumps(values, ensure_ascii=False)),
    )
    db.add(application)
    await db.flush()
    memory.pop("application_draft", None)
    memory["application_id"] = str(application.id)
    lead.status = LeadStatus.PAYMENT_PENDING if course.application_fee else LeadStatus.UNDER_REVIEW
    await write_audit_log(
        db,
        tenant_id=lead.tenant_id,
        actor="conversation-engine",
        action="application.submitted",
        lead_id=lead.id,
        details={"application_id": str(application.id)},
    )
    return Reply(
        text="Your application is submitted for institutional review. "
        "This does not grant admission or reserve a seat. "
        + (
            "The configured application fee remains unpaid; "
            "review the fee before requesting a payment link."
            if course.application_fee
            else "No application fee is configured."
        ),
        buttons=(
            [
                Button(
                    text="Review application fee",
                    data=callback_data("pay", f"review-{application.id.hex}", lead.id, bot.id),
                )
            ]
            if course.application_fee
            else []
        ),
    )


async def collect_application(
    db: AsyncSession, lead: Lead, bot: TelegramBot, memory: dict[str, Any], text: str
) -> Reply:
    if text == "/cancel":
        return await application_action(db, lead, bot, memory, "cancel")
    draft = memory["application_draft"]
    if (draft["course_id"], draft["batch_id"]) != (
        str(lead.current_course_id),
        str(lead.current_batch_id),
    ):
        memory.pop("application_draft", None)
        return Reply(text="Your course or batch changed. Please start a new application.")
    missing = next((key for key in FIELDS if key not in draft["values"]), None)
    if missing is None:
        return prompt(draft, lead, bot)
    value = text.strip()
    if not value or value.startswith("/") or len(value) > (1000 if missing == "address" else 200):
        return prompt(draft, lead, bot)
    if missing == "dob":
        try:
            dob = date.fromisoformat(value)
            if not date(1900, 1, 1) <= dob <= date.today():
                raise ValueError("Date outside supported range")
            value = dob.isoformat()
        except ValueError:
            return Reply(text="Enter a valid past date of birth as YYYY-MM-DD, or use /cancel.")
    draft["values"][missing] = value
    lead.status = LeadStatus.FORM_COLLECTING
    return prompt(draft, lead, bot)
