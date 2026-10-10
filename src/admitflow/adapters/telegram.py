"""Telegram handlers and asyncio-compatible bot lifecycle."""

import logging
import re
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
    application.add_handler(CommandHandler("resume", resume_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    return application


def keyboard(
    reply: Reply,
    *,
    ai_processing_allowed: bool = False,
    language: str = "en",
) -> InlineKeyboardMarkup | None:
    buttons = list(reply.buttons)
    if not any(data == "language:menu" for _, data in buttons):
        language_label = {
            "en": "Change language",
            "hi": "भाषा बदलें",
            "ml": "ഭാഷ മാറ്റുക",
            "hinglish": "Language badlein",
        }.get(language, "Change language")
        buttons.append((f"🌐 {language_label}", "language:menu"))
    if ai_processing_allowed and not any(data == "ai:processing:off" for _, data in buttons):
        opt_out_label = {
            "en": "Turn off OpenAI processing",
            "hi": "OpenAI प्रोसेसिंग बंद करें",
            "ml": "OpenAI പ്രോസസ്സിംഗ് ഓഫ് ചെയ്യുക",
            "hinglish": "OpenAI processing band karein",
        }.get(language, "Turn off OpenAI processing")
        buttons.append((opt_out_label, "ai:processing:off"))
    if not buttons:
        return None
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(label, callback_data=data)] for label, data in buttons]
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


