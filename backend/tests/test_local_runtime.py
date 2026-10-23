"""Local bootstrap preserves secrets and legacy ingress stays explicitly opt-in."""

from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.core.settings import Settings
from src.main import create_app
from src.scripts.configure_compose import configure


def test_compose_configuration_is_private_and_never_overwrites(tmp_path: Path) -> None:
    target = tmp_path / ".env"
    configure(target)
    original = target.read_bytes()
    assert b"PII_ENCRYPTION_KEY=" in original
    assert b"PHONE_HASH_KEY=" in original
    assert b"TELEGRAM_BOT_TOKEN=\n" in original
    assert b"OPENAI_API_KEY=\n" in original
    assert b"APP_ENV=dev" in original
    with pytest.raises(FileExistsError):
        configure(target)
    assert target.read_bytes() == original


def test_legacy_webhook_is_absent_and_nondev_debug_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("src.main.get_settings", lambda: Settings(_env_file=None, app_env="prod"))
    app = create_app()
    assert not app.debug
    with TestClient(app) as client:
        assert client.post("/api/webhook", json={}).status_code == 404


@pytest.mark.asyncio
async def test_preexisting_legacy_job_cannot_dispatch_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from src.tasks import processing

    handler = AsyncMock()
    monkeypatch.setattr(processing, "handle_turn", handler)
    monkeypatch.setattr(processing, "get_settings", lambda: Settings(_env_file=None))
    await processing.process_inbound_message({"synthetic": True})
    handler.assert_not_awaited()
