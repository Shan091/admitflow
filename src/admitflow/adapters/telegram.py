"""Telegram handlers and asyncio-compatible bot lifecycle."""

import logging
import re
from typing import Any, cast

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
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
    show_ai_processing_control: bool = False,
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
    if (
        show_ai_processing_control
        and ai_processing_allowed
        and not any(data == "ai:processing:off" for _, data in buttons)
    ):
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
    *,
    show_ai_processing_control: bool = False,
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
            show_ai_processing_control=show_ai_processing_control,
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
    await _send_reply(
        update, reply, repository, admissions, lead_id, show_ai_processing_control=True
    )


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
    elif data.startswith("guidance:goal:"):
        goal_slug = data.removeprefix("guidance:goal:")
        reply = await admissions.choose_guidance_goal(
            lead_id, None if goal_slug == "skip" else goal_slug
        )
    elif data.startswith("guidance:language:"):
        support_slug = data.removeprefix("guidance:language:")
        reply = await admissions.choose_guidance_language_support(
            lead_id, None if support_slug == "open" else support_slug
        )
    elif data.startswith("guidance:mode:"):
        mode_slug = data.removeprefix("guidance:mode:")
        reply = await admissions.choose_guidance_delivery_mode(
            lead_id, None if mode_slug == "open" else mode_slug
        )
    elif data.startswith("guidance:activity:"):
        reply = await admissions.choose_guidance_signal(
            lead_id, activity_slug=data.removeprefix("guidance:activity:")
        )
    elif data.startswith("guidance:level:"):
        reply = await admissions.choose_guidance_signal(
            lead_id, level=data.removeprefix("guidance:level:")
        )
    elif data.startswith("guidance:confirm:"):
        reply = await admissions.confirm_guidance(lead_id, data.removeprefix("guidance:confirm:"))
    elif data.startswith("guidance:continue:"):
        reply = admissions.continue_guidance_course(
            lead_id, data.removeprefix("guidance:continue:")
        )
    elif data.startswith("guidance:course:"):
        reply = admissions.explore_guidance_course(lead_id, data.removeprefix("guidance:course:"))
    elif data == "guidance:matches":
        reply = admissions.show_guidance_matches(lead_id)
    elif data.startswith("guidance:revise:"):
        reply = await admissions.revise_guidance(lead_id, data.removeprefix("guidance:revise:"))
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
    elif data.startswith("grade12:yes:"):
        reply = admissions.answer_grade12(lead_id, True, data.removeprefix("grade12:yes:"))
    elif data.startswith("grade12:no:"):
        reply = admissions.answer_grade12(lead_id, False, data.removeprefix("grade12:no:"))
    elif data.startswith("sample-prerequisites:yes:"):
        reply = admissions.answer_sample_prerequisites(
            lead_id, True, data.removeprefix("sample-prerequisites:yes:")
        )
    elif data.startswith("sample-prerequisites:no:"):
        reply = admissions.answer_sample_prerequisites(
            lead_id, False, data.removeprefix("sample-prerequisites:no:")
        )
    elif data == "payment:yes":
        lead = repository.get_lead(lead_id)
        if lead is None or lead["eligible"] != 1:
            reply = Reply("Complete the course eligibility check before requesting a payment link.")
        elif payment_service is None:
            reply = Reply("Payment links aren't available right now. Please try again later.")
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
                        f"Application fee: {format_inr_from_paise(amount_paise)}. "
                        f"This is a test payment and won't submit an application: {url}"
                    )
                else:
                    reply = Reply(
                        "Payment links aren't available right now. Please try again later."
                    )
            else:
                url, amount_paise = offer
                reply = Reply(
                    f"Application fee: {format_inr_from_paise(amount_paise)}. "
                    f"This is a test payment and won't submit an application: {url}"
                )
    else:
        reply = Reply("Send /start to explore courses.")
    repository.add_message(lead_id, "outbound", reply.text)
    message = update.effective_message
    if message is not None:
        ai_processing_allowed = admissions.ai_processing_enabled(lead_id)
        await message.reply_text(
            reply.text,
            reply_markup=keyboard(
                reply,
                ai_processing_allowed=ai_processing_allowed,
                show_ai_processing_control=data in {"menu:start", "ai:processing:on"},
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
            reply = Reply("I don't see an application payment link for you yet.")
        elif payment["status"] == "paid":
            reply = Reply(
                "Your Razorpay test payment is confirmed as paid. This does not submit an "
                "application or confirm admission."
            )
        elif payment["status"] == "created":
            reply = Reply(
                "Your application-fee test payment is still pending. Complete the Razorpay "
                "test-mode "
                "payment link, then ask again after the webhook is received."
            )
        elif payment["status"] == "failed":
            reply = Reply(
                "Your payment link could not be created. Staff support details are not "
                "configured; try again later."
            )
        else:
            reply = Reply("Your payment is still being set up. Please check again shortly.")
    else:
        if admissions.ai_processing_enabled(lead_id):
            try:
                await context.bot.send_chat_action(
                    chat_id=message.chat_id,
                    action=ChatAction.TYPING,
                )
            except Exception:
                # A typing indicator is best-effort and must not block the actual reply.
                logger.debug("Unable to send Telegram typing indicator", exc_info=True)
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
