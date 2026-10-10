import hashlib
import hmac
from pathlib import Path

from fastapi.testclient import TestClient

from admitflow.config import Settings, get_settings
from admitflow.main import create_app


def test_health_and_dashboard_require_staff_login(tmp_path: Path) -> None:
    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
        staff_username="demo-staff",
        staff_password="local-pass",
        staff_session_secret="test-session-secret-long-enough",
    )
    app = create_app(settings)

    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.get("/", follow_redirects=False).status_code == 303
        assert client.get("/login").status_code == 200
        rejected = client.post("/login", data={"username": "demo-staff", "password": "bad"})
        assert rejected.status_code == 401
        signed_in = client.post(
            "/login",
            data={"username": "demo-staff", "password": "local-pass"},
            follow_redirects=False,
        )
        assert signed_in.status_code == 303
        assert "httponly" in signed_in.headers["set-cookie"].casefold()
        dashboard = client.get("/", follow_redirects=True)
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
        assert "Application fee payment" in detail.text
        assert client.post("/logout", follow_redirects=False).status_code == 303
        assert client.get(f"/leads/{lead_id}", follow_redirects=False).status_code == 303


def test_dashboard_fails_closed_without_staff_configuration(tmp_path: Path) -> None:
    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
    )
    with TestClient(create_app(settings)) as client:
        assert client.get("/", follow_redirects=False).status_code == 303
        assert "not configured" in client.get("/login").text
        assert client.post("/login", data={"username": "x", "password": "y"}).status_code == 503


def test_razorpay_webhook_endpoint_checks_signature_and_accepts_test_event(tmp_path: Path) -> None:
    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
        razorpay_key_id="rzp_test_key",
        razorpay_key_secret="test-api-secret",
        razorpay_webhook_secret="test-webhook-secret",
    )
    body = b'{"event":"payment_link.paid"}'
    signature = hmac.new(b"test-webhook-secret", body, hashlib.sha256).hexdigest()
    with TestClient(create_app(settings)) as client:
        headers = {"X-Razorpay-Event-Id": "evt-1", "X-Razorpay-Signature": "wrong"}
        assert client.post("/webhooks/razorpay", content=body, headers=headers).status_code == 401
        headers["X-Razorpay-Signature"] = signature
        response = client.post("/webhooks/razorpay", content=body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"status": "ignored"}


def test_settings_read_tokens_paths_and_rag_thresholds_from_environment(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "custom.sqlite3"))
    monkeypatch.setenv("RAG_MIN_SIMILARITY", "0.8")
    monkeypatch.setenv("RAG_MIN_MARGIN", "0.1")
    monkeypatch.setenv("STAFF_USERNAME", "staff-user")
    monkeypatch.setenv("STAFF_PASSWORD", "staff-pass")
    monkeypatch.setenv("STAFF_SESSION_SECRET", "session-secret")
    monkeypatch.setenv("RAZORPAY_KEY_ID", "rzp_test_key")

    settings = get_settings()

    assert settings.telegram_bot_token == "test-token"
    assert settings.openai_api_key == "test-key"
    assert settings.database_path == tmp_path / "custom.sqlite3"
    assert settings.rag_min_similarity == 0.8
    assert settings.rag_min_margin == 0.1
    assert settings.staff_username == "staff-user"
    assert settings.staff_password == "staff-pass"
    assert settings.staff_session_secret == "session-secret"
    assert settings.razorpay_key_id == "rzp_test_key"
