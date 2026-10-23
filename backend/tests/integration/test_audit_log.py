"""Integration test: ``write_audit_log`` persists to real Postgres and reads back.

Spins up ``pgvector/pgvector:pg16`` with testcontainers (needs a running Docker daemon),
runs the Alembic migrations, then round-trips an audit row. Marked
``integration`` and excluded from the default gate; run with
``uv run pytest -m integration``. Skips (does not fail) if Docker is unreachable.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import select

from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import AuditLog, Institution
from src.db.session import get_engine, get_sessionmaker

pytestmark = pytest.mark.integration

try:  # testcontainers import is cheap; the daemon check happens on start.
    from testcontainers.community.postgres import PostgresContainer
except ImportError:  # pragma: no cover - dependency always present in dev
    PostgresContainer = None  # type: ignore[assignment,misc]


@pytest.fixture(scope="module")
def migrated_db() -> Iterator[None]:
    """Start Postgres, point settings at it, migrate to head; tear down after."""
    if PostgresContainer is None:
        pytest.skip("testcontainers not installed")
    try:
        container = PostgresContainer("pgvector/pgvector:pg16", driver="asyncpg")
        container.start()
    except Exception as exc:  # noqa: BLE001 - Docker down/unavailable -> skip, don't fail
        pytest.skip(f"Docker/Postgres unavailable: {exc}")

    mp = pytest.MonkeyPatch()
    mp.setenv("DATABASE_URL", container.get_connection_url())
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_sessionmaker.cache_clear()
    try:
        command.upgrade(Config("alembic.ini"), "head")
        yield
    finally:
        command.downgrade(Config("alembic.ini"), "base")
        asyncio.run(get_engine().dispose())
        container.stop()
        mp.undo()
        get_settings.cache_clear()
        get_engine.cache_clear()
        get_sessionmaker.cache_clear()


def test_write_audit_log_persists_and_reads_back(migrated_db: None) -> None:
    async def _run() -> None:
        sessionmaker = get_sessionmaker()
        inst_id = uuid.uuid4()
        async with sessionmaker() as session:
            session.add(
                Institution(id=inst_id, name="Test Inst", whatsapp_phone_number_id="pn-audit")
            )
            await session.flush()
            entry = await write_audit_log(
                session,
                tenant_id=inst_id,
                action="data.deleted",
                actor="admin@test",
                details={"reason": "dsr"},
            )
            assert entry.id is not None
            entry_id = entry.id
            await session.commit()

        async with sessionmaker() as session:
            row = (
                await session.execute(select(AuditLog).where(AuditLog.id == entry_id))
            ).scalar_one()
            assert row.tenant_id == inst_id
            assert row.action == "data.deleted"
            assert row.actor == "admin@test"
            assert row.details == {"reason": "dsr"}
            assert row.created_at is not None  # server_default now() populated

    asyncio.run(_run())
