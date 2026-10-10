import hashlib
import hmac
import json
from pathlib import Path
from types import SimpleNamespace

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
        response = client.post("/api/v1/webhooks/razorpay", content=body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"status": "ignored"}


def test_paid_webhook_sends_one_telegram_confirmation_with_next_step(tmp_path: Path) -> None:
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
    app = create_app(settings)

    class FakeBot:
        def __init__(self) -> None:
            self.sent: list[tuple[int, str]] = []

        async def send_message(self, *, chat_id: int, text: str) -> None:
            self.sent.append((chat_id, text))

    bot = FakeBot()
    body = json.dumps(
        {
            "event": "payment_link.paid",
            "payload": {
                "payment_link": {
                    "entity": {
                        "id": "plink_test_123",
                        "reference_id": "AF-test-reference",
                        "status": "paid",
                        "amount": 50000,
                        "amount_paid": 50000,
                        "currency": "INR",
                    }
                }
            },
        }
    ).encode()
    signature = hmac.new(b"test-webhook-secret", body, hashlib.sha256).hexdigest()

    with TestClient(app) as client:
        repository = app.state.repository
        lead_id = repository.upsert_lead(repository.tenant_id, "42", "sample")
        repository.update_lead(lead_id, selected_course_id="foundations-computing", eligible=True)
        payment, created = repository.get_or_create_payment_intent(
            repository.tenant_id, lead_id, "AF-test-reference"
        )
        assert created and payment is not None
        repository.save_payment_link(payment["id"], "plink_test_123", "https://rzp.io/i/test123")
        app.state.telegram_application = SimpleNamespace(bot=bot)
        headers = {
            "X-Razorpay-Event-Id": "evt-paid-confirmation",
            "X-Razorpay-Signature": signature,
        }

        response = client.post("/api/v1/webhooks/razorpay", content=body, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"status": "applied"}
        assert len(bot.sent) == 1
        chat_id, message = bot.sent[0]
        assert chat_id == 42
        assert "Payment successful" in message
        assert "reach out soon with course access instructions" in message
        assert "not automatically enabled" in message

        duplicate = client.post("/api/v1/webhooks/razorpay", content=body, headers=headers)
        assert duplicate.json() == {"status": "duplicate"}
        assert len(bot.sent) == 1


def test_settings_read_tokens_paths_and_rag_thresholds_from_environment(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_WEBHOOK_SECRET", "webhook-secret")
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
    assert settings.telegram_webhook_secret == "webhook-secret"
    assert settings.openai_api_key == "test-key"
    assert settings.database_path == tmp_path / "custom.sqlite3"
    assert settings.rag_min_similarity == 0.8
    assert settings.rag_min_margin == 0.1
    assert settings.staff_username == "staff-user"
    assert settings.staff_password == "staff-pass"
    assert settings.staff_session_secret == "session-secret"
    assert settings.razorpay_key_id == "rzp_test_key"


def test_telegram_webhook_requires_configured_application_and_secret(tmp_path: Path) -> None:
    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
        telegram_webhook_secret="webhook-secret",
    )
    with TestClient(create_app(settings)) as client:
        assert (
            client.post(
                "/api/v1/webhooks/telegram",
                json={"update_id": 123},
                headers={"X-Telegram-Bot-Api-Secret-Token": "webhook-secret"},
            ).status_code
            == 503
        )


def test_telegram_application_uses_webhook_lifecycle_only_with_both_secrets(
    tmp_path: Path, monkeypatch
) -> None:
    from admitflow import main

    started: list[object] = []
    stopped: list[object] = []
    fake_application = object()

    monkeypatch.setattr(main, "build_telegram_application", lambda *args: fake_application)

    async def start(application) -> None:
        started.append(application)

    async def stop(application) -> None:
        stopped.append(application)

    monkeypatch.setattr(main, "start_application", start)
    monkeypatch.setattr(main, "stop_application", stop)
    settings = Settings(
        telegram_bot_token="test-bot-token",
        telegram_webhook_secret="webhook-secret",
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
    )
    app = create_app(settings)

    with TestClient(app):
        assert app.state.telegram_enabled
        assert app.state.telegram_application is fake_application

    assert started == [fake_application]
    assert stopped == [fake_application]

    incomplete_settings = Settings(
        telegram_bot_token="test-bot-token",
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "incomplete.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
    )
    incomplete_app = create_app(incomplete_settings)
    with TestClient(incomplete_app):
        assert not incomplete_app.state.telegram_enabled
        assert incomplete_app.state.telegram_application is None
    assert started == [fake_application]
    assert stopped == [fake_application]


def test_telegram_webhook_authenticates_and_queues_valid_updates(tmp_path: Path) -> None:
    from types import SimpleNamespace

    from telegram import Update

    settings = Settings(
        telegram_bot_token=None,
        openai_api_key=None,
        openai_decisions_model="gpt-6-luna",
        openai_embedding_model="text-embedding-3-small",
        database_path=tmp_path / "demo.sqlite3",
        rag_min_similarity=0.72,
        rag_min_margin=0.05,
        telegram_webhook_secret="webhook-secret",
    )
    app = create_app(settings)

    class FakeQueue:
        def __init__(self) -> None:
            self.items: list[Update] = []

        async def put(self, update: Update) -> None:
            self.items.append(update)

    queue = FakeQueue()

    with TestClient(app) as client:
        app.state.telegram_application = SimpleNamespace(bot=object(), update_queue=queue)
        path = "/api/v1/webhooks/telegram"
        assert client.post(path, json={"update_id": 123}).status_code == 401
        rejected = client.post(
            path,
            json={"update_id": 123},
            headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"},
        )
        assert rejected.status_code == 401
        malformed = client.post(
            path,
            json=[],
            headers={"X-Telegram-Bot-Api-Secret-Token": "webhook-secret"},
        )
        assert malformed.status_code == 400
        accepted = client.post(
            path,
            json={"update_id": 123},
            headers={"X-Telegram-Bot-Api-Secret-Token": "webhook-secret"},
        )

    assert accepted.status_code == 200
    assert accepted.json() == {"status": "queued"}
    assert len(queue.items) == 1
    assert queue.items[0].update_id == 123
