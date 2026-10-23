"""Integration test: Discovery node fetches courses correctly."""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import Iterator
from unittest.mock import AsyncMock

import pytest
from alembic import command
from alembic.config import Config

from src.core.settings import get_settings
from src.db.enums import LeadStatus
from src.db.models import Batch, Course, Institution
from src.db.session import get_engine, get_sessionmaker
from src.engine.nodes.discovery import present_courses
from src.engine.state import EngineState

pytestmark = pytest.mark.integration

try:
    from testcontainers.community.postgres import PostgresContainer
except ImportError:
    PostgresContainer = None  # type: ignore[assignment,misc]


@pytest.fixture(scope="module")
def migrated_db() -> Iterator[None]:
    """Start Postgres, point settings at it, migrate to head; tear down after."""
    if PostgresContainer is None:
        pytest.skip("testcontainers not installed")
    try:
        container = PostgresContainer("pgvector/pgvector:pg16", driver="asyncpg")
        container.start()
    except Exception as exc:
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


@pytest.mark.asyncio
async def test_present_courses_with_available_batches(migrated_db: None) -> None:
    sessionmaker = get_sessionmaker()
    tenant_id = uuid.uuid4()
    lead_id = uuid.uuid4()

    async with sessionmaker() as session:
        session.add(Institution(id=tenant_id, name="Test Inst", whatsapp_phone_number_id="pn-disc"))

        # Course 1: Active with seats
        c1 = Course(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            name="B.Tech CS",
            is_active=True,
            application_fee=1000,
        )
        b1 = Batch(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            course_id=c1.id,
            name="Fall",
            capacity=50,
            seats_remaining=10,
            is_active=True,
        )

        # Course 2: Active but NO seats
        c2 = Course(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            name="B.Tech IT",
            is_active=True,
            application_fee=1000,
        )
        b2 = Batch(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            course_id=c2.id,
            name="Fall",
            capacity=50,
            seats_remaining=0,
            is_active=True,
        )

        # Course 3: Inactive
        c3 = Course(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            name="B.Tech EE",
            is_active=False,
            application_fee=1000,
        )
        b3 = Batch(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            course_id=c3.id,
            name="Fall",
            capacity=50,
            seats_remaining=10,
            is_active=True,
        )

        session.add_all([c1, c2, c3, b1, b2, b3])
        await session.commit()

    async with sessionmaker() as session:
        state = EngineState(lead_id=lead_id, tenant_id=tenant_id, status=LeadStatus.NEW)
        mock_sender = AsyncMock()

        new_state = await present_courses(state, session, mock_sender, "919876543210")

        # Should transition to DISCOVERING
        assert new_state.status == LeadStatus.DISCOVERING

        # Should only send B.Tech CS (the only active course with seats)
        mock_sender.send_buttons.assert_called_once()
        call_kwargs = mock_sender.send_buttons.call_args.kwargs
        assert call_kwargs["to"] == "919876543210"
        assert len(call_kwargs["buttons"]) == 1
        assert call_kwargs["buttons"][0]["title"] == "B.Tech CS"
