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

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.audit import AuditLog


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
