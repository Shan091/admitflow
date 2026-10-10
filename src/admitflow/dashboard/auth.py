"""Small signed-cookie helpers for the single-staff demo dashboard."""

import base64
import hashlib
import hmac
import json
import secrets
import time

SESSION_COOKIE = "admitflow_staff"
SESSION_MAX_AGE = 8 * 60 * 60


def create_session(username: str, secret: str, now: int | None = None) -> str:
    payload = json.dumps(
        {
            "username": username,
            "expires": (int(time.time()) if now is None else now) + SESSION_MAX_AGE,
            "nonce": secrets.token_urlsafe(12),
        },
        separators=(",", ":"),
    ).encode()
    encoded = base64.urlsafe_b64encode(payload).rstrip(b"=").decode()
    signature = hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"


def verify_session(
    token: str | None, username: str | None, secret: str | None, now: int | None = None
) -> bool:
    if not token or not username or not secret or "." not in token:
        return False
    encoded, supplied_signature = token.rsplit(".", 1)
    expected_signature = hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(supplied_signature, expected_signature):
        return False
    try:
        padding = "=" * (-len(encoded) % 4)
        payload = json.loads(base64.urlsafe_b64decode(encoded + padding))
    except (ValueError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict):
        return False
    current_time = int(time.time()) if now is None else now
    return (
        payload.get("username") == username
        and isinstance(payload.get("expires"), int)
        and payload["expires"] > current_time
    )


def create_delete_demo_data_token(session_cookie: str, secret: str) -> str:
    """Bind the destructive form token to the authenticated staff session."""
    message = f"delete-demo-data:{session_cookie}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()


def create_delete_lead_token(session_cookie: str, lead_id: int, secret: str) -> str:
    """Bind an individual deletion form token to its staff session and target lead."""
    message = f"delete-lead:{lead_id}:{session_cookie}".encode()
    return hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
