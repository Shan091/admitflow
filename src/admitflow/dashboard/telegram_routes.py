"""Telegram webhook receiver for the running PTB application."""

import hmac
import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from telegram import Update
from telegram.ext import Application

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/v1/webhooks/telegram", status_code=200)
async def telegram_webhook(request: Request) -> dict[str, str]:
    """Authenticate and enqueue one Telegram update for PTB's background processor."""
    secret = request.app.state.settings.telegram_webhook_secret
    application: Application[Any, Any, Any, Any, Any, Any] | None = getattr(
        request.app.state, "telegram_application", None
    )
    if not secret or application is None:
        raise HTTPException(status_code=503, detail="Telegram webhook is not configured")

    supplied_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(supplied_secret, secret):
        raise HTTPException(status_code=401, detail="Invalid Telegram webhook secret")

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            raise ValueError("Update payload must be a JSON object")
        update = Update.de_json(payload, application.bot)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid Telegram update") from exc
    except Exception as exc:
        logger.warning("Unable to decode Telegram webhook update", exc_info=exc)
        raise HTTPException(status_code=400, detail="Invalid Telegram update") from exc

    await application.update_queue.put(update)
    return {"status": "queued"}
