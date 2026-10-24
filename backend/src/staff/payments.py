"""Scoped payment monitoring and explicit, read-only provider reconciliation."""

import uuid
from typing import Any

from cryptography.fernet import InvalidToken
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, update

from src.core.demo_admissions import demo_fee
from src.core.security import EncryptionKeyNotConfiguredError, decrypt_pii, encrypt_pii
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.enums import PaymentStatus
from src.db.models import Course, Institution, Lead, OutboundMessage, PaymentOrder
from src.engine.contracts import Reply
from src.payments.provider import Credentials, PaymentProviderError, RazorpayClient
from src.staff.auth import Db, Staff, require_admin, require_browser_write
from src.telegram.outbound import enqueue_outbound

router = APIRouter(prefix="/api/staff/payments", tags=["staff payments"])


async def owned(db: Db, staff: Staff, order_id: uuid.UUID) -> PaymentOrder:
    order = await db.scalar(
        select(PaymentOrder).where(
            PaymentOrder.id == order_id, PaymentOrder.tenant_id == staff.tenant_id
        )
    )
    if order is None:
        raise HTTPException(404, "Payment not found.")
    return order


async def locked(db: Db, staff: Staff, order_id: uuid.UUID) -> PaymentOrder:
    order = await owned(db, staff, order_id)
    await db.scalar(
        select(Lead)
        .where(Lead.id == order.lead_id, Lead.tenant_id == staff.tenant_id)
        .with_for_update()
    )
    await db.refresh(order, with_for_update=True)
    return order


async def provider(db: Db, staff: Staff) -> RazorpayClient:
    institution = await db.get(Institution, staff.tenant_id)
    try:
        if institution is None or not institution.razorpay_credentials_enc:
            raise ValueError("Missing configuration")
        credentials = Credentials.model_validate_json(
            decrypt_pii(institution.razorpay_credentials_enc)
        )
        settings = get_settings()
        return RazorpayClient(
            credentials, allow_live=settings.app_env == "prod" and settings.payments_live_enabled
        )
    except (ValueError, InvalidToken, EncryptionKeyNotConfiguredError):
        raise HTTPException(
            409, "Payment credentials are unavailable for this institution."
        ) from None


@router.get("")
async def payments(
    staff: Staff, db: Db, offset: int = Query(default=0, ge=0), status: PaymentStatus | None = None
) -> list[dict[str, Any]]:
    statement = select(PaymentOrder).where(PaymentOrder.tenant_id == staff.tenant_id)
    if status is not None:
        statement = statement.where(PaymentOrder.status == status)
    orders = (
        await db.scalars(
            statement.order_by(PaymentOrder.created_at.desc(), PaymentOrder.id)
            .offset(offset)
            .limit(50)
        )
    ).all()
    # One bounded query for delivery state; never expose the bearer payment URL.
    keys = [f"payment-link:{order.id}" for order in orders]
    deliveries = dict(
        (
            await db.execute(
                select(OutboundMessage.dedup_key, OutboundMessage.status).where(
                    OutboundMessage.tenant_id == staff.tenant_id,
                    OutboundMessage.dedup_key.in_(keys),
                )
            )
        ).all()
    )
    await write_audit_log(
        db, tenant_id=staff.tenant_id, actor=str(staff.id), action="staff.payments_viewed"
    )
    await db.commit()
    return [
        {
            "id": str(order.id),
            "lead_id": str(order.lead_id),
            "application_id": str(order.application_id),
            "amount": order.amount,
            "is_demo": order.is_demo,
            "currency": order.currency,
            "status": order.status.value,
            "creation_state": order.creation_state,
            "attempts": order.creation_attempts,
            "error_code": order.last_error,
            "link_sent": order.payment_link_sent,
            "delivery_status": deliveries.get(f"payment-link:{order.id}"),
            "created_at": order.created_at.isoformat(),
        }
        for order in orders
    ]


