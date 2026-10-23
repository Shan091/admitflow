"""Async engine and session factory.

Built lazily from ``settings.database_url`` so the app still boots with no
database configured (the health check and Task-1 tests must not require one).
Anything that actually touches the DB calls :func:`get_sessionmaker` /
:func:`get_session`, which raises a clear error when the URL is unset.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings import get_settings


class DatabaseNotConfiguredError(RuntimeError):
    """Raised when a DB session is requested but ``DATABASE_URL`` is unset."""


@lru_cache
def get_engine() -> AsyncEngine:
    """Return the process-wide async engine (one pool for the app)."""
    settings = get_settings()
    if not settings.database_url:
        raise DatabaseNotConfiguredError(
            "DATABASE_URL is not set — configure it before using the database."
        )
    return create_async_engine(settings.database_url, pool_pre_ping=True)


@lru_cache
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """Return the process-wide async session factory."""
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding a session that closes after the request."""
    async with get_sessionmaker()() as session:
        yield session
