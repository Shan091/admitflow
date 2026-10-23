"""Raw-body authenticated, amount-checked and replay-safe payment confirmation."""

import hashlib
import json
import uuid
from typing import Literal

from cryptography.fernet import InvalidToken
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from src.core.security import EncryptionKeyNotConfiguredError, decrypt_pii
from src.db.audit import write_audit_log
from src.db.enums import ApplicationStatus, LeadStatus, PaymentStatus
from src.db.models import (
    Application,
    DiscountCode,
    Institution,
    Lead,
    OutboundMessage,
    PaymentEvent,
    PaymentOrder,
)
from src.engine.contracts import Reply
from src.payments.provider import Credentials
from src.payments.rules import verify_webhook
from src.staff.auth import Db
from src.telegram.outbound import enqueue_outbound

router = APIRouter(prefix="/api/payments", tags=["payment webhooks"])


class LinkEntity(BaseModel):
    id: str = Field(pattern=r"^plink_[A-Za-z0-9]+$")
    reference_id: uuid.UUID
    amount: int = Field(ge=100, strict=True)
    amount_paid: int = Field(ge=100, strict=True)
    currency: Literal["INR"]
    status: Literal["paid"]


class PaymentEntity(BaseModel):
    id: str = Field(pattern=r"^pay_[A-Za-z0-9]+$")
    amount: int = Field(ge=100, strict=True)
    currency: Literal["INR"]
    status: Literal["captured"]


class LinkEnvelope(BaseModel):
    entity: LinkEntity


class PaymentEnvelope(BaseModel):
    entity: PaymentEntity


class PaidPayload(BaseModel):
    payment_link: LinkEnvelope
    payment: PaymentEnvelope


class PaidEvent(BaseModel):
    event: Literal["payment_link.paid"]
    payload: PaidPayload


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
    link, payment = event.payload.payment_link.entity, event.payload.payment.entity
    reference = (
        await db.execute(
            select(PaymentOrder.id, PaymentOrder.lead_id).where(
                PaymentOrder.tenant_id == tenant_id, PaymentOrder.id == link.reference_id
            )
        )
    ).first()
    if reference is None:
        raise HTTPException(404, "Payment reference not found.")
    lead = await db.scalar(
        select(Lead)
        .where(Lead.id == reference.lead_id, Lead.tenant_id == tenant_id)
        .with_for_update()
    )
    order = await db.scalar(
        select(PaymentOrder)
        .where(PaymentOrder.id == reference.id, PaymentOrder.tenant_id == tenant_id)
        .with_for_update()
    )
    if lead is None or order is None:
        raise HTTPException(404, "Payment reference not found.")
    if (
        order.amount != link.amount
        or order.amount != link.amount_paid
        or order.amount != payment.amount
        or order.currency != link.currency
        or order.currency != payment.currency
        or (order.razorpay_payment_link_id and order.razorpay_payment_link_id != link.id)
    ):
        raise HTTPException(409, "Payment details do not match the invoice.")
    if order.status == PaymentStatus.WAIVED:
        raise HTTPException(409, "This application fee was waived.")
    if order.status == PaymentStatus.PAID and order.razorpay_payment_id != payment.id:
        raise HTTPException(409, "A different payment is already recorded for this invoice.")
    digest = hashlib.sha256(raw).hexdigest()
    if await db.scalar(
        select(PaymentEvent.id).where(
            PaymentEvent.tenant_id == tenant_id, PaymentEvent.body_digest == digest
        )
    ):
        return {"status": "duplicate"}
    application = await db.scalar(
        select(Application)
        .where(
            Application.id == order.application_id,
            Application.tenant_id == tenant_id,
            Application.lead_id == lead.id,
        )
        .with_for_update()
    )
    if application is None:
        raise HTTPException(404, "Application not found.")
    already_paid = order.status == PaymentStatus.PAID
    try:
        await db.execute(
            update(OutboundMessage)
            .where(
                OutboundMessage.tenant_id == tenant_id,
                OutboundMessage.lead_id == lead.id,
                OutboundMessage.dedup_key == f"payment-link:{order.id}",
                OutboundMessage.status == "queued",
            )
            .values(status="failed", error_code="payment_already_settled")
        )
        if not already_paid:
            order.status = PaymentStatus.PAID
            order.creation_state = "created"
            order.razorpay_payment_link_id = link.id
            order.razorpay_payment_id = payment.id
            order.last_error = None
            order.webhook_event = {
                "event": event.event,
                "body_digest": digest,
                "amount": payment.amount,
                "currency": payment.currency,
                "payment_id": payment.id,
            }
            if order.discount_code_id:
                discount = await db.scalar(
                    select(DiscountCode)
                    .where(
                        DiscountCode.id == order.discount_code_id,
                        DiscountCode.tenant_id == tenant_id,
                    )
                    .with_for_update()
                )
                if discount:
                    discount.uses_count += 1
            if application.status == ApplicationStatus.SUBMITTED:
                application.status = ApplicationStatus.UNDER_REVIEW
                if lead.status != LeadStatus.HANDED_OFF:
                    lead.status = LeadStatus.UNDER_REVIEW
            await enqueue_outbound(
                db,
                tenant_id=tenant_id,
                lead_id=lead.id,
                kind="payment_paid",
                dedup_key=f"payment-paid:{order.id}",
                reply=Reply(
                    text=f"Payment received: INR {order.amount / 100:.2f}. "
                    "Your institution can review the application. "
                    "Payment does not grant admission or reserve a seat."
                ),
            )
            await write_audit_log(
                db,
                tenant_id=tenant_id,
                actor="razorpay-webhook",
                action="payment.confirmed",
                lead_id=lead.id,
                details={"payment_order_id": str(order.id)},
            )
        db.add(
            PaymentEvent(
                tenant_id=tenant_id, payment_order_id=order.id, body_digest=digest, kind=event.event
            )
        )
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "This payment transaction is already recorded.") from None
    return {"status": "confirmed" if not already_paid else "duplicate"}
