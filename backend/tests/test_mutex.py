"""Tests for the Redis distributed mutex (Task 7).

The mutex must guarantee:
1. Only one holder at a time per key
2. Owner-safe release (only the acquirer can release)
3. Auto-release after TTL if the holder crashes
4. Keepalive extends TTL while held

We test against a fake/mock Redis to avoid a real server dependency in the
default test suite.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from src.core.mutex import MutexAcquireError, RedisMutex


class TestRedisMutexAcquire:
    """Acquiring and releasing the mutex."""

    @pytest.mark.asyncio
    async def test_acquire_succeeds_on_free_key(self) -> None:
        """First caller acquires the lock immediately."""
        mock_redis = AsyncMock()
        # SET NX returns True when key didn't exist.
        mock_redis.set = AsyncMock(return_value=True)
        mock_redis.delete = AsyncMock()

        mutex = RedisMutex(mock_redis, "test:key", ttl_seconds=10, keepalive=False)
        async with mutex:
            # We got in — the SET NX call was made.
            mock_redis.set.assert_called_once()
            call_kwargs = mock_redis.set.call_args
            assert call_kwargs.kwargs.get("nx") is True

    @pytest.mark.asyncio
    async def test_acquire_fails_when_key_held(self) -> None:
        """When the key is already held, acquire raises MutexAcquireError."""
        mock_redis = AsyncMock()
        # SET NX returns False/None when key already exists.
        mock_redis.set = AsyncMock(return_value=False)

        mutex = RedisMutex(mock_redis, "test:key", ttl_seconds=10, keepalive=False, retry_count=0)
        with pytest.raises(MutexAcquireError):
            async with mutex:
                pass  # pragma: no cover — should never reach here

    @pytest.mark.asyncio
    async def test_owner_safe_release(self) -> None:
        """Release only deletes the key if the value matches the owner token."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock(return_value=True)
        # evalsha / eval for Lua script — return 1 means success.
        mock_redis.evalsha = AsyncMock(return_value=1)
        mock_redis.eval = AsyncMock(return_value=1)

        mutex = RedisMutex(mock_redis, "test:key", ttl_seconds=10, keepalive=False)
        async with mutex:
            pass
        # The Lua-based release should have been called.
        assert mock_redis.eval.called or mock_redis.evalsha.called


class TestRedisMutexTTL:
    """TTL and keepalive behaviour."""

    @pytest.mark.asyncio
    async def test_set_uses_ttl(self) -> None:
        """The SET call includes the configured TTL."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock(return_value=True)

        mutex = RedisMutex(mock_redis, "test:key", ttl_seconds=30, keepalive=False)
        async with mutex:
            call_kwargs = mock_redis.set.call_args
            # TTL should be passed as px (milliseconds) or ex (seconds).
            px = call_kwargs.kwargs.get("px")
            ex = call_kwargs.kwargs.get("ex")
            assert (px is not None and px > 0) or (ex is not None and ex > 0)

    @pytest.mark.asyncio
    async def test_keepalive_extends_ttl(self) -> None:
        """When keepalive is enabled, the mutex periodically extends the TTL."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock(return_value=True)
        mock_redis.pexpire = AsyncMock(return_value=True)

        mutex = RedisMutex(
            mock_redis,
            "test:key",
            ttl_seconds=1,
            keepalive=True,
            keepalive_interval=0.1,
        )

        async with mutex:
            # Wait long enough for at least one keepalive tick.
            await asyncio.sleep(0.25)

        # pexpire should have been called at least once during the hold.
        assert mock_redis.pexpire.call_count >= 1


class TestRedisMutexRetry:
    """Retry behaviour when the lock is initially held."""

    @pytest.mark.asyncio
    async def test_retries_and_succeeds(self) -> None:
        """Lock acquired on a retry after initial failure."""
        mock_redis = AsyncMock()
        # Fail twice, then succeed.
        mock_redis.set = AsyncMock(side_effect=[False, False, True])

        mutex = RedisMutex(
            mock_redis,
            "test:key",
            ttl_seconds=10,
            keepalive=False,
            retry_count=5,
            retry_delay=0.01,
        )
        async with mutex:
            pass
        assert mock_redis.set.call_count == 3

    @pytest.mark.asyncio
    async def test_retries_exhausted_raises(self) -> None:
        """When all retries fail, MutexAcquireError is raised."""
        mock_redis = AsyncMock()
        mock_redis.set = AsyncMock(return_value=False)

        mutex = RedisMutex(
            mock_redis,
            "test:key",
            ttl_seconds=10,
            keepalive=False,
            retry_count=2,
            retry_delay=0.01,
        )
        with pytest.raises(MutexAcquireError):
            async with mutex:
                pass  # pragma: no cover
