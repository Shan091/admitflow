"""Tests for the TaskIQ broker setup and task execution (Task 3).

All tests run against the ``InMemoryBroker`` (no Redis required) because the
default test environment has no ``REDIS_URL`` set.
"""

from __future__ import annotations

from src.tasks.broker import broker


def test_broker_is_in_memory_without_redis_url() -> None:
    """When REDIS_URL is unset the factory should yield an InMemoryBroker."""
    from taskiq import InMemoryBroker

    assert isinstance(broker, InMemoryBroker)


async def test_ping_task_returns_result() -> None:
    """The ping task should run and return the expected payload."""
    from src.tasks.processing import ping

    await broker.startup()
    try:
        result = await ping.kiq("hello")
        task_result = await result.wait_result(timeout=5.0)
        assert task_result.return_value == {"result": "hello"}
    finally:
        await broker.shutdown()


async def test_ping_task_default_payload() -> None:
    """Ping without an explicit payload should default to 'pong'."""
    from src.tasks.processing import ping

    await broker.startup()
    try:
        result = await ping.kiq()
        task_result = await result.wait_result(timeout=5.0)
        assert task_result.return_value == {"result": "pong"}
    finally:
        await broker.shutdown()
