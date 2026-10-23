"""Bounded login throttling; shared Redis when configured, development fallback."""

import hashlib
import time

from fastapi import HTTPException, Request

from src.core.redis import get_redis
from src.core.settings import get_settings

_local: dict[str, tuple[int, float]] = {}


async def check_login_limit(request: Request, institution: str, email: str) -> None:
    host = request.client.host if request.client else "unknown"
    await consume_limit(f"login-host:{host}", 100)
    await consume_limit(f"login-account:{host}:{institution}:{email.lower()}", 10)


async def consume_limit(key: str, limit: int) -> None:
    """Fixed five-minute windows, shared across API processes in production."""
    digest = hashlib.sha256(key.encode()).hexdigest()
    if get_settings().redis_url:
        try:
            count = await get_redis().eval(
                "local n=redis.call('INCR',KEYS[1]); if n==1 then "
                "redis.call('EXPIRE',KEYS[1],300) end; return n",
                1,
                f"staff-workspace:{digest}",
            )
        except Exception:
            raise HTTPException(
                503, "Workspace service is temporarily unavailable. Try again shortly."
            ) from None
    else:
        if get_settings().app_env == "prod":
            raise HTTPException(503, "Workspace service is unavailable.")
        now = time.monotonic()
        for key, (_, expiry) in list(_local.items()):
            if expiry <= now:
                _local.pop(key, None)
        if digest not in _local and len(_local) >= 10000:
            raise HTTPException(429, "Too many requests. Try again later.")
        previous, expiry = _local.get(digest, (0, now + 300))
        count = previous + 1
        _local[digest] = (count, expiry)
    if count > limit:
        raise HTTPException(429, "Too many requests. Try again in a few minutes.")
