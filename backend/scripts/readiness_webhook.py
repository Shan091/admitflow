"""Expose only the existing Meta webhook through the temporary demo tunnel."""

import hashlib
import json
import logging
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from src.main import lifespan
from src.whatsapp.webhook import router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)
app.include_router(router, prefix="/api/webhook")


@app.middleware("http")
async def log_delivery_status(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Observe only authenticated status events, without recipient or error text."""
    body = await request.body() if request.method == "POST" else b""
    response = await call_next(request)
    if request.url.path != "/api/webhook" or response.status_code != 200 or not body:
        return response
    payload = json.loads(body)
    logger = logging.getLogger("uvicorn.error")
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for status in change.get("value", {}).get("statuses", []):
                state = status.get("status")
                if state not in {"sent", "delivered", "read", "failed", "deleted"}:
                    continue
                codes = [
                    error["code"]
                    for error in status.get("errors", [])
                    if isinstance(error.get("code"), int)
                ]
                reference = hashlib.sha256(str(status.get("id", "")).encode()).hexdigest()[:12]
                logger.info(
                    "whatsapp_delivery status=%s message_ref=%s error_codes=%s",
                    state,
                    reference,
                    codes,
                )
    return response
