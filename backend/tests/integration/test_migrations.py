"""Migration + schema integration tests against real Postgres.

Spins up ``pgvector/pgvector:pg16`` with testcontainers, so these need a running Docker
daemon. They are marked ``integration`` and excluded from the default gate;
run explicitly with ``uv run pytest -m integration``. If Docker is unreachable
the module skips rather than fails.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterator

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.settings import get_settings
from src.db.session import get_engine, get_sessionmaker

pytestmark = pytest.mark.integration

try:  # testcontainers import is cheap; the daemon check happens on start.
    from testcontainers.community.postgres import PostgresContainer
except ImportError:  # pragma: no cover - dependency always present in dev
    PostgresContainer = None  # type: ignore[assignment,misc]


@pytest.fixture(scope="module")
def pg_url(monkeypatch_session: pytest.MonkeyPatch) -> Iterator[str]:
    """Start Postgres, point settings at it, yield the asyncpg URL."""
    if PostgresContainer is None:
        pytest.skip("testcontainers not installed")
    try:
        container = PostgresContainer("pgvector/pgvector:pg16", driver="asyncpg")
        container.start()
    except Exception as exc:  # noqa: BLE001 - Docker down/unavailable -> skip, don't fail
        pytest.skip(f"Docker/Postgres unavailable: {exc}")

    url = container.get_connection_url()
    monkeypatch_session.setenv("DATABASE_URL", url)
    # Rebuild the cached settings + engine so they see the container URL.
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_sessionmaker.cache_clear()
    try:
        yield url
    finally:
        container.stop()
        get_settings.cache_clear()
        get_engine.cache_clear()
        get_sessionmaker.cache_clear()


@pytest.fixture(scope="module")
def monkeypatch_session() -> Iterator[pytest.MonkeyPatch]:
    mp = pytest.MonkeyPatch()
    yield mp
    mp.undo()


def _alembic_config() -> Config:
    cfg = Config("alembic.ini")
    return cfg


def test_migration_applies_up_and_down(pg_url: str) -> None:
    """The tier requirement: alembic upgrade head then downgrade base, both clean."""
    cfg = _alembic_config()
    command.upgrade(cfg, "head")

    # All expected tables exist after upgrade.
    async def _tables() -> set[str]:
        engine = create_async_engine(pg_url)
        try:
            async with engine.connect() as conn:
                names = await conn.run_sync(
                    lambda sync_conn: set(sa.inspect(sync_conn).get_table_names())
                )
            return names
        finally:
            await engine.dispose()

    tables = asyncio.run(_tables())
    assert {"institutions", "leads", "courses", "payment_orders"} <= tables

    # And it reverses cleanly.
    command.downgrade(cfg, "base")
    remaining = asyncio.run(_tables())
    assert "institutions" not in remaining
    assert "leads" not in remaining


def test_password_setup_downgrade_revokes_restricted_access(pg_url: str) -> None:
    import uuid
    from datetime import UTC, datetime, timedelta

    from src.db.enums import StaffRole
    from src.db.models import Institution, StaffSession, StaffUser

    cfg = _alembic_config()
    command.upgrade(cfg, "head")
    tenant_id = uuid.uuid4()
    pending, normal = uuid.uuid4(), uuid.uuid4()

    async def seed():
        engine = create_async_engine(pg_url)
        async with engine.begin() as db:
            await db.execute(
                sa.insert(Institution).values(id=tenant_id, name="Synthetic rollback institution")
            )
            for user_id, restricted in ((pending, True), (normal, False)):
                await db.execute(
                    sa.insert(StaffUser).values(
                        id=user_id,
                        tenant_id=tenant_id,
                        email=f"{user_id}@example.test",
                        hashed_password="synthetic-unusable-hash",
                        role=StaffRole.AGENT,
                        is_active=True,
                        must_change_password=restricted,
                    )
                )
                await db.execute(
                    sa.insert(StaffSession).values(
                        tenant_id=tenant_id,
                        user_id=user_id,
                        token_hash=uuid.uuid4().hex * 2,
                        expires_at=datetime.now(UTC) + timedelta(hours=1),
                    )
                )
        await engine.dispose()

    asyncio.run(seed())
    command.downgrade(cfg, "6dd017583606")

    async def inspect():
        engine = create_async_engine(pg_url)
        async with engine.begin() as db:
            rows = dict(
                (
                    await db.execute(
                        sa.select(StaffUser.id, StaffUser.is_active).where(
                            StaffUser.tenant_id == tenant_id
                        )
                    )
                ).all()
            )
            assert rows == {pending: False, normal: True}
            remaining = list(
                (
                    await db.execute(
                        sa.select(StaffSession.user_id).where(StaffSession.tenant_id == tenant_id)
                    )
                ).scalars()
            )
            assert remaining == [normal]
        await engine.dispose()

    asyncio.run(inspect())
    command.upgrade(cfg, "head")

    async def clean():
        engine = create_async_engine(pg_url)
        async with engine.begin() as db:
            await db.execute(sa.delete(Institution).where(Institution.id == tenant_id))
        await engine.dispose()

    asyncio.run(clean())


def test_tenant_fk_and_unique_constraints_hold(pg_url: str) -> None:
    """Round-trip an Institution -> Lead; the tenant FK + phone uniqueness bind."""
    from src.db.enums import LeadStatus
    from src.db.models import Institution, Lead

    cfg = _alembic_config()
    command.upgrade(cfg, "head")

    async def _roundtrip() -> None:
        sessionmaker = get_sessionmaker()
        try:
            async with sessionmaker() as session:
                inst = Institution(name="Test Inst", whatsapp_phone_number_id="pn-1")
                session.add(inst)
                await session.flush()

                lead = Lead(
                    tenant_id=inst.id,
                    phone_hash="hash-1",
                    phone_enc="cipher-1",
                    status=LeadStatus.NEW,
                )
                session.add(lead)
                await session.commit()

                # Duplicate (tenant_id, phone_hash) must violate the unique constraint.
                dup = Lead(
                    tenant_id=inst.id,
                    phone_hash="hash-1",
                    phone_enc="cipher-2",
                    status=LeadStatus.NEW,
                )
                session.add(dup)
                with pytest.raises(sa.exc.IntegrityError):
                    await session.commit()
        finally:
            await get_engine().dispose()

    asyncio.run(_roundtrip())
    command.downgrade(cfg, "base")
