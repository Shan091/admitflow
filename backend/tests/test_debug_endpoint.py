"""Tests for the /debug endpoints (Task 3 verification)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_enqueue_ping_returns_task_id() -> None:
    """GET /debug/enqueue-ping should enqueue a ping task and return its ID."""
    resp = client.get("/debug/enqueue-ping")
    assert resp.status_code == 200
    body = resp.json()
    assert "task_id" in body
    # Task IDs are non-empty strings assigned by the broker.
    assert isinstance(body["task_id"], str)
    assert len(body["task_id"]) > 0
