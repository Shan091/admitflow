"""Bound resource use and reject browser cross-origin mutations before database access."""

from typing import Any

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.requests import Request as StarletteRequest

from src.core.settings import Settings
from src.knowledge.limits import UploadBodyLimit
from src.staff import throttle
from src.staff.auth import require_browser_write


def test_request_limit_with_and_without_content_length(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = Settings(_env_file=None, upload_batch_max_bytes=1024)
    monkeypatch.setattr("src.knowledge.limits.get_settings", lambda: settings)
    app = FastAPI()
    app.add_middleware(UploadBodyLimit)

    @app.post("/api/knowledge/documents")
    async def read(request: Request) -> dict[str, int]:
        return {"size": len(await request.body())}

    with TestClient(app) as client:
        assert (
            client.post("/api/knowledge/documents", content=b"x" * (2 * 1024 * 1024)).status_code
            == 413
        )
        assert (
            client.post(
                "/api/knowledge/documents", content=iter([b"x" * (2 * 1024 * 1024)])
            ).status_code
            == 413
        )
        assert client.post("/api/knowledge/documents", content=b"small").json() == {"size": 5}


async def test_login_throttle_blocks_rotating_accounts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(throttle, "get_settings", lambda: Settings(_env_file=None, redis_url=None))
    monkeypatch.setattr(throttle, "_local", {})
    request = StarletteRequest({"type": "http", "client": ("192.0.2.1", 1), "headers": []})
    for index in range(100):
        await throttle.check_login_limit(request, "synthetic", f"user{index}@example.test")
    with pytest.raises(Exception) as error:
        await throttle.check_login_limit(request, "synthetic", "another@example.test")
    assert error.value.status_code == 429


async def test_invalid_embeddings_cannot_publish(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.knowledge import processing

    class Result:
        data: list[dict[str, Any]] = [{"index": 0, "embedding": [0.0] * 1536}]

    async def invalid(**kwargs: Any) -> Result:
        return Result()

    monkeypatch.setattr(processing, "aembedding", invalid)
    monkeypatch.setattr(
        processing, "get_settings", lambda: Settings(_env_file=None, openai_api_key="synthetic-key")
    )
    with pytest.raises(ValueError, match="embedding"):
        await processing.embed_chunks(["synthetic"])


async def test_embedding_key_loaded_from_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    from src.knowledge import processing

    captured: dict[str, Any] = {}

    class Result:
        data = [{"index": 0, "embedding": [1.0] + [0.0] * 1535}]

    async def respond(**kwargs: Any) -> Result:
        captured.update(kwargs)
        return Result()

    monkeypatch.setattr(processing, "aembedding", respond)
    monkeypatch.setattr(
        processing, "get_settings", lambda: Settings(_env_file=None, openai_api_key="synthetic-key")
    )
    await processing.embed_chunks(["synthetic"])
    assert captured["api_key"] == "synthetic-key"
    assert captured["dimensions"] == 1536


def test_custom_header_and_origin_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.staff.auth.get_settings", lambda: Settings(_env_file=None))
    request = StarletteRequest(
        {
            "type": "http",
            "headers": [(b"origin", b"https://attacker.test"), (b"x-admitflow-request", b"1")],
        }
    )
    with pytest.raises(Exception) as error:
        require_browser_write(request)
    assert error.value.status_code == 403
