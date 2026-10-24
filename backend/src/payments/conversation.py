"""Code-owned fee previews and explicit, conversation-bound payment requests."""

import secrets
import time
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import decrypt_pii
from src.db.enums import PaymentStatus
from src.db.models import Institution, Lead, PaymentOrder, TelegramBot
from src.engine.contracts import Button, Reply
from src.payments.service import PaymentRequestError, existing_payment, fee_details, request_payment
from src.telegram.callbacks import callback_data


def button(label: str, target: str, lead: Lead, bot: TelegramBot) -> Button:
    return Button(text=label, data=callback_data("pay", target, lead.id, bot.id))


def order_reply(order: PaymentOrder) -> Reply:
    if order.status == PaymentStatus.PAID:
        return Reply(
            text=f"Payment of INR {order.amount / 100:.2f} is confirmed. "
            "Your institution reviews the application separately. This is not admission."
        )
    if order.status == PaymentStatus.WAIVED:
        return Reply(
            text="The application fee is waived. Your application is available for staff review. "
            "This is not admission or a seat reservation."
        )
    if order.creation_state == "created" and order.payment_url_enc:
        return Reply(
            text=f"Application fee: INR {order.amount / 100:.2f}. "
            f"Open the institution's existing payment link: {decrypt_pii(order.payment_url_enc)}\n"
            "Paying the application fee does not grant admission or reserve a seat."
        )
    if order.creation_state in {"queued", "creating"}:
        return Reply(
            text=f"Your payment link for INR {order.amount / 100:.2f} is being prepared. "
            "It will appear here when available. Your application is saved."
        )
    return Reply(
        text="The payment link needs staff review. "
        "Contact your institution before paying again. Your application is saved."
    )


async def preview(
    db: AsyncSession,
    lead: Lead,
    bot: TelegramBot,
    memory: dict[str, Any],
    application_id: uuid.UUID,
) -> Reply:
    existing = await existing_payment(db, lead, application_id)
    if existing:
        return order_reply(existing)
    _, course, amount, _ = await fee_details(db, lead, application_id, memory.get("discount_code"))
    if course.application_fee == 0:
        return Reply(
            text="No application fee is configured. Your application is available for staff review."
        )
    institution = await db.get(Institution, lead.tenant_id)
    if amount and (institution is None or not institution.razorpay_credentials_enc):
        memory.pop("payment_quote", None)
        return Reply(
            text=f"Application fee: INR {amount / 100:.2f}. "
            "Online payments are not available yet. Your application is saved."
        )
    nonce = secrets.token_hex(8)
    memory["payment_quote"] = {
        "application_id": str(application_id),
        "amount": amount,
        "discount_code": memory.get("discount_code"),
        "nonce": nonce,
        "expires_at": int(time.time()) + 600,
    }
    return Reply(
        text=f"Application fee to pay: INR {amount / 100:.2f}. "
        "This is an application fee, not tuition or a seat reservation. "
        "Use /discount CODE to apply an institution-issued discount before requesting a link.",
        buttons=[
            button(
                "Apply fee waiver" if amount == 0 else "Create payment link",
                f"create-{nonce}",
                lead,
                bot,
            )
        ],
    )


async def payment_action(
    db: AsyncSession, lead: Lead, bot: TelegramBot, memory: dict[str, Any], target: str
) -> Reply:
    operation, _, reference = target.partition("-")
    try:
        if operation == "review":
            return await preview(db, lead, bot, memory, uuid.UUID(reference))
        quote = memory.get("payment_quote")
        if (
            operation != "create"
            or not quote
            or quote.get("nonce") != reference
            or quote.get("expires_at", 0) < time.time()
        ):
            return Reply(text="This fee quote has expired. Use /pay to review the current fee.")
        application_id = uuid.UUID(quote["application_id"])
        existing = await existing_payment(db, lead, application_id)
        if existing:
            return order_reply(existing)
        _, _, amount, _ = await fee_details(db, lead, application_id, quote.get("discount_code"))
        if amount != quote["amount"] or quote.get("discount_code") != memory.get("discount_code"):
            updated = await preview(db, lead, bot, memory, application_id)
            return Reply(
                text="The fee or discount changed. Please review it again.\n\n" + updated.text,
                buttons=updated.buttons,
            )
        return order_reply(
            await request_payment(db, lead, application_id, quote.get("discount_code"))
        )
    except (ValueError, PaymentRequestError) as error:
        if isinstance(error, PaymentRequestError):
            return Reply(text=str(error))
        return Reply(
            text="This payment choice is no longer valid. Use /pay to review your application fee."
        )


async def discount_action(
    db: AsyncSession,
    lead: Lead,
    bot: TelegramBot,
    memory: dict[str, Any],
    application_id: uuid.UUID,
    code: str,
) -> Reply:
    try:
        if await existing_payment(db, lead, application_id):
            return Reply(
                text="An invoice already exists. Ask staff to review it before changing a discount."
            )
        if not code.strip() or len(code.strip()) > 64:
            raise PaymentRequestError("Use /discount followed by an institution-issued code.")
        await fee_details(db, lead, application_id, code)
        memory["discount_code"] = code.strip().upper()
        return await preview(db, lead, bot, memory, application_id)
    except PaymentRequestError as error:
        return Reply(text=str(error))
