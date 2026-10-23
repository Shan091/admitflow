"""Commit minimal events/outbox rows in the source audit transaction."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Connection, insert, select
from sqlalchemy.orm import Mapper

from src.db.enums import LeadStatus
from src.db.models import AuditLog, IntegrationEvent, WebhookDelivery, WebhookEndpoint

KINDS = frozenset(
    {
        "application.submitted",
        "application.approved",
        "application.rejected",
        "application.waitlisted",
        "application.under_review",
        "payment.confirmed",
        "payment.fee_waived",
        "payment.link_created",
        "human.requested",
        "staff.draft_generated",
        "delivery.attention",
        "lead.stage_changed",
        "knowledge.ready",
    }
)


def capture_event(_mapper: Mapper[AuditLog], connection: Connection, audit: AuditLog) -> None:
    if audit.action not in KINDS:
        return
    state = (audit.details or {}).get("to") if audit.action == "lead.stage_changed" else None
    if state not in {item.value for item in LeadStatus}:
        state = None
    notification = {
        "payment.confirmed": "payment",
        "staff.draft_generated": "draft",
        "delivery.attention": "delivery",
    }.get(audit.action)
    if state == LeadStatus.ADMISSION_READY.value:
        notification = "qualified"
    event_id = audit.id
    connection.execute(
        insert(IntegrationEvent).values(
            id=event_id,
            tenant_id=audit.tenant_id,
            lead_id=audit.lead_id,
            kind=audit.action,
            state=state,
            notification=notification,
            created_at=datetime.now(UTC),
        )
    )
    endpoint = connection.execute(
        select(WebhookEndpoint.id, WebhookEndpoint.generation).where(
            WebhookEndpoint.tenant_id == audit.tenant_id, WebhookEndpoint.enabled.is_(True)
        )
    ).first()
    if endpoint:
        connection.execute(
            insert(WebhookDelivery).values(
                id=uuid.uuid4(),
                tenant_id=audit.tenant_id,
                event_id=event_id,
                endpoint_id=endpoint.id,
                generation=endpoint.generation,
                status="queued",
                attempts=0,
            )
        )
