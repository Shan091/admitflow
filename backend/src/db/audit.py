"""Audit-log write helper.

:func:`write_audit_log` is the one path significant actions (state changes,
payments, data deletion, human takeover — SPEC §12) take into the append-only
``audit_logs`` table. It stages the row on the caller's session and flushes so
the generated id/timestamp are available, but leaves the commit to the caller
(one unit of work per turn).

``details`` is free-form JSONB and must never carry raw PII — reference records
by id (``lead_id``), per security-and-production.md.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import event, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.db.enums import LeadStatus
from src.db.models.audit import AuditLog
from src.db.models.lead import Lead
from src.integrations.events import capture_event


def record_stage_changes(session: Session, _flush_context: Any, _instances: Any) -> None:
    """Record persisted ORM transitions atomically; never infer an earlier stage."""
    for entity in list(session.dirty):
        if not isinstance(entity, Lead):
            continue
        history = inspect(entity).attrs.status.history
        if not history.has_changes() or not history.added:
            continue
        destination = history.added[0]
        if not isinstance(destination, LeadStatus):
            continue
        previous = history.deleted[0] if history.deleted else None
        session.add(
            AuditLog(
                tenant_id=entity.tenant_id,
                lead_id=entity.id,
                actor="domain-state",
                action="lead.stage_changed",
                details={
                    "from": previous.value if isinstance(previous, LeadStatus) else None,
                    "to": destination.value,
                },
            )
        )


event.listen(Session, "before_flush", record_stage_changes)

event.listen(AuditLog, "after_insert", capture_event)


async def write_audit_log(
    session: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    action: str,
    actor: str,
    lead_id: uuid.UUID | None = None,
    details: dict[str, Any] | None = None,
) -> AuditLog:
    """Append one entry to ``audit_logs`` on ``session``; return it flushed, not committed."""
    entry = AuditLog(
        tenant_id=tenant_id,
        action=action,
        actor=actor,
        lead_id=lead_id,
        details=details,
    )
    session.add(entry)
    await session.flush()
    return entry
