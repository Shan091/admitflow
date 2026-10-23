"""Redis distributed mutex with owner-safe release and keepalive (Task 7).

Ensures only one worker processes a message per phone number at a time.
Uses ``SET NX PX`` for acquisition and a Lua CAS script for release so only
the owner can unlock — if a worker crashes, the TTL auto-releases the lock.

Usage::

    from src.core.redis import get_redis

    async with RedisMutex(get_redis(), f"wa_mutex:{phone}"):
        await process_message(...)

Or use the convenience helper::

    from src.core.mutex import redis_mutex

    async with redis_mutex(f"wa_mutex:{phone}"):
        await process_message(...)
"""

from __future__ import annotations

import asyncio
import uuid
from types import TracebackType

import redis.asyncio as aioredis


class MutexAcquireError(RuntimeError):
    """Raised when the mutex cannot be acquired after all retries."""


# Lua script: compare-and-swap delete — only the owner can release.
# KEYS[1] = lock key, ARGV[1] = owner token.
# Returns 1 on success, 0 if the key didn't exist or had a different owner.
_RELEASE_LUA = """
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
"""


class RedisMutex:
    """Async context-manager mutex backed by Redis ``SET NX``.

    Parameters:
        redis: An async Redis client.
        key: The lock key (e.g. ``wa_mutex:+919876543210``).
        ttl_seconds: Auto-release timeout in seconds.
        keepalive: If ``True``, a background task extends the TTL while held.
        keepalive_interval: Seconds between keepalive ticks (default: ttl / 3).
        retry_count: Number of retries after the initial attempt (0 = no retry).
        retry_delay: Seconds between retries.
    """

    def __init__(
        self,
        redis: aioredis.Redis,
        key: str,
        *,
        ttl_seconds: int = 30,
        keepalive: bool = True,
        keepalive_interval: float | None = None,
        retry_count: int = 3,
        retry_delay: float = 0.2,
    ) -> None:
        self._redis = redis
        self._key = key
        self._ttl_ms = ttl_seconds * 1000
        self._owner = uuid.uuid4().hex
        self._keepalive = keepalive
        self._keepalive_interval = keepalive_interval or (ttl_seconds / 3.0)
        self._retry_count = retry_count
        self._retry_delay = retry_delay
        self._keepalive_task: asyncio.Task[None] | None = None

    async def acquire(self) -> None:
        """Attempt to acquire the lock, retrying up to ``retry_count`` times."""
        for attempt in range(1 + self._retry_count):
            acquired = await self._redis.set(self._key, self._owner, nx=True, px=self._ttl_ms)
            if acquired:
                if self._keepalive:
                    self._keepalive_task = asyncio.create_task(self._run_keepalive())
                return
            if attempt < self._retry_count:
                await asyncio.sleep(self._retry_delay)

        raise MutexAcquireError(
            f"Could not acquire mutex {self._key!r} after {1 + self._retry_count} attempts."
        )

    async def release(self) -> None:
        """Release the lock using the Lua CAS script (owner-safe)."""
        if self._keepalive_task is not None:
            self._keepalive_task.cancel()
            try:
                await self._keepalive_task
            except asyncio.CancelledError:
                pass
            self._keepalive_task = None

        await self._redis.eval(_RELEASE_LUA, 1, self._key, self._owner)

    async def _run_keepalive(self) -> None:
        """Background loop that extends the TTL while the lock is held."""
        try:
            while True:
                await asyncio.sleep(self._keepalive_interval)
                await self._redis.pexpire(self._key, self._ttl_ms)
        except asyncio.CancelledError:
            return

    async def __aenter__(self) -> RedisMutex:
        await self.acquire()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.release()
