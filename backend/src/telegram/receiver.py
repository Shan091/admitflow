"""One advisory-locked long poller per bot, with durable offsets and queue recovery."""

import argparse
import asyncio
import logging
import uuid

from sqlalchemy import select, text

from src.core.security import encrypt_pii
from src.core.settings import get_settings
from src.db.models import Institution, TelegramBot
from src.db.session import get_engine, get_sessionmaker
from src.tasks.broker import broker
from src.telegram.adapter import TelegramAPIError, TelegramClient
from src.telegram.service import accept_update, recover_pending

logger = logging.getLogger(__name__)


async def provision_bot(code: str) -> tuple[uuid.UUID, str]:
    token = get_settings().telegram_bot_token
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured")
    client = TelegramClient(token.get_secret_value())
    identity = await client.call("getMe", {})
    hook = await client.call("getWebhookInfo", {})
    if hook.get("url"):
        raise ValueError("This bot has a webhook; explicitly remove it before enabling polling")
    async with get_sessionmaker()() as db:
        institution = await db.scalar(select(Institution).where(Institution.slug == code))
        if not institution:
            raise ValueError("Provision an institution or run the synthetic seed first")
        bot = await db.scalar(
            select(TelegramBot)
            .where(TelegramBot.telegram_bot_id == identity["id"])
            .with_for_update()
        )
        if bot and bot.tenant_id != institution.id:
            raise ValueError("Bot already belongs to another institution")
        if not bot:
            bot = TelegramBot(
                tenant_id=institution.id,
                telegram_bot_id=identity["id"],
                token_enc=encrypt_pii(token.get_secret_value()),
            )
            db.add(bot)
        else:
            bot.token_enc = encrypt_pii(token.get_secret_value())
        await db.flush()
        result = bot.id
        await db.commit()
        return result, str(identity["username"])


async def recovery() -> None:
    while True:
        try:
            await recover_pending()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning("telegram_queue_unavailable; pending events retained")
        await asyncio.sleep(15)


async def run(code: str) -> None:
    bot_id, username = await provision_bot(code)
    token = get_settings().telegram_bot_token
    assert token is not None
    client = TelegramClient(token.get_secret_value())
    # A dedicated database connection holds the cross-process receiver lock.
    async with get_engine().connect() as guard:
        lock_id = bot_id.int % (2**63 - 1)
        owned = await guard.scalar(text("SELECT pg_try_advisory_lock(:key)"), {"key": lock_id})
        if not owned:
            raise ValueError("Another receiver already owns this bot")
        await broker.startup()
        job = asyncio.create_task(recovery())
        print(f"Telegram receiver ready: https://t.me/{username}", flush=True)
        try:
            while True:
                await guard.execute(text("SELECT 1"))
                async with get_sessionmaker()() as db:
                    bot = await db.get(TelegramBot, bot_id)
                    if bot is None or not bot.is_active:
                        return
                    offset = bot.last_update_id + 1 if bot.last_update_id is not None else 0
                try:
                    updates = await client.call(
                        "getUpdates",
                        {
                            "offset": offset,
                            "limit": 25,
                            "timeout": 25,
                            "allowed_updates": ["message", "callback_query"],
                        },
                    )
                    for update in updates:
                        await accept_update(bot_id, update)
                    if updates:
                        try:
                            await recover_pending()
                        except Exception:
                            logger.warning("telegram_enqueue_deferred")
                except TelegramAPIError as error:
                    logger.warning("telegram_poll_failed code=%d", error.code)
                    await asyncio.sleep(min(max(error.retry_after, 2), 30))
        finally:
            job.cancel()
            await asyncio.gather(job, return_exceptions=True)
            await broker.shutdown()
            await guard.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": lock_id})
            await guard.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution-code", default=get_settings().telegram_institution_code)
    args = parser.parse_args()
    # Provider HTTP URLs can contain tokens. Do not enable HTTP debug logging.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    try:
        asyncio.run(run(args.institution_code))
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(
            f"Receiver stopped: {type(error).__name__}. "
            "Check configuration and service availability."
        )
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