@router.post("/{order_id}/reconcile", dependencies=[Depends(require_browser_write)])
async def reconcile(order_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    order = await owned(db, staff, order_id)
    if order.status in {PaymentStatus.PAID, PaymentStatus.WAIVED}:
        return {"result": "already_settled"}
    if order.creation_state in {"queued", "creating", "legacy"}:
        raise HTTPException(409, "This invoice is not available for provider reconciliation.")
    if order.is_demo:
        course = await db.scalar(
            select(Course).where(
                Course.id == order.course_id,
                Course.tenant_id == staff.tenant_id,
            )
        )
        if course is None or await demo_fee(db, course) is None:
            raise HTTPException(409, "Demo provider checks require the enabled test configuration.")
    if order.is_demo and order.razorpay_payment_link_id:
        from src.payments.demo import check_demo_payment

        await write_audit_log(
            db,
            tenant_id=staff.tenant_id,
            actor=str(staff.id),
            action="payment.lookup_requested",
            lead_id=order.lead_id,
            details={"payment_order_id": str(order.id), "is_demo": True},
        )
        await db.commit()
        try:
            confirmed = await check_demo_payment(order.id)
        except PaymentProviderError:
            raise HTTPException(
                502, "Test payment lookup unavailable. The invoice is unchanged."
            ) from None
        return {"result": "test_payment_confirmed" if confirmed else "test_payment_pending"}
    client = await provider(db, staff)
    amount = order.amount
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="payment.lookup_requested",
        lead_id=order.lead_id,
        details={"payment_order_id": str(order.id)},
    )
    await db.commit()  # No database lock or transaction held over provider I/O.
    try:
        link = await client.find_link(order_id.hex, amount)
    except PaymentProviderError:
        raise HTTPException(
            502, "Provider lookup failed. No new payment link was requested."
        ) from None
    order = await locked(db, staff, order_id)
    if order.status in {PaymentStatus.PAID, PaymentStatus.WAIVED}:
        return {"result": "already_settled"}
    if order.amount != amount or order.creation_state in {"queued", "creating"}:
        raise HTTPException(409, "The invoice changed during lookup. Reload before continuing.")
    result = "not_found"
    if link is not None:
        if order.razorpay_payment_link_id and order.razorpay_payment_link_id != link.id:
            raise HTTPException(409, "The provider reference does not match this invoice.")
        order.razorpay_payment_link_id = link.id
        order.payment_url_enc = encrypt_pii(link.short_url)
        if link.status == "created":
            order.creation_state, order.last_error = "created", None
            await enqueue_outbound(
                db,
                tenant_id=staff.tenant_id,
                lead_id=order.lead_id,
                kind="payment_link",
                dedup_key=f"payment-link:{order.id}",
                reply=Reply(
                    text=(
                        f"Demo application fee: INR {amount / 100:.2f}. Razorpay TEST mode. "
                        f"Use test payment details only: {link.short_url}"
                    )
                    if order.is_demo
                    else (
                        f"Your application fee is INR {amount / 100:.2f}. "
                        f"Open the institution's payment link: {link.short_url}\n"
                        "Payment is an application fee, not admission or a seat reservation."
                    )
                ),
            )
            result = "link_recovered"
        elif link.status in {"paid", "partially_paid"}:
            order.creation_state = "created"
            order.last_error = (
                "awaiting_test_confirmation" if order.is_demo else "awaiting_signed_confirmation"
            )
            result = "test_payment_pending" if order.is_demo else "awaiting_signed_confirmation"
        else:
            order.creation_state, order.last_error = "failed", f"provider_{link.status}"
            result = "link_unavailable"
        if link.status != "created":
            await db.execute(
                update(OutboundMessage)
                .where(
                    OutboundMessage.tenant_id == staff.tenant_id,
                    OutboundMessage.lead_id == order.lead_id,
                    OutboundMessage.dedup_key == f"payment-link:{order.id}",
                    OutboundMessage.status == "queued",
                )
                .values(status="failed", error_code="payment_link_unavailable")
            )
    # Not found is not evidence that the earlier POST failed. Retain uncertainty.
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="payment.lookup_completed",
        lead_id=order.lead_id,
        details={"payment_order_id": str(order.id), "result": result},
    )
    await db.commit()
    return {"result": result}


@router.post("/{order_id}/retry", dependencies=[Depends(require_browser_write)])
async def retry(order_id: uuid.UUID, staff: Staff, db: Db) -> dict[str, str]:
    require_admin(staff)
    order = await locked(db, staff, order_id)
    if (
        order.creation_state != "failed"
        or order.status != PaymentStatus.CREATED
        or order.last_error not in {"configuration_unavailable", "provider_429"}
        or order.creation_attempts >= 3
        or order.razorpay_payment_link_id
    ):
        raise HTTPException(409, "This request cannot be retried safely. Use provider lookup.")
    await provider(db, staff)  # Validate the replacement configuration before requeueing.
    order.creation_state, order.last_error, order.next_attempt_at = "queued", None, None
    await write_audit_log(
        db,
        tenant_id=staff.tenant_id,
        actor=str(staff.id),
        action="payment.retry_requested",
        lead_id=order.lead_id,
        details={"payment_order_id": str(order.id)},
    )
    await db.commit()
    return {"result": "queued"}
