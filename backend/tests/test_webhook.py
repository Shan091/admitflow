"""Tests for the Meta WhatsApp webhook endpoints (Task 5)."""

from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


# Fixture for a test app with the webhook router mounted
@pytest.fixture
def app() -> FastAPI:
    from src.whatsapp.webhook import router

    app_ = FastAPI()
    app_.include_router(router, prefix="/api/webhook")
    return app_


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def mock_settings() -> Generator[AsyncMock, None, None]:
    with patch("src.whatsapp.webhook.get_settings") as mock:
        mock.return_value.meta_app_secret = "test_secret"
        mock.return_value.whatsapp_verify_token = "test_token"
        yield mock


def sign_payload(payload: dict[str, Any], secret: str = "test_secret") -> str:
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


class TestWebhookVerification:
    """GET /api/webhook challenge verification."""

    def test_verify_success(self, client: TestClient) -> None:
        response = client.get(
            "/api/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "test_token",
                "hub.challenge": "123456789",
            },
        )
        assert response.status_code == 200
        # FastAPI returns integer responses as JSON by default, but Meta expects raw text/integer
        # TestClient might decode it. We'll check the text.
        assert response.text == "123456789"

    def test_verify_invalid_token(self, client: TestClient) -> None:
        response = client.get(
            "/api/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong_token",
                "hub.challenge": "123456789",
            },
        )
        assert response.status_code == 403

    def test_verify_missing_params(self, client: TestClient) -> None:
        response = client.get("/api/webhook")
        assert response.status_code == 422


class TestWebhookProcessing:
    """POST /api/webhook payload processing."""

    @pytest.fixture(autouse=True)
    def mock_redis(self) -> Generator[AsyncMock, None, None]:
        with patch("src.whatsapp.webhook.get_redis") as mock_get_redis:
            mock_redis_client = AsyncMock()
            mock_redis_client.set.return_value = True  # True means acquired SETNX
            mock_get_redis.return_value = mock_redis_client
            yield mock_redis_client

    @pytest.fixture
    def mock_task_kiq(self) -> Generator[AsyncMock, None, None]:
        with patch("src.whatsapp.webhook.process_inbound_message.kiq") as mock:
            yield mock

    def test_post_success(
        self, client: TestClient, mock_redis: AsyncMock, mock_task_kiq: AsyncMock
    ) -> None:
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "123",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "1234",
                                    "phone_number_id": "5678",
                                },
                                "contacts": [
                                    {"profile": {"name": "Test"}, "wa_id": "919876543210"}
                                ],
                                "messages": [
                                    {
                                        "from": "919876543210",
                                        "id": "wamid.123",
                                        "timestamp": "1234567890",
                                        "type": "text",
                                        "text": {"body": "Hello"},
                                    }
                                ],
                            },
                            "field": "messages",
                        }
                    ],
                }
            ],
        }

        body = json.dumps(payload, separators=(",", ":"))
        signature = sign_payload(payload)

        response = client.post(
            "/api/webhook", content=body, headers={"X-Hub-Signature-256": signature}
        )

        assert response.status_code == 200

        # Redis SETNX should be called with the message ID
        mock_redis.set.assert_called_once()
        assert mock_redis.set.call_args.args[0] == "webhook_dedup:wamid.123"
        assert mock_redis.set.call_args.kwargs["nx"] is True

        # The task should be enqueued
        mock_task_kiq.assert_called_once()
        # The first arg should be the message payload, the second the raw wa_id
        enqueued_payload = mock_task_kiq.call_args.kwargs["payload"]
        assert enqueued_payload["messages"][0]["id"] == "wamid.123"
        assert enqueued_payload["contacts"][0]["wa_id"] == "919876543210"

    def test_post_invalid_signature(self, client: TestClient) -> None:
        payload = {"object": "whatsapp_business_account"}
        response = client.post(
            "/api/webhook", json=payload, headers={"X-Hub-Signature-256": "sha256=invalid"}
        )
        assert response.status_code == 401

    def test_post_missing_signature(self, client: TestClient) -> None:
        response = client.post("/api/webhook", json={})
        assert response.status_code == 401

    def test_post_duplicate_message_dropped(
        self, client: TestClient, mock_redis: AsyncMock, mock_task_kiq: AsyncMock
    ) -> None:
        # Mock Redis SETNX to return None/False (meaning key already exists)
        mock_redis.set.return_value = None

        payload = {
            "object": "whatsapp_business_account",
            "entry": [{"changes": [{"value": {"messages": [{"id": "wamid.duplicate"}]}}]}],
        }

        response = client.post(
            "/api/webhook",
            content=json.dumps(payload, separators=(",", ":")),
            headers={"X-Hub-Signature-256": sign_payload(payload)},
        )

        # We must return 200 OK so Meta stops retrying, but we don't process it
        assert response.status_code == 200
        mock_task_kiq.assert_not_called()

    def test_post_no_messages_in_payload(
        self, client: TestClient, mock_task_kiq: AsyncMock
    ) -> None:
        """Statuses (read/delivered) have no 'messages' array."""
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {"changes": [{"value": {"statuses": [{"id": "wamid.123", "status": "read"}]}}]}
            ],
        }

        response = client.post(
            "/api/webhook",
            content=json.dumps(payload, separators=(",", ":")),
            headers={"X-Hub-Signature-256": sign_payload(payload)},
        )

        # Should just ack and return 200
        assert response.status_code == 200
        mock_task_kiq.assert_not_called()
