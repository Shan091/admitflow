from pathlib import Path

from fastapi.testclient import TestClient

from admitflow.config import Settings, get_settings
from admitflow.main import create_app


def test_health_and_dashboard_render_without_credentials(tmp_path: Path) -> None:
    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
    )
    app = create_app(settings)

    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        dashboard = client.get("/")
        assert dashboard.status_code == 200
        assert "fictional demo" in dashboard.text
        assert "No leads yet" in dashboard.text

        repository = app.state.repository
        lead_id = repository.upsert_lead(repository.tenant_id, "42", "sample")
        repository.update_lead(lead_id, selected_course_id="foundations-computing")
        repository.add_message(lead_id, "inbound", "/start", 123)
        assert "sample" in client.get("/").text
        detail = client.get(f"/leads/{lead_id}")
        assert detail.status_code == 200
        assert "Foundations of Computing" in detail.text
        assert "/start" in detail.text


def test_settings_read_tokens_paths_and_rag_thresholds_from_environment(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "custom.sqlite3"))
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "0.8")
    monkeypatch.setenv("RAG_MIN_MARGIN", "0.1")

    settings = get_settings()

    assert settings.telegram_bot_token == "test-token"
    assert settings.openai_api_key == "test-key"
    assert settings.database_path == tmp_path / "custom.sqlite3"
    assert settings.rag_min_similarity == 0.8
    assert settings.rag_min_margin == 0.1
