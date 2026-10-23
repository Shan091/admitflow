"""Daily limits use institution-local dates and fail closed in production."""

import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from src.telegram import budget


def test_local_midnight_handles_dst():
    key, reset = budget.day_window(
        uuid.UUID(int=1), "America/New_York", datetime(2026, 11, 1, 4, 30, tzinfo=UTC)
    )
    assert "2026-11-01" in key
    assert reset == datetime(2026, 11, 2, 5, tzinfo=UTC)
    assert budget.day_window(
        uuid.UUID(int=1), "Asia/Kolkata", datetime(2026, 10, 23, 20, tzinfo=UTC)
    )[1] == datetime(2026, 10, 24, 18, 30, tzinfo=UTC)


async def test_development_limit_replay_and_confirmed_count(monkeypatch):
    monkeypatch.setattr(
        budget, "get_settings", lambda: SimpleNamespace(redis_url=None, app_env="dev")
    )
    tenant = SimpleNamespace(id=uuid.uuid4(), timezone="Asia/Kolkata", telegram_daily_send_limit=2)
    now = datetime(2026, 10, 24, 5, tzinfo=UTC)
    first = await budget.reserve(tenant, "r:one:1", now=now)
    assert first.allowed
    assert (await budget.reserve(tenant, "r:one:1", now=now)).allowed
    await budget.record_sent(first)
    await budget.record_sent(first)
    assert (await budget.reserve(tenant, "o:two:1", now=now)).allowed
    denied = await budget.reserve(tenant, "r:three:1", now=now)
    assert not denied.allowed and denied.reason == "daily_send_budget"
    assert denied.retry_at == datetime(2026, 10, 24, 18, 30, tzinfo=UTC)
    usage = await budget.usage(tenant, now=now)
    tenant.telegram_daily_send_limit = 0
    assert not (await budget.reserve(tenant, "r:one:1", now=now)).allowed
    tenant.telegram_daily_send_limit = 2
    assert usage["attempts"] == 2 and usage["confirmed_sent"] == 1 and usage["warning"]
    assert (
        await budget.reserve(tenant, "r:three:1", now=datetime(2026, 10, 25, 5, tzinfo=UTC))
    ).allowed


async def test_production_without_redis_defers_delivery(monkeypatch):
    monkeypatch.setattr(
        budget, "get_settings", lambda: SimpleNamespace(redis_url=None, app_env="prod")
    )
    tenant = SimpleNamespace(id=uuid.uuid4(), timezone="Asia/Kolkata", telegram_daily_send_limit=10)
    result = await budget.reserve(tenant, "r:one:1")
    assert not result.allowed and result.reason == "send_budget_unavailable"
    assert not (await budget.usage(tenant))["available"]


@pytest.mark.parametrize("limit", [0, 1])
async def test_zero_pauses_and_one_stops_after_first(limit, monkeypatch):
    monkeypatch.setattr(
        budget, "get_settings", lambda: SimpleNamespace(redis_url=None, app_env="dev")
    )
    tenant = SimpleNamespace(id=uuid.uuid4(), timezone="UTC", telegram_daily_send_limit=limit)
    assert (await budget.reserve(tenant, "first")).allowed == bool(limit)
    assert not (await budget.reserve(tenant, "second")).allowed


async def test_redis_failure_never_admits_a_send_or_claims_zero_usage(monkeypatch):
    monkeypatch.setattr(
        budget,
        "get_settings",
        lambda: SimpleNamespace(redis_url="redis://unavailable", app_env="prod"),
    )

    def unavailable():
        raise ConnectionError("Synthetic budget outage")

    monkeypatch.setattr(budget, "get_redis", unavailable)
    tenant = SimpleNamespace(id=uuid.uuid4(), timezone="UTC", telegram_daily_send_limit=100)
    result = await budget.reserve(tenant, "outage")
    assert not result.allowed and result.reason == "send_budget_unavailable"
    stats = await budget.usage(tenant)
    assert not stats["available"] and stats["attempts"] is None and stats["remaining"] is None
