"""Shared async Redis client for application code.

Carry-over prerequisite #1: the TaskIQ broker has its own internal Redis
connection. Application-level code (webhook dedup via SETNX, the distributed
mutex, rate-limit counters) needs a *separate* ``redis.asyncio.Redis`` instance
drawn from ``settings.redis_url``.

Access through :func:`get_redis`, which is ``lru_cache``-d so the whole process
shares one client (and therefore one connection pool). If ``REDIS_URL`` is
unset, it raises :class:`RedisNotConfiguredError` — same fail-loud contract as
:class:`~src.db.session.DatabaseNotConfiguredError`.
"""

from __future__ import annotations

from functools import lru_cache

import redis.asyncio as aioredis

from src.core.settings import get_settings


class RedisNotConfiguredError(RuntimeError):
    """Raised when Redis is needed but ``REDIS_URL`` is unset in settings."""


@lru_cache
def get_redis() -> aioredis.Redis:
    """Return the process-wide async Redis client singleton.

    The client is created lazily and cached. It uses the ``hiredis`` parser
    when available (the ``redis[hiredis]`` extra is already in dependencies).

    Raises:
        RedisNotConfiguredError: If ``REDIS_URL`` is not configured.
    """
    url = get_settings().redis_url
    if not url:
        raise RedisNotConfiguredError("REDIS_URL is not set — configure it before using Redis.")
    return aioredis.from_url(url, decode_responses=True)
