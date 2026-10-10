"""Public Razorpay webhook endpoint; provider signatures authenticate callbacks."""

from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.post("/webhooks/razorpay")
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
    return {"status": result}
