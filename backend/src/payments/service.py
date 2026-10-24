"""Explicit fee requests, immutable invoices and recoverable payment-link creation."""

import uuid
from datetime import UTC, datetime, timedelta

from cryptography.fernet import InvalidToken
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import EncryptionKeyNotConfiguredError, decrypt_pii, encrypt_pii
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.enums import ApplicationStatus, DiscountType, LeadStatus, PaymentStatus
from src.db.models import Application, Batch, Course, DiscountCode, Institution, Lead, PaymentOrder
from src.db.session import get_sessionmaker
from src.engine.contracts import Reply
from src.payments.provider import Credentials, PaymentProviderError, RazorpayClient
from src.payments.rules import discounted_amount
from src.telegram.outbound import enqueue_outbound


class PaymentRequestError(ValueError):
    """A safe, actionable request error; never contains a provider payload."""


async def existing_payment(
    db: AsyncSession, lead: Lead, application_id: uuid.UUID
) -> PaymentOrder | None:
    settled = await db.scalar(
        select(PaymentOrder)
        .where(
            PaymentOrder.tenant_id == lead.tenant_id,
            PaymentOrder.application_id == application_id,
            PaymentOrder.lead_id == lead.id,
            PaymentOrder.status.in_([PaymentStatus.PAID, PaymentStatus.WAIVED]),
        )
        .order_by(PaymentOrder.created_at.desc())
        .limit(1)
    )
    if settled:
        return settled
    return await db.scalar(
        select(PaymentOrder)
        .where(
            PaymentOrder.tenant_id == lead.tenant_id,
            PaymentOrder.application_id == application_id,
            PaymentOrder.lead_id == lead.id,
        )
        .order_by(PaymentOrder.created_at.desc())
        .limit(1)
    )


async def fee_details(
    db: AsyncSession, lead: Lead, application_id: uuid.UUID, code: str | None = None
) -> tuple[Application, Course, int, DiscountCode | None]:
    application = await db.scalar(
        select(Application)
        .where(
            Application.id == application_id,
            Application.tenant_id == lead.tenant_id,
            Application.lead_id == lead.id,
        )
        .with_for_update()
    )
    if application is None or application.status in {
        ApplicationStatus.APPROVED,
        ApplicationStatus.REJECTED,
    }:
        raise PaymentRequestError("This application is not available for a new payment.")
    course = await db.scalar(
        select(Course).where(
            Course.tenant_id == lead.tenant_id,
            Course.id == application.course_id,
            Course.is_active.is_(True),
            Course.is_reference.is_(False),
        )
    )
    batch = await db.scalar(
        select(Batch.id).where(
            Batch.tenant_id == lead.tenant_id,
            Batch.id == application.batch_id,
            Batch.course_id == application.course_id,
            Batch.is_active.is_(True),
            Batch.seats_remaining > 0,
        )
    )
    if course is None or batch is None:
        raise PaymentRequestError(
            "The course or batch is unavailable. Request staff review before paying."
        )
    discount = None
    amount = course.application_fee
    if code:
        discount = await db.scalar(
            select(DiscountCode)
            .where(
                DiscountCode.tenant_id == lead.tenant_id,
                DiscountCode.code == code.strip().upper(),
                DiscountCode.is_active.is_(True),
            )
            .with_for_update()
        )
        now = datetime.now(UTC)
        if (
            discount is None
            or (discount.valid_from and discount.valid_from > now)
            or (discount.valid_until and discount.valid_until <= now)
        ):
            raise PaymentRequestError("That discount code is not currently valid.")
        pending = await db.scalar(
            select(func.count())
            .select_from(PaymentOrder)
            .where(
                PaymentOrder.tenant_id == lead.tenant_id,
                PaymentOrder.discount_code_id == discount.id,
                PaymentOrder.status.not_in(
                    [PaymentStatus.PAID, PaymentStatus.WAIVED, PaymentStatus.FAILED]
                ),
                PaymentOrder.creation_state != "failed",
            )
        )
        if (
            discount.max_uses is not None
            and discount.uses_count + int(pending or 0) >= discount.max_uses
        ):
            raise PaymentRequestError("That discount code has reached its usage limit.")
        amount = discounted_amount(
            amount,
            "percent" if discount.discount_type == DiscountType.PERCENT else "flat",
            discount.amount,
        )
    return application, course, amount, discount


async def request_payment(
    db: AsyncSession, lead: Lead, application_id: uuid.UUID, code: str | None = None
) -> PaymentOrder:
    existing = await existing_payment(db, lead, application_id)
    if existing:
        return existing
    application, course, amount, discount = await fee_details(db, lead, application_id, code)
    if 0 < amount < 100:
        raise PaymentRequestError("The payable fee is below INR 1. Request staff review.")
    institution = await db.get(Institution, lead.tenant_id)
    if amount and (institution is None or not institution.razorpay_credentials_enc):
        raise PaymentRequestError(
            "Online payments are not available yet. Your application is saved."
        )
    order = PaymentOrder(
        id=uuid.uuid4(),
        tenant_id=lead.tenant_id,
        lead_id=lead.id,
        application_id=application.id,
        course_id=course.id,
        discount_code_id=discount.id if discount else None,
        amount=amount,
        currency="INR",
        request_key=application_id.hex,
        creation_state="queued" if amount else "created",
        creation_attempts=0,
        status=PaymentStatus.CREATED if amount else PaymentStatus.WAIVED,
    )
    db.add(order)
    if not amount:
        if discount:
            discount.uses_count += 1
        application.status = ApplicationStatus.UNDER_REVIEW
        if lead.status != LeadStatus.HANDED_OFF:
            lead.status = LeadStatus.UNDER_REVIEW
    await write_audit_log(
        db,
        tenant_id=lead.tenant_id,
        actor="conversation-engine",
        action="payment.requested" if amount else "payment.fee_waived",
        lead_id=lead.id,
        details={"payment_order_id": str(order.id)},
    )
    return order


