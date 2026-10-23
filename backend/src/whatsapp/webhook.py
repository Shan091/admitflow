"""WhatsApp Webhook routing (Task 5).

Handles GET (challenge) and POST (incoming messages) from Meta.
Verifies HMAC signatures and enqueues to TaskIQ.
"""

from __future__ import annotations

import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Query, Request, Response

from src.core.redis import get_redis
from src.core.settings import get_settings
from src.tasks.processing import process_inbound_message

router = APIRouter(tags=["whatsapp-webhook"])


@router.get("")
async def verify_webhook(
    mode: str = Query(..., alias="hub.mode"),
    verify_token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge"),
) -> Response:
    """Handle Meta's webhook challenge."""
    settings = get_settings()
    if not settings.whatsapp_verify_token:
        raise HTTPException(status_code=500, detail="Webhook verify token not configured")

    if mode == "subscribe" and verify_token == settings.whatsapp_verify_token:
        # Must return the integer/string directly in text/plain
        return Response(content=challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive_message(
    request: Request,
    signature: str = Header(None, alias="X-Hub-Signature-256"),
) -> dict[str, str]:
    """Receive messages from Meta, verify signature, dedup, and enqueue."""
    settings = get_settings()
    if not settings.meta_app_secret:
        raise HTTPException(status_code=500, detail="Meta app secret not configured")

    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")

    # Read raw body for HMAC verification
    body = await request.body()
    expected_hash = hmac.new(settings.meta_app_secret.encode(), body, hashlib.sha256).hexdigest()

    expected_signature = f"sha256={expected_hash}"
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

    # Fast path: ignore statuses (read, delivered, sent)
    try:
        entries = payload.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})

                # Check for actual messages
                messages = value.get("messages", [])
                if not messages:
                    continue

                # In production, Meta usually sends 1 message per payload, but we iterate to be safe
                for msg in messages:
                    msg_id = msg.get("id")
                    if not msg_id:
                        continue

                    # Redis dedup (SETNX). TTL 24h (86400s)
                    # ADR-002: We don't enforce a DB-level UNIQUE constraint on wa_message_id
                    # to keep the failure modes clean when Redis is bypassed.
                    redis = get_redis()
                    acquired = await redis.set(f"webhook_dedup:{msg_id}", "1", nx=True, ex=86400)

                    if acquired:
                        # Pass the whole payload chunk (or just the value dict) to TaskIQ
                        # The TaskIQ worker will extract the sender phone and process it
                        await process_inbound_message.kiq(payload=value)

    except Exception:
        # We catch exceptions so we still return 200 OK.
        # Meta will retry if we return 500, leading to a flood of retries for bad payloads.
        pass

    # Always return 200 OK so Meta knows we got it
    return {"status": "ok"}
