"""Liveness is separate from readiness and production has no public debug enqueue."""

import pytest
from fastapi.testclient import TestClient

from src.core.settings import Settings
from src.main import create_app


def test_unconfigured_runtime_is_not_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.main.get_settings",
        lambda: Settings(
            _env_file=None, database_url=None, redis_url=None, knowledge_recovery_enabled=False
        ),
    )
    with TestClient(create_app()) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/ready").status_code == 503


def test_production_debug_enqueue_is_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "src.main.get_settings",
        lambda: Settings(
            _env_file=None,
            app_env="prod",
            database_url=None,
            redis_url=None,
            knowledge_recovery_enabled=False,
        ),
    )
    with TestClient(create_app()) as client:
        assert client.get("/debug/enqueue-ping").status_code == 404
        assert "/debug/enqueue-ping" not in client.get("/openapi.json").json()["paths"]
