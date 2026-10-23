"""Unit test for the audit-log write helper.

The real INSERT path (JSONB, server-default timestamp) is covered by the
integration test; here we assert the helper builds the right row and stages it
on the caller's session without needing a database.
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

from src.db.audit import write_audit_log
from src.db.models.audit import AuditLog


async def test_write_audit_log_stages_and_flushes_entry() -> None:
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock()

    tenant_id = uuid.uuid4()
    lead_id = uuid.uuid4()
    entry = await write_audit_log(
        session,
        tenant_id=tenant_id,
        action="lead.status_changed",
        actor="engine",
        lead_id=lead_id,
        details={"from": "new", "to": "discovering"},
    )

    assert isinstance(entry, AuditLog)
    assert entry.tenant_id == tenant_id
    assert entry.action == "lead.status_changed"
    assert entry.actor == "engine"
    assert entry.lead_id == lead_id
    assert entry.details == {"from": "new", "to": "discovering"}
    session.add.assert_called_once_with(entry)
    session.flush.assert_awaited_once()
    # The commit is the caller's — the helper must not swallow the unit of work.
    session.commit.assert_not_called()


async def test_write_audit_log_defaults_optional_fields() -> None:
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock()

    entry = await write_audit_log(
        session,
        tenant_id=uuid.uuid4(),
        action="data.exported",
        actor="admin@test",
    )

    assert entry.lead_id is None
    assert entry.details is None
