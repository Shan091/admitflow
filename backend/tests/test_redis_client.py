"""Tests for the shared async Redis client helper (carry-over prerequisite #1).

The helper must provide a singleton ``redis.asyncio.Redis`` from settings and
fail loud when ``redis_url`` is unset — same contract as
``DatabaseNotConfiguredError``.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from src.core.redis import RedisNotConfiguredError, get_redis


class TestGetRedis:
    """get_redis() singleton behaviour."""

    def test_raises_when_redis_url_unset(self) -> None:
        """Calling get_redis() with no REDIS_URL must fail loud."""
        with patch("src.core.redis.get_settings") as mock_settings:
            mock_settings.return_value.redis_url = None
            # Clear any cached client from a prior call.
            get_redis.cache_clear()
            with pytest.raises(RedisNotConfiguredError):
                get_redis()

    def test_returns_redis_client_when_configured(self) -> None:
        """When REDIS_URL is set, get_redis() returns a Redis client."""
        with patch("src.core.redis.get_settings") as mock_settings:
            mock_settings.return_value.redis_url = "redis://localhost:6379/0"
            get_redis.cache_clear()
            client = get_redis()
            # Should be a redis.asyncio.Redis (or compatible) instance.
            assert client is not None
            # Calling again returns the same cached instance.
            assert get_redis() is client
            get_redis.cache_clear()