async def _send_reply(
    update: Update,
    reply: Reply,
    repository: Repository,
    admissions: AdmissionsService,
    lead_id: int,
) -> None:
    message = update.effective_message
    if message is None:
        return
    repository.add_message(lead_id, "outbound", reply.text)
    ai_processing_allowed = admissions.ai_processing_enabled(lead_id)
    await message.reply_text(
        reply.text,
        reply_markup=keyboard(
            reply,
            ai_processing_allowed=ai_processing_allowed,
            language=admissions.preferred_language(lead_id),
        ),
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, _, _ = _services(context)
    user = update.effective_user
    if user is None:
        return
    lead_id, reply = admissions.start(str(user.id), user.username)
    repository.add_message(lead_id, "inbound", "/start", update.update_id)
    await _send_reply(update, reply, repository, admissions, lead_id)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, _, payment_service = _services(context)
    query = update.callback_query
    user = update.effective_user
    if query is None or user is None:
        return
    await query.answer()
    lead_id = repository.upsert_lead(admissions.tenant_id, str(user.id), user.username)
    data = query.data or ""
    repository.add_message(lead_id, "inbound", data, update.update_id)
    if data in {"ai:consent:yes", "ai:processing:on"}:
        reply = admissions.set_ai_processing_enabled(lead_id, True)
    elif data in {"ai:consent:no", "ai:processing:off"}:
        reply = admissions.set_ai_processing_enabled(lead_id, False)
    elif data.startswith("path:"):
        reply = admissions.begin_path(lead_id, data.removeprefix("path:"))
    elif data.startswith("guidance:activity:"):
        reply = await admissions.choose_guidance_signal(
            lead_id, activity_slug=data.removeprefix("guidance:activity:")
        )
    elif data.startswith("guidance:level:"):
        reply = await admissions.choose_guidance_signal(
            lead_id, level=data.removeprefix("guidance:level:")
        )
    elif data.startswith("speaker:"):
        reply = admissions.choose_speaker(lead_id, data.removeprefix("speaker:"))
    elif data.startswith("course:confirm:"):
        reply = admissions.confirm_parent_course(lead_id, data.removeprefix("course:confirm:"))
    elif data.startswith("field:"):
        reply = admissions.recommend_field(lead_id, data.removeprefix("field:"))
    elif data.startswith("level:"):
        reply = admissions.choose_level(lead_id, data.removeprefix("level:"))
    elif data.startswith("activity:"):
        reply = admissions.choose_activity(lead_id, data.removeprefix("activity:"))
    elif data == "discovery:pause":
        reply = admissions.pause_discovery(lead_id)
    elif data == "discovery:back_field":
        reply = admissions.back_to_field(lead_id)
    elif data == "discovery:back_level":
        reply = admissions.back_to_level(lead_id)
    elif data == "language:menu":
        reply = admissions.language_menu(lead_id)
    elif data.startswith("language:"):
        reply = admissions.choose_language(lead_id, data.removeprefix("language:"))
    elif data == "menu:start":
        _, reply = admissions.start(str(user.id), user.username)
    elif data == "handoff:request":
        reply = admissions.handoff(lead_id, "Student requested a staff member.")
    elif data == "browse":
        reply = admissions.browse(lead_id)
    elif data.startswith("course:"):
        reply = admissions.select_course(lead_id, data.removeprefix("course:"))
    elif data == "grade12:yes":
        reply = admissions.answer_grade12(lead_id, True)
    elif data == "grade12:no":
        reply = admissions.answer_grade12(lead_id, False)
    elif data == "payment:yes":
        lead = repository.get_lead(lead_id)
        if lead is None or lead["eligible"] != 1:
            reply = Reply("I can only offer a sample payment link after the sample rules are met.")
        elif payment_service is None:
            reply = Reply("The demo payment link is not configured right now.")
        else:
            repository.update_lead(lead_id, readiness_status="ready_to_apply")
            try:
                offer = await payment_service.create_for_qualified_lead(lead_id)
            except Exception:
                logger.exception("Razorpay test Payment Link creation failed for lead %s", lead_id)
                offer = None
            if offer is None:
                payment = repository.get_payment_for_lead(admissions.tenant_id, lead_id)
                if payment and payment.get("short_url"):
                    url, amount_paise = payment["short_url"], payment["amount_paise"]
                    reply = Reply(
                        f"Demo application fee: {format_inr_from_paise(amount_paise)}. "
                        f"Complete the Razorpay test-mode payment here: {url}"
                    )
                else:
                    reply = Reply("The demo payment link is not available right now.")
            else:
                url, amount_paise = offer
                reply = Reply(
                    f"Demo application fee: {format_inr_from_paise(amount_paise)}. "
                    f"Complete the Razorpay test-mode payment here: {url}"
                )
    else:
        reply = Reply("Please send /start to see the demo options.")
    repository.add_message(lead_id, "outbound", reply.text)
    message = update.effective_message
    if message is not None:
        ai_processing_allowed = admissions.ai_processing_enabled(lead_id)
        await message.reply_text(
            reply.text,
            reply_markup=keyboard(
                reply,
                ai_processing_allowed=ai_processing_allowed,
                language=admissions.preferred_language(lead_id),
            ),
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, intent_router, _ = _services(context)
    user = update.effective_user
    message = update.effective_message
    if user is None or message is None or message.text is None:
        return
    lead_id = repository.upsert_lead(admissions.tenant_id, str(user.id), user.username)
    repository.add_message(lead_id, "inbound", message.text, update.update_id)
    if _is_payment_status_question(message.text):
        payment = repository.get_payment_for_lead(admissions.tenant_id, lead_id)
        if payment is None:
            reply = Reply("I don't see a demo application payment link for you yet.")
        elif payment["status"] == "paid":
            reply = Reply("Your demo application payment is confirmed as paid.")
        elif payment["status"] == "created":
            reply = Reply(
                "Your demo application payment is still pending. Complete the Razorpay test-mode "
                "payment link, then ask again after the webhook is received."
            )
        elif payment["status"] == "failed":
            reply = Reply(
                "Your demo payment link could not be created. Staff support details are not "
                "configured; try again later."
            )
        else:
            reply = Reply("Your demo payment is still being set up. Please check again shortly.")
    else:
        reply = await admissions.free_text(lead_id, message.text, intent_router)
    await _send_reply(update, reply, repository, admissions, lead_id)


async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    repository, admissions, _, _ = _services(context)
    user = update.effective_user
    if user is None:
        return
    lead_id = repository.upsert_lead(admissions.tenant_id, str(user.id), user.username)
    repository.add_message(lead_id, "inbound", "/resume", update.update_id)
    await _send_reply(update, admissions.resume_discovery(lead_id), repository, admissions, lead_id)


def _is_payment_status_question(text: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()
    phrases = (
        "payment status",
        "payment received",
        "payment confirmed",
        "payment go through",
        "payment gone through",
        "payment completed",
        "did i pay",
        "have i paid",
        "paid yet",
    )
    return any(phrase in normalized for phrase in phrases)


async def start_application(
    application: Application[Any, Any, Any, Any, Any, Any],
) -> None:
    await application.initialize()
    await application.start()
    logger.info("Telegram webhook application started")


async def stop_application(
    application: Application[Any, Any, Any, Any, Any, Any],
) -> None:
    if application.running:
        await application.stop()
    await application.shutdown()
    logger.info("Telegram webhook application stopped")
