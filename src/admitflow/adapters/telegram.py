"""Telegram handlers and asyncio-compatible bot lifecycle."""

import logging
from typing import Any, cast

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from admitflow.adapters.sqlite import Repository
from admitflow.domain.pricing import format_inr_from_paise
from admitflow.services.admissions import AdmissionsService, Reply
from admitflow.services.contracts import IntentRouter
from admitflow.services.payments import PaymentService

logger = logging.getLogger(__name__)


def build_telegram_application(
    token: str,
    repository: Repository,
    admissions: AdmissionsService,
    intent_router: IntentRouter | None,
    payment_service: PaymentService | None = None,
) -> Application[Any, Any, Any, Any, Any, Any]:
    application = ApplicationBuilder().token(token).build()
    application.bot_data["repository"] = repository
    application.bot_data["admissions"] = admissions
    application.bot_data["intent_router"] = intent_router
    application.bot_data["payment_service"] = payment_service
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    return application


def keyboard(reply: Reply) -> InlineKeyboardMarkup | None:
    if not reply.buttons:
        return None
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(label, callback_data=data)] for label, data in reply.buttons]
    )


def _services(
    context: ContextTypes.DEFAULT_TYPE,
) -> tuple[Repository, AdmissionsService, IntentRouter | None, PaymentService | None]:
    return (
        cast(Repository, context.application.bot_data["repository"]),
        cast(AdmissionsService, context.application.bot_data["admissions"]),
        cast(IntentRouter | None, context.application.bot_data["intent_router"]),
        cast(PaymentService | None, context.application.bot_data.get("payment_service")),
    )


async def _send_reply(update: Update, reply: Reply, repository: Repository, lead_id: int) -> None:
    message = update.effective_message
    if message is None:
        return
    repository.add_message(lead_id, "outbound", reply.text)
    await message.reply_text(reply.text, reply_markup=keyboard(reply))


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, _, _ = _services(context)
    user = update.effective_user
    if user is None:
        return
    lead_id, reply = admissions.start(str(user.id), user.username)
    repository.add_message(lead_id, "inbound", "/start", update.update_id)
    await _send_reply(update, reply, repository, lead_id)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, _, _ = _services(context)
    query = update.callback_query
    user = update.effective_user
    if query is None or user is None:
        return
    await query.answer()
    lead_id = repository.upsert_lead(admissions.tenant_id, str(user.id), user.username)
    data = query.data or ""
    repository.add_message(lead_id, "inbound", data, update.update_id)
    if data == "browse":
        reply = admissions.browse(lead_id)
    elif data.startswith("course:"):
        reply = admissions.select_course(lead_id, data.removeprefix("course:"))
    elif data == "grade12:yes":
        reply = admissions.answer_grade12(lead_id, True)
    elif data == "grade12:no":
        reply = admissions.answer_grade12(lead_id, False)
    else:
        reply = Reply("Please send /start to see the demo options.")
    repository.add_message(lead_id, "outbound", reply.text)
    message = update.effective_message
    if message is not None:
        await message.reply_text(reply.text, reply_markup=keyboard(reply))


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, intent_router, payment_service = _services(context)
    user = update.effective_user
    message = update.effective_message
    if user is None or message is None or message.text is None:
        return
    lead_id = repository.upsert_lead(admissions.tenant_id, str(user.id), user.username)
    repository.add_message(lead_id, "inbound", message.text, update.update_id)
    lead_before = repository.get_lead(lead_id)
    reply = await admissions.free_text(lead_id, message.text, intent_router)
    lead_after = repository.get_lead(lead_id)
    if (
        payment_service is not None
        and lead_before is not None
        and lead_before["state"] == "awaiting_marks"
        and lead_after is not None
        and lead_after["eligible"] == 1
    ):
        try:
            offer = await payment_service.create_for_qualified_lead(lead_id)
        except Exception:
            logger.exception("Razorpay test Payment Link creation failed for lead %s", lead_id)
            offer = None
        if offer is not None:
            url, amount_paise = offer
            reply = Reply(
                f"{reply.text}\n\nDemo application fee: "
                f"{format_inr_from_paise(amount_paise)}. Complete the Razorpay test-mode "
                f"payment here: {url}"
            )
        elif lead_after.get("eligible") == 1:
            reply = Reply(f"{reply.text}\n\nThe demo payment link is not available right now.")
    await _send_reply(update, reply, repository, lead_id)


async def start_polling(
    application: Application[Any, Any, Any, Any, Any, Any],
) -> None:
    await application.initialize()
    await application.start()
    updater = application.updater
    if updater is None:
        raise RuntimeError("Telegram updater is not available")
    await updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram polling started")


async def stop_polling(
    application: Application[Any, Any, Any, Any, Any, Any],
) -> None:
    updater = application.updater
    if updater is not None and updater.running:
        await updater.stop()
    if application.running:
        await application.stop()
    await application.shutdown()
