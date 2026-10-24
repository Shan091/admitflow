"""Atomic reset removes dummy records while preserving access and polling state."""

import asyncio
import json
from pathlib import Path

import pytest
from sqlalchemy import delete, func, select

from src.core.security import encrypt_pii
from src.db.models import Course, Document, Institution, Lead, StaffUser, TelegramBot
from src.scripts.replace_demo_catalogue import NAME, PublicCatalogue, replace
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration


def test_reset_is_atomic_and_preserves_administrator_and_bot(workspace, monkeypatch):
    raw = json.loads(
        (Path(__file__).parents[2] / "data/jain-kochi/catalogue.json").read_text(encoding="utf-8")
    )
    raw["programmes"] = raw["programmes"][:2]
    catalogue = PublicCatalogue.model_validate(raw)

    async def exercise():
        from types import SimpleNamespace
        from unittest.mock import AsyncMock

        from src.scripts import seed_demo

        first, second = workspace["tenants"]
        async with workspace["sessions"]() as db:
            institution = await db.get(Institution, first)
            institution.name, institution.slug = "AdmitFlow Demo Institute", "demo"
            other = await db.get(Institution, second)
            other.name = "AdmitFlow Synthetic Demo Institution"
            await db.execute(delete(StaffUser).where(StaffUser.tenant_id == second))
            await db.execute(delete(StaffUser).where(StaffUser.email == "agent@example.test"))
            admin = await db.scalar(select(StaffUser).where(StaffUser.tenant_id == first))
            admin_id, password = admin.id, admin.hashed_password
            bot = TelegramBot(
                tenant_id=first,
                telegram_bot_id=12345,
                token_enc=encrypt_pii("synthetic"),
                last_update_id=99,
            )
            db.add_all(
                [
                    bot,
                    Lead(tenant_id=first),
                    Course(tenant_id=first, name="Old dummy", application_fee=123),
                ]
            )
            await db.commit()
            bot_id = bot.id
        async with workspace["sessions"]() as db:
            with pytest.raises(ValueError):
                await replace(db, "demo", catalogue, [])
            assert await db.scalar(select(func.count()).select_from(Lead)) == 1
            await replace(db, "demo", catalogue, [[0.0] * 1536 for _ in range(3)])
            await db.rollback()
            assert await db.scalar(select(func.count()).select_from(Lead)) == 1
        async with workspace["sessions"]() as db:
            await replace(db, "demo", catalogue, [[0.0] * 1536 for _ in range(3)])
            await db.commit()
        async with workspace["sessions"]() as db:
            assert await db.scalar(select(func.count()).select_from(Lead)) == 0
            assert await db.scalar(select(func.count()).select_from(Institution)) == 1
            assert (await db.get(Institution, first)).name == NAME
            assert (await db.get(StaffUser, admin_id)).hashed_password == password
            assert (await db.get(TelegramBot, bot_id)).last_update_id == 99
            assert await db.scalar(select(func.count()).select_from(Document)) == 3
            assert all(c.is_reference for c in (await db.scalars(select(Course))).all())
        monkeypatch.setattr(seed_demo, "get_sessionmaker", lambda: workspace["sessions"])
        monkeypatch.setattr(
            seed_demo, "get_settings", lambda: SimpleNamespace(telegram_institution_code="demo")
        )
        monkeypatch.setattr(seed_demo, "get_engine", lambda: SimpleNamespace(dispose=AsyncMock()))
        await seed_demo.seed()
        async with workspace["sessions"]() as db:
            assert await db.scalar(select(func.count()).select_from(Course)) == 2

    asyncio.run(exercise())
