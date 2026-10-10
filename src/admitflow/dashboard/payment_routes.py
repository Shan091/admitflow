"""Public Razorpay webhook endpoint; provider signatures authenticate callbacks."""

import json
import logging

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()
logger = logging.getLogger(__name__)

PAYMENT_SUCCESS_MESSAGE = (
    "✅ Payment successful! Your demo application fee is confirmed and your application is "
    "recorded. Next, admissions staff can review it and share course access steps. "
    "Course access is not provisioned automatically in this demo."
)


@router.post("/webhooks/razorpay")
@router.post("/api/v1/webhooks/razorpay")
async def razorpay_webhook(request: Request) -> dict[str, str]:
    payment_service = getattr(request.app.state, "payment_service", None)
    if payment_service is None:
        raise HTTPException(status_code=503, detail="Razorpay webhook is not configured")
    signature = request.headers.get("X-Razorpay-Signature", "")
    event_id = request.headers.get("X-Razorpay-Event-Id", "")
    if not signature or not event_id or len(event_id) > 255:
        raise HTTPException(status_code=400, detail="Missing Razorpay webhook headers")
    try:
        result = payment_service.apply_webhook(await request.body(), signature, event_id)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    if result == "applied":
        repository = getattr(request.app.state, "repository", None)
        telegram_application = getattr(request.app.state, "telegram_application", None)
        if repository is not None and telegram_application is not None:
            event = json.loads(await request.body())
            payment_link = event.get("payload", {}).get("payment_link", {}).get("entity", {})
            link_id = payment_link.get("id") if isinstance(payment_link, dict) else None
            user_id = (
                repository.get_telegram_user_for_payment_link(link_id)
                if isinstance(link_id, str)
                else None
            )
            if user_id is not None and user_id.isdigit():
                try:
                    await telegram_application.bot.send_message(
                        chat_id=int(user_id), text=PAYMENT_SUCCESS_MESSAGE
                    )
                except Exception:
                    logger.exception("Could not send Telegram payment confirmation to lead")
    return {"status": result}
