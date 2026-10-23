"""Atomic daily send-attempt budgets shared by every Telegram delivery path."""

import logging
import math
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from src.core.redis import get_redis
from src.core.settings import get_settings
from src.db.models import Institution

logger = logging.getLogger(__name__)
_local: dict[str, tuple[set[str], set[str], datetime]] = {}
RESERVE = """
if tonumber(ARGV[2]) <= 0 then return 0 end
if redis.call('SISMEMBER', KEYS[1], ARGV[1]) == 1 then return 1 end
if redis.call('SCARD', KEYS[1]) >= tonumber(ARGV[2]) then return 0 end
redis.call('SADD', KEYS[1], ARGV[1]); redis.call('EXPIRE', KEYS[1], ARGV[3]); return 1
"""
CONFIRM = """
redis.call('SADD', KEYS[1], ARGV[1]); redis.call('EXPIRE', KEYS[1], ARGV[2]); return 1
"""


def safe_zone(timezone: str) -> ZoneInfo:
    try:
        return ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")  # Legacy invalid settings cannot bypass the daily cap.


def day_window(tenant_id: uuid.UUID, timezone: str, now: datetime) -> tuple[str, datetime]:
    zone = safe_zone(timezone)
    local = now.astimezone(zone)
    reset = datetime.combine(local.date() + timedelta(days=1), time.min, zone).astimezone(UTC)
    return f"telegram-budget:{{{tenant_id}}}:{local.date().isoformat()}", reset


@dataclass(frozen=True)
class Reservation:
    allowed: bool
    retry_at: datetime
    reason: str | None
    key: str
    token: str
    local: bool


def local_counts(key: str, reset: datetime, now: datetime) -> tuple[set[str], set[str]]:
    for stale, (_, _, expiry) in list(_local.items()):
        if expiry <= now:
            _local.pop(stale, None)
    if key not in _local:
        if len(_local) >= 10000:
            raise RuntimeError("Development budget capacity reached")
        _local[key] = (set(), set(), reset + timedelta(days=2))
    attempts, sent, _ = _local[key]
    return attempts, sent


async def reserve(
    institution: Institution, token: str, *, now: datetime | None = None
) -> Reservation:
    now = now or datetime.now(UTC)
    key, reset = day_window(institution.id, institution.timezone, now)
    settings = get_settings()
    local = not settings.redis_url and settings.app_env != "prod"
    try:
        if local:
            attempts, _ = local_counts(key, reset, now)
            allowed = institution.telegram_daily_send_limit > 0 and (
                token in attempts or len(attempts) < institution.telegram_daily_send_limit
            )
            if allowed:
                attempts.add(token)
        else:
            allowed = bool(
                await get_redis().eval(
                    RESERVE,
                    1,
                    key + ":attempts",
                    token,
                    institution.telegram_daily_send_limit,
                    max(1, math.ceil((reset - now).total_seconds())) + 172800,
                )
            )
    except Exception:
        return Reservation(
            False, now + timedelta(seconds=60), "send_budget_unavailable", key, token, local
        )
    return Reservation(allowed, reset, None if allowed else "daily_send_budget", key, token, local)


async def record_sent(reservation: Reservation) -> None:
    """Count confirmed deliveries once; a stats failure must not repeat a sent message."""
    if not reservation.allowed:
        return
    try:
        if reservation.local:
            if reservation.key in _local:
                _local[reservation.key][1].add(reservation.token)
        else:
            await get_redis().eval(CONFIRM, 1, reservation.key + ":sent", reservation.token, 259200)
    except Exception:
        logger.warning("telegram_delivery_statistics_unavailable")


async def usage(institution: Institution, *, now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    key, reset = day_window(institution.id, institution.timezone, now)
    limit = institution.telegram_daily_send_limit
    result: dict[str, Any] = {
        "day": key.rsplit(":", 1)[1],
        "timezone": str(safe_zone(institution.timezone)),
        "limit": limit,
        "resets_at": reset.isoformat(),
        "available": False,
        "attempts": None,
        "confirmed_sent": None,
        "remaining": None,
        "warning": True,
    }
    settings = get_settings()
    try:
        if not settings.redis_url and settings.app_env != "prod":
            attempted, sent = local_counts(key, reset, now)
            attempts, confirmed = len(attempted), len(sent)
        else:
            async with get_redis().pipeline(transaction=True) as pipe:
                pipe.scard(key + ":attempts")
                pipe.scard(key + ":sent")
                attempts, confirmed = await pipe.execute()
        result.update(
            available=True,
            attempts=attempts,
            confirmed_sent=confirmed,
            remaining=max(0, limit - attempts),
            warning=limit == 0 or attempts >= math.ceil(limit * 0.8),
        )
    except Exception:
        pass  # Unknown counts are explicit; never claim zero usage during an outage.
    return result
