"""Explicit, audited erasure and tenant-configured inactivity retention."""

import uuid
from datetime import UTC, datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from sqlalchemy import delete, exists, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.audit import write_audit_log
from src.db.models import (
    AuditLog,
    ConversationEvent,
    ConversationMemory,
    ConversationReply,
    Institution,
    IntegrationEvent,
    Lead,
    LeadFact,
    Message,
    OutboundMessage,
    PaymentOrder,
    WebhookDelivery,
)
from src.db.session import get_sessionmaker
from src.staff.auth import Db, Staff, require_admin, require_browser_write, require_staff

router = APIRouter(prefix="/api/staff", tags=["applicant privacy"])


class EraseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confirm_id: uuid.UUID


async def in_flight(db: AsyncSession, tenant_id: uuid.UUID, lead_id: uuid.UUID) -> bool:
    checks = [
        select(OutboundMessage.id).where(
            OutboundMessage.tenant_id == tenant_id,
            OutboundMessage.lead_id == lead_id,
            OutboundMessage.status == "sending",
        ),
        select(ConversationReply.id)
        .join(
            ConversationEvent,
            (ConversationEvent.id == ConversationReply.event_id)
            & (ConversationEvent.tenant_id == ConversationReply.tenant_id),
        )
        .where(
            ConversationReply.tenant_id == tenant_id,
            ConversationEvent.lead_id == lead_id,
            ConversationReply.status == "sending",
        ),
        select(PaymentOrder.id).where(
            PaymentOrder.tenant_id == tenant_id,
            PaymentOrder.lead_id == lead_id,
            PaymentOrder.creation_state == "creating",
        ),
        select(WebhookDelivery.id)
        .join(
            IntegrationEvent,
            (IntegrationEvent.id == WebhookDelivery.event_id)
            & (IntegrationEvent.tenant_id == WebhookDelivery.tenant_id),
        )
        .where(
            WebhookDelivery.tenant_id == tenant_id,
            IntegrationEvent.lead_id == lead_id,
            WebhookDelivery.status == "sending",
        ),
    ]
    return bool(await db.scalar(select(or_(*(exists(statement) for statement in checks)))))


async def erase(
    db: AsyncSession, lead: Lead, *, actor: str, reason: Literal["staff_request"]
) -> uuid.UUID:
    # Caller owns the lead row lock. Send/payment claims use the same first lock.
    if await in_flight(db, lead.tenant_id, lead.id):
        raise HTTPException(
            409, "A delivery or payment operation is in progress. Retry after it finishes."
        )
    tenant_id, lead_id = lead.tenant_id, lead.id
    # Preserve an anonymous action history without a subject ID or linked details.
    await db.execute(
        update(AuditLog)
        .where(AuditLog.tenant_id == tenant_id, AuditLog.lead_id == lead_id)
        .values(lead_id=None, details=None)
    )
    await db.execute(delete(Lead).where(Lead.tenant_id == tenant_id, Lead.id == lead_id))
    receipt = await write_audit_log(
        db, tenant_id=tenant_id, actor=actor, action="privacy.deleted", details={"reason": reason}
    )
    return receipt.id


@router.delete("/leads/{lead_id}", dependencies=[Depends(require_browser_write)])
async def erase_inquiry(
    lead_id: uuid.UUID, payload: EraseRequest, staff: Staff, db: Db, request: Request
) -> dict[str, str]:
    require_admin(staff)
    if payload.confirm_id != lead_id:
        raise HTTPException(422, "The confirmation must match the selected inquiry.")
    lead = await db.scalar(
        select(Lead).where(Lead.tenant_id == staff.tenant_id, Lead.id == lead_id).with_for_update()
    )
    if lead is None:
        raise HTTPException(404, "Inquiry not found.")
    require_admin(await require_staff(request, db))
    receipt = await erase(db, lead, actor=str(staff.id), reason="staff_request")
    await db.commit()
    return {"status": "deleted", "receipt_id": str(receipt)}


async def purge_retained(*, now: datetime | None = None) -> int:
    """Expire inactive dialogue; applications, payments and CRM records survive."""
    now = now or datetime.now(UTC)
    total = 0
    sessions = get_sessionmaker()
    async with sessions() as db:
        tenants = (
            await db.scalars(select(Institution.id).where(Institution.retention_days.is_not(None)))
        ).all()
    for tenant_id in tenants:
        async with sessions() as db:
            institution = await db.scalar(
                select(Institution)
                .where(Institution.id == tenant_id)
                .with_for_update(key_share=True)
            )
            days = institution.retention_days if institution else None
            if days is None or days < 1:
                continue
            cutoff = now - timedelta(days=days)
            # Lock and recheck activity against the actual communication dates,
            # not updated_at (staff reads/settings/reindexing must not reset policy).
            activity = func.greatest(Lead.created_at, Lead.last_inbound_at, Lead.last_outbound_at)
            leads = (
                await db.scalars(
                    select(Lead)
                    .where(
                        Lead.tenant_id == tenant_id,
                        activity < cutoff,
                        or_(
                            Lead.conversation_purged_at.is_(None),
                            activity > Lead.conversation_purged_at,
                        ),
                        ~exists(
                            select(ConversationEvent.id).where(
                                ConversationEvent.tenant_id == tenant_id,
                                ConversationEvent.lead_id == Lead.id,
                                ConversationEvent.status == "queued",
                            )
                        ),
                    )
                    .order_by(Lead.created_at, Lead.id)
                    .limit(100)
                    .with_for_update(skip_locked=True)
                )
            ).all()
            for lead in leads:
                pending = await db.scalar(
                    select(ConversationEvent.id)
                    .where(
                        ConversationEvent.tenant_id == tenant_id,
                        ConversationEvent.lead_id == lead.id,
                        ConversationEvent.status == "queued",
                    )
                    .limit(1)
                )
                if pending:
                    continue
                if await in_flight(db, tenant_id, lead.id):
                    continue
                # History expiry is narrower than explicit full inquiry erasure.
                # Queued side effects cannot outlive the cleared dialogue consent.
                await db.execute(
                    update(PaymentOrder)
                    .where(
                        PaymentOrder.tenant_id == tenant_id,
                        PaymentOrder.lead_id == lead.id,
                        PaymentOrder.creation_state == "queued",
                    )
                    .values(
                        creation_state="failed",
                        last_error="conversation_expired",
                        next_attempt_at=None,
                    )
                )
                for model in (
                    ConversationEvent,
                    ConversationMemory,
                    LeadFact,
                    Message,
                    OutboundMessage,
                ):
                    await db.execute(
                        delete(model).where(model.tenant_id == tenant_id, model.lead_id == lead.id)
                    )
                await db.execute(
                    delete(IntegrationEvent).where(
                        IntegrationEvent.tenant_id == tenant_id,
                        IntegrationEvent.lead_id == lead.id,
                        IntegrationEvent.kind.in_(
                            [
                                "lead.stage_changed",
                                "human.requested",
                                "staff.draft_generated",
                                "delivery.attention",
                            ]
                        ),
                    )
                )
                lead.conversation_purged_at = now
                lead.followup_consent = False
                lead.followup_due_at = None
                lead.followup_consent_updated_at = now
                await write_audit_log(
                    db,
                    tenant_id=tenant_id,
                    lead_id=lead.id,
                    actor="retention-scheduler",
                    action="conversation.history_expired",
                )
                total += 1
            await db.commit()
    return total
