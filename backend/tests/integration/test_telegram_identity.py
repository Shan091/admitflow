"""Exercise Telegram tenant/identity constraints and safe migration rollback."""

import asyncio
import uuid
from collections.abc import Iterator

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.community.postgres import PostgresContainer

from src.core.security import decrypt_pii, encrypt_pii
from src.core.settings import Settings
from src.db.enums import LeadStatus
from src.db.models import Institution, Lead, TelegramBot, TelegramIdentity
from src.telegram.identity import hash_telegram_identifier

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def identity_database() -> Iterator[str]:
    """Use a disposable pgvector database; never mutate the demo database."""
    with PostgresContainer("pgvector/pgvector:pg16", driver="asyncpg") as container:
        url = container.get_connection_url()
        with pytest.MonkeyPatch.context() as mp:
            settings = Settings(
                _env_file=None,
                database_url=url,
                pii_encryption_key=Fernet.generate_key().decode(),
                phone_hash_key="synthetic-identity-key",
            )
            mp.setattr("src.core.settings.get_settings", lambda: settings)
            mp.setattr("src.core.security.get_settings", lambda: settings)
            mp.setattr("src.telegram.identity.get_settings", lambda: settings)
            command.upgrade(Config("alembic.ini"), "head")
            yield url
            command.downgrade(Config("alembic.ini"), "base")


def test_private_identities_are_encrypted_unique_and_tenant_bound(identity_database: str) -> None:
    async def exercise() -> None:
        engine = create_async_engine(identity_database)
        try:
            async with async_sessionmaker(engine, expire_on_commit=False)() as session:
                # Roll back all synthetic rows after verifying constraints.
                async with session.begin():
                    first = Institution(name="First synthetic institution")
                    second = Institution(name="Second synthetic institution")
                    session.add_all([first, second])
                    await session.flush()
                    first_lead = Lead(tenant_id=first.id, status=LeadStatus.NEW)
                    second_lead = Lead(tenant_id=second.id, status=LeadStatus.NEW)
                    bot = TelegramBot(
                        tenant_id=first.id,
                        telegram_bot_id=123456789,
                        token_enc=encrypt_pii("synthetic-token"),
                    )
                    session.add_all([first_lead, second_lead, bot])
                    await session.flush()

                    def identity(
                        tenant_id: uuid.UUID, lead_id: uuid.UUID, user_id: int
                    ) -> TelegramIdentity:
                        return TelegramIdentity(
                            tenant_id=tenant_id,
                            bot_id=bot.id,
                            lead_id=lead_id,
                            user_hash=hash_telegram_identifier(
                                tenant_id, 123456789, "user", user_id
                            ),
                            chat_hash=hash_telegram_identifier(
                                tenant_id, 123456789, "chat", user_id
                            ),
                            user_id_enc=encrypt_pii(str(user_id)),
                            chat_id_enc=encrypt_pii(str(user_id)),
                        )

                    valid = identity(first.id, first_lead.id, 8000000000000)
                    session.add(valid)
                    await session.flush()
                    assert first_lead.phone_enc is None
                    assert first.whatsapp_phone_number_id is None
                    assert valid.user_id_enc != "8000000000000"
                    assert decrypt_pii(valid.user_id_enc) == "8000000000000"
                    assert decrypt_pii(bot.token_enc) == "synthetic-token"

                    async def rejects(record: TelegramIdentity | Lead | TelegramBot) -> None:
                        with pytest.raises(sa.exc.IntegrityError):
                            async with session.begin_nested():
                                session.add(record)
                                await session.flush()

                    await rejects(identity(first.id, first_lead.id, 8000000000000))
                    # Same tenant as bot, wrong tenant for lead.
                    await rejects(identity(first.id, second_lead.id, 8000000000001))
                    # Same tenant as lead, wrong tenant for bot.
                    await rejects(identity(second.id, second_lead.id, 8000000000002))
                    await rejects(
                        TelegramBot(
                            tenant_id=second.id,
                            telegram_bot_id=123456789,
                            token_enc=encrypt_pii("another-synthetic-token"),
                        )
                    )
                    await rejects(Lead(tenant_id=first.id, phone_hash="unpaired-contact"))
                    await session.rollback()
        finally:
            await engine.dispose()

    asyncio.run(exercise())


def test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(
    identity_database: str,
) -> None:
    cfg = Config("alembic.ini")

    async def insert_rows() -> tuple[uuid.UUID, uuid.UUID]:
        engine = create_async_engine(identity_database)
        try:
            async with AsyncSession(engine, expire_on_commit=False) as session:
                legacy = Institution(name="Legacy synthetic", whatsapp_phone_number_id="legacy")
                telegram = Institution(name="Telegram synthetic")
                session.add_all([legacy, telegram])
                await session.flush()
                session.add(
                    Lead(tenant_id=legacy.id, phone_hash="legacy-hash", phone_enc="legacy-cipher")
                )
                session.add(
                    TelegramBot(
                        tenant_id=legacy.id,
                        telegram_bot_id=987654321,
                        token_enc=encrypt_pii("synthetic-existing-bot"),
                    )
                )
                await session.commit()
                return legacy.id, telegram.id
        finally:
            await engine.dispose()

    legacy_id, telegram_id = asyncio.run(insert_rows())
    with pytest.raises(RuntimeError, match="Migrate Telegram-only records"):
        command.downgrade(cfg, "c470f1ebc811")

    async def inspect_and_clean() -> None:
        engine = create_async_engine(identity_database)
        try:
            async with engine.begin() as conn:
                tables = await conn.run_sync(lambda c: sa.inspect(c).get_table_names())
                assert "telegram_identities" in tables
                assert await conn.scalar(
                    sa.select(Institution.id).where(Institution.id == legacy_id)
                )
                await conn.execute(sa.delete(Institution).where(Institution.id == telegram_id))
        finally:
            await engine.dispose()

    asyncio.run(inspect_and_clean())
    # A bot attached to a legacy institution still contains routing/credential
    # data. Refuse to drop it even though all remaining phone fields are filled.
    with pytest.raises(RuntimeError, match="Migrate Telegram-only records"):
        command.downgrade(cfg, "c470f1ebc811")

    async def remove_test_bot() -> None:
        engine = create_async_engine(identity_database)
        try:
            async with engine.begin() as conn:
                await conn.execute(sa.delete(TelegramBot).where(TelegramBot.tenant_id == legacy_id))
        finally:
            await engine.dispose()

    asyncio.run(remove_test_bot())
    command.downgrade(cfg, "c470f1ebc811")
    command.upgrade(cfg, "head")

    async def verify_legacy() -> None:
        engine = create_async_engine(identity_database)
        try:
            async with AsyncSession(engine) as session:
                legacy_lead = await session.scalar(
                    sa.select(Lead).where(Lead.tenant_id == legacy_id)
                )
                assert legacy_lead is not None
                assert legacy_lead.phone_enc == "legacy-cipher"
                await session.execute(sa.delete(Institution).where(Institution.id == legacy_id))
                await session.commit()
        finally:
            await engine.dispose()

    asyncio.run(verify_legacy())
