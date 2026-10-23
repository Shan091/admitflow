"""The temporary tunnel must not expose local debug or documentation routes."""

import hashlib
import hmac
import json
import logging
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from scripts.readiness_webhook import app
from src.core.settings import Settings


@pytest.mark.parametrize("path", ["/", "/debug/enqueue-ping", "/docs", "/openapi.json", "/health"])
def test_tunnel_app_exposes_no_other_routes(path: str) -> None:
    assert TestClient(app).get(path).status_code == 404


def test_tunnel_app_keeps_webhook_verification() -> None:
    settings = Settings(_env_file=None, whatsapp_verify_token="synthetic", meta_app_secret="test")
    with patch("src.whatsapp.webhook.get_settings", return_value=settings):
        client = TestClient(app)
        params = {"hub.mode": "subscribe", "hub.verify_token": "synthetic", "hub.challenge": "123"}
        response = client.get("/api/webhook", params=params)
        assert response.status_code == 200
        assert response.text == "123"
        params["hub.verify_token"] = "wrong"
        assert client.get("/api/webhook", params=params).status_code == 403
        assert client.post("/api/webhook", json={}).status_code == 401


@pytest.mark.parametrize("valid_signature", [True, False])
def test_delivery_status_logs_are_authenticated_and_exclude_pii(
    caplog: pytest.LogCaptureFixture, valid_signature: bool
) -> None:
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "statuses": [
                                {
                                    "id": "wamid.synthetic",
                                    "status": "failed",
                                    "recipient_id": "919999999999",
                                    "errors": [
                                        {"code": 131030, "message": "private detail 919999999999"}
                                    ],
                                }
                            ]
                        }
                    }
                ]
            }
        ],
    }
    body = json.dumps(payload).encode()
    signature = hmac.new(b"test" if valid_signature else b"wrong", body, hashlib.sha256)
    settings = Settings(_env_file=None, meta_app_secret="test")
    with (
        patch("src.whatsapp.webhook.get_settings", return_value=settings),
        caplog.at_level(logging.INFO, logger="uvicorn.error"),
    ):
        response = TestClient(app).post(
            "/api/webhook",
            content=body,
            headers={"X-Hub-Signature-256": f"sha256={signature.hexdigest()}"},
        )
    assert response.status_code == (200 if valid_signature else 401)
    assert ("whatsapp_delivery status=failed" in caplog.text) is valid_signature
    if valid_signature:
        assert "131030" in caplog.text
    assert "919999999999" not in caplog.text
    assert "private detail" not in caplog.text
