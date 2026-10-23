"""TaskIQ broker singleton.

In production (and local dev with Redis running) the broker is a
:class:`~taskiq_redis.ListQueueBroker` backed by Redis — using ``LPUSH`` /
``BRPOP`` so each message is consumed by exactly one worker.

When ``REDIS_URL`` is not set the broker falls back to
:class:`~taskiq.InMemoryBroker` so the test suite and the health-check can
boot without a running Redis instance.

The module path ``src.tasks.broker:broker`` is what the ``taskiq worker``
CLI references (SPEC §3 — Key Commands).
"""

from __future__ import annotations

import taskiq

from src.core.settings import get_settings


def _build_broker() -> taskiq.AsyncBroker:
    """Construct the right broker based on the current settings.

    This is a plain factory called once at import time. Tests that override
    settings (or pass ``REDIS_URL=None``) get the in-memory variant
    automatically.
    """
    settings = get_settings()

    if settings.redis_url:
        from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

        # BRPOP waits indefinitely for work; redis-py's default read deadline
        # otherwise kills an idle worker. Keep this scoped to the queue pool.
        return ListQueueBroker(url=settings.redis_url, socket_timeout=None).with_result_backend(
            RedisAsyncResultBackend(redis_url=settings.redis_url),
        )

    # No Redis configured — fall back to a zero-dependency in-memory broker.
    # Works for unit tests and for booting the API without Redis.
    return taskiq.InMemoryBroker()


broker = _build_broker()