async def process_payment(order_id: uuid.UUID) -> uuid.UUID | None:
    sessions = get_sessionmaker()
    async with sessions() as db:
        owner = (
            await db.execute(
                select(PaymentOrder.tenant_id, PaymentOrder.lead_id).where(
                    PaymentOrder.id == order_id
                )
            )
        ).first()
        if owner is None:
            return None
        if (
            await db.scalar(
                select(Lead.id)
                .where(Lead.tenant_id == owner.tenant_id, Lead.id == owner.lead_id)
                .with_for_update()
            )
            is None
        ):
            return None
        order = await db.scalar(
            update(PaymentOrder)
            .where(
                PaymentOrder.id == order_id,
                PaymentOrder.tenant_id == owner.tenant_id,
                PaymentOrder.creation_state == "queued",
                PaymentOrder.creation_attempts < 3,
                (PaymentOrder.next_attempt_at.is_(None))
                | (PaymentOrder.next_attempt_at <= datetime.now(UTC)),
            )
            .values(creation_state="creating", creation_attempts=PaymentOrder.creation_attempts + 1)
            .returning(PaymentOrder)
        )
        if order is None:
            return None
        tenant_id, lead_id, amount, attempts = (
            order.tenant_id,
            order.lead_id,
            order.amount,
            order.creation_attempts,
        )
        institution = await db.get(Institution, tenant_id)
        application = await db.scalar(
            select(Application).where(
                Application.id == order.application_id,
                Application.tenant_id == tenant_id,
                Application.lead_id == lead_id,
                Application.course_id == order.course_id,
            )
        )
        try:
            if (
                institution is None
                or not institution.razorpay_credentials_enc
                or application is None
                or application.status in {ApplicationStatus.APPROVED, ApplicationStatus.REJECTED}
            ):
                raise ValueError("Payment routing unavailable")
            credentials = Credentials.model_validate_json(
                decrypt_pii(institution.razorpay_credentials_enc)
            )
            client = RazorpayClient(
                credentials,
                allow_live=get_settings().app_env == "prod"
                and get_settings().payments_live_enabled,
            )
        except (ValueError, InvalidToken, EncryptionKeyNotConfiguredError):
            order.creation_state, order.last_error = "failed", "configuration_unavailable"
            await db.commit()
            return None
        await db.commit()
    try:
        link = await client.create_link(order_id.hex, amount)
    except PaymentProviderError as error:
        state = "uncertain" if error.uncertain else "failed"
        next_attempt = None
        if error.code == "provider_429" and attempts < 3:
            state = "queued"
            next_attempt = datetime.now(UTC) + timedelta(seconds=30)
        async with sessions() as db:
            await db.execute(
                update(PaymentOrder)
                .where(
                    PaymentOrder.id == order_id,
                    PaymentOrder.tenant_id == tenant_id,
                    PaymentOrder.creation_state == "creating",
                )
                .values(creation_state=state, last_error=error.code, next_attempt_at=next_attempt)
            )
            await db.commit()
        return None
    async with sessions() as db:
        # Match the engine/webhook lock order before inserting a lead-owned delivery.
        await db.scalar(
            select(Lead).where(Lead.id == lead_id, Lead.tenant_id == tenant_id).with_for_update()
        )
        saved = await db.scalar(
            select(PaymentOrder)
            .where(PaymentOrder.id == order_id, PaymentOrder.tenant_id == tenant_id)
            .with_for_update()
        )
        if saved is None or saved.creation_state != "creating":
            return None
        saved.creation_state = "created"
        saved.razorpay_payment_link_id = link.id
        saved.payment_url_enc = encrypt_pii(link.short_url)
        saved.last_error = None
        message_id = await enqueue_outbound(
            db,
            tenant_id=tenant_id,
            lead_id=lead_id,
            kind="payment_link",
            dedup_key=f"payment-link:{order_id}",
            reply=Reply(
                text=f"Your application fee is INR {amount / 100:.2f}. "
                f"Open the institution's payment link: {link.short_url}\n"
                "Payment is an application fee, not admission or a seat reservation."
            ),
        )
        await write_audit_log(
            db,
            tenant_id=tenant_id,
            actor="payment-worker",
            action="payment.link_created",
            lead_id=lead_id,
            details={"payment_order_id": str(order_id)},
        )
        await db.commit()
        return message_id


async def recover_payments() -> None:
    from src.tasks.payments import create_payment_link

    async with get_sessionmaker()() as db:
        await db.execute(
            update(PaymentOrder)
            .where(
                PaymentOrder.creation_state == "creating",
                PaymentOrder.updated_at < datetime.now(UTC) - timedelta(seconds=90),
            )
            .values(creation_state="uncertain", last_error="worker_interrupted")
        )
        ids = list(
            (
                await db.scalars(
                    select(PaymentOrder.id)
                    .where(
                        PaymentOrder.creation_state == "queued",
                        (PaymentOrder.next_attempt_at.is_(None))
                        | (PaymentOrder.next_attempt_at <= datetime.now(UTC)),
                    )
                    .order_by(PaymentOrder.created_at, PaymentOrder.id)
                    .limit(100)
                )
            ).all()
        )
        await db.commit()
    for order_id in ids:
        await create_payment_link.kiq(str(order_id))
