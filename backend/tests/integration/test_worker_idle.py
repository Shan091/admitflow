"""A real Redis worker must stay listening while its queue is idle."""

import asyncio
from uuid import uuid4

import pytest
from redis.asyncio import Redis
from taskiq_redis import ListQueueBroker

from src.core.settings import get_settings
from src.tasks.broker import _build_broker

pytestmark = pytest.mark.integration


async def test_idle_queue_listener_receives_a_later_message() -> None:
    url = get_settings().redis_url
    if not url:
        pytest.skip("Set REDIS_URL to a dedicated test Redis")

    broker = _build_broker()
    assert isinstance(broker, ListQueueBroker)
    broker.queue_name = f"readiness-idle-test:{uuid4()}"
    redis = Redis.from_url(url)
    listener = broker.listen()
    pending = asyncio.create_task(anext(listener))
    try:
        # redis-py's default socket read deadline is five seconds. A blocking
        # queue listener must outlive it and accept work after a quiet period.
        await asyncio.sleep(6)
        await redis.lpush(broker.queue_name, b"after-idle")
        assert await asyncio.wait_for(pending, timeout=3) == b"after-idle"
    finally:
        if not pending.done():
            pending.cancel()
        await asyncio.gather(pending, return_exceptions=True)
        await listener.aclose()
        await redis.delete(broker.queue_name)
        await redis.aclose()
        await broker.shutdown()
