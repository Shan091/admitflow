"""Actual Redis Lua reservations must remain bounded under concurrent workers."""

import asyncio
import uuid
from types import SimpleNamespace

import pytest
from redis.asyncio import Redis

from src.core.settings import get_settings
from src.telegram import budget

pytestmark = pytest.mark.integration


async def test_atomic_shared_reservations_and_isolation(monkeypatch):
    url = get_settings().redis_url
    if not url:
        pytest.skip("Set REDIS_URL for the real Redis budget check")
    client = Redis.from_url(url, decode_responses=True)
    monkeypatch.setattr(budget, "get_redis", lambda: client)
    monkeypatch.setattr(
        budget, "get_settings", lambda: SimpleNamespace(redis_url=url, app_env="prod")
    )
    tenant = SimpleNamespace(id=uuid.uuid4(), timezone="Asia/Kolkata", telegram_daily_send_limit=7)
    second = SimpleNamespace(id=uuid.uuid4(), timezone="Asia/Kolkata", telegram_daily_send_limit=7)
    keys = []
    try:
        results = await asyncio.gather(
            *(budget.reserve(tenant, f"attempt:{n}") for n in range(100))
        )
        keys.extend([results[0].key + ":attempts", results[0].key + ":sent"])
        permitted = [value for value in results if value.allowed]
        assert len(permitted) == 7
        replayed = await asyncio.gather(
            *(budget.reserve(tenant, permitted[0].token) for _ in range(20))
        )
        assert all(value.allowed for value in replayed)
        await asyncio.gather(*(budget.record_sent(permitted[0]) for _ in range(20)))
        stats = await budget.usage(tenant)
        assert stats["attempts"] == 7 and stats["confirmed_sent"] == 1 and stats["warning"]
        assert await client.ttl(keys[0]) > 0
        other = await budget.reserve(second, "independent")
        keys.extend([other.key + ":attempts", other.key + ":sent"])
        assert other.allowed and (await budget.usage(second))["attempts"] == 1
        tenant.telegram_daily_send_limit = 0
        assert not (await budget.reserve(tenant, permitted[0].token)).allowed
    finally:
        if keys:
            await client.delete(*keys)
        await client.aclose()
