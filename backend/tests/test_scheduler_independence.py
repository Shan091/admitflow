"""A queue outage must not suppress a configured database privacy sweep."""

from unittest.mock import AsyncMock

import pytest

from src.scripts import scheduler


@pytest.mark.parametrize("startup_failure", [False, True])
async def test_queue_failure_does_not_skip_retention(monkeypatch, startup_failure):
    monkeypatch.setattr(
        scheduler.broker,
        "startup",
        AsyncMock(side_effect=ConnectionError("synthetic") if startup_failure else None),
    )
    shutdown = AsyncMock()
    monkeypatch.setattr(scheduler.broker, "shutdown", shutdown)
    monkeypatch.setattr(
        scheduler, "dispatch_due", AsyncMock(side_effect=ConnectionError("synthetic"))
    )
    monkeypatch.setattr(scheduler, "recover_outbound", AsyncMock())
    monkeypatch.setattr(scheduler, "dispatch_integrations", AsyncMock())
    monkeypatch.setattr(scheduler, "check_demo_payments", AsyncMock(return_value=0))
    purge = AsyncMock(return_value=1)
    monkeypatch.setattr(scheduler, "purge_retained", purge)
    with pytest.raises(RuntimeError):
        await scheduler.run(once=True)
    purge.assert_awaited_once()
    if startup_failure:
        shutdown.assert_not_awaited()
    else:
        shutdown.assert_awaited_once()
