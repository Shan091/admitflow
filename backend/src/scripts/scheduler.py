"""Produce due reminder jobs and recover queued deliveries; safe to run after restart."""

import argparse
import asyncio
import logging
from collections.abc import Awaitable, Callable

from src.integrations.delivery import dispatch_pending as dispatch_integrations
from src.outreach.followups import dispatch_due
from src.payments.demo import check_demo_payments
from src.staff.privacy import purge_retained
from src.tasks.broker import broker
from src.telegram.outbound import recover_outbound

logger = logging.getLogger(__name__)


async def run(*, once: bool = False, interval: int = 60) -> None:
    broker_ready = False
    operations: tuple[tuple[str, Callable[[], Awaitable[int | None]]], ...] = (
        ("retention", purge_retained),
        ("followups", dispatch_due),
        ("demo_payments", check_demo_payments),
        ("outbound", recover_outbound),
        ("integrations", dispatch_integrations),
    )
    try:
        while True:
            failed = []
            try:
                if not broker_ready:
                    await broker.startup()
                    broker_ready = True
            except asyncio.CancelledError:
                raise
            except Exception:
                failed.append("queue")
                logger.warning("scheduler_queue_startup_unavailable")
            results = {}
            for component, operation in operations:
                try:
                    results[component] = await operation()
                except asyncio.CancelledError:
                    raise
                except Exception:
                    failed.append(component)
                    logger.warning(
                        "scheduler_sweep_unavailable component=%s; durable work retained", component
                    )
            if once:
                print(f"Due follow-up jobs queued: {results.get('followups', 0)}", flush=True)
                print(
                    f"Expired conversation histories removed: {results.get('retention', 0)}",
                    flush=True,
                )
                if failed:
                    raise RuntimeError("One or more scheduler components are unavailable")
                return
            await asyncio.sleep(interval)
    finally:
        if broker_ready:
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
