"""Produce due reminder jobs and recover queued deliveries; safe to run after restart."""

import argparse
import asyncio
import logging

from src.integrations.delivery import dispatch_pending as dispatch_integrations
from src.outreach.followups import dispatch_due
from src.tasks.broker import broker
from src.telegram.outbound import recover_outbound

logger = logging.getLogger(__name__)


async def run(*, once: bool = False, interval: int = 60) -> None:
    await broker.startup()
    try:
        while True:
            try:
                count = await dispatch_due()
                await recover_outbound()
                await dispatch_integrations()
                if once:
                    print(f"Due follow-up jobs queued: {count}", flush=True)
            except asyncio.CancelledError:
                raise
            except Exception:
                if once:
                    raise
                logger.warning("scheduler_sweep_unavailable; durable work retained")
            if once:
                return
            await asyncio.sleep(interval)
    finally:
        await broker.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()
    if not 15 <= args.interval <= 3600:
        parser.error("interval must be between 15 and 3600 seconds")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    try:
        asyncio.run(run(once=args.once, interval=args.interval))
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(f"Scheduler stopped: {type(error).__name__}. Check configuration and data services.")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
