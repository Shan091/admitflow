"""Raw-body authenticated, amount-checked and replay-safe payment confirmation."""

import json
import uuid

from cryptography.fernet import InvalidToken
from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from src.core.security import EncryptionKeyNotConfiguredError, decrypt_pii
from src.db.models import Institution
from src.payments.confirmation import PaidEvent, settle_payment
from src.payments.provider import Credentials
from src.payments.rules import verify_webhook
from src.staff.auth import Db

router = APIRouter(prefix="/api/payments", tags=["payment webhooks"])


@router.post("/webhook/{tenant_id}")
async def payment_webhook(tenant_id: uuid.UUID, request: Request, db: Db) -> dict[str, str]:
    body = bytearray()
    async for chunk in request.stream():
        body.extend(chunk)
        if len(body) > 256 * 1024:
            raise HTTPException(413, "Payment event is too large.")
    institution = await db.get(Institution, tenant_id)
    if institution is None or not institution.razorpay_credentials_enc:
        raise HTTPException(404, "Payment endpoint not configured.")
    try:
        credentials = Credentials.model_validate_json(
            decrypt_pii(institution.razorpay_credentials_enc)
        )
    except (ValueError, InvalidToken, EncryptionKeyNotConfiguredError):
        raise HTTPException(503, "Payment verification is unavailable.") from None
    raw = bytes(body)
    if not verify_webhook(
        raw,
        request.headers.get("x-razorpay-signature", ""),
        credentials.webhook_secret.get_secret_value(),
    ):
        raise HTTPException(401, "Invalid payment signature.")
    try:
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError("Expected event object")
        if value.get("event") != "payment_link.paid":
            return {"status": "ignored"}
        event = PaidEvent.model_validate(value)
    except (ValueError, ValidationError):
        raise HTTPException(400, "Malformed payment event.") from None
    return await settle_payment(tenant_id, event, raw, db)
