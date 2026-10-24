"""Synthetic collection latency evidence; no database writes or Telegram operations."""

import asyncio
import json
import statistics
import time
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Lead, TelegramBot
from src.decision import decide
from src.engine import applications


async def evaluate() -> dict[str, Any]:
    calls = 0
    original = decide

    async def counted(*args: Any, **kwargs: Any) -> Any:
        nonlocal calls
        calls += 1
        return await original(*args, **kwargs)

    provider_patch = patch("src.engine.applications.decide", counted)
    provider_patch.start()
    scenarios = [
        ("greeting", "hi", {}, {}),
        ("short-answer", "Anu Nair", {}, {"full_name": "Anu Nair"}),
        (
            "multiple-details",
            "My name is Anu Nair. My DOB is 2005-03-14.",
            {},
            {"full_name": "Anu Nair", "dob": "2005-03-14"},
        ),
        (
            "explicit-correction",
            "Actually my name is Anu Menon.",
            {"full_name": "Anu Nair", "dob": "2005-03-14"},
            {"full_name": "Anu Menon", "dob": "2005-03-14"},
        ),
        ("no-inferred-birthday", "Actually I only know I am 21; I cannot give a birthday.", {}, {}),
    ]
    rows: list[dict[str, Any]] = []
    try:
        async with AsyncSession() as db:
            for name, message, initial, expected in scenarios:
                tenant, cid, batch = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
                lead = Lead(
                    id=uuid.uuid4(), tenant_id=tenant, current_course_id=cid, current_batch_id=batch
                )
                bot = TelegramBot(id=uuid.uuid4(), tenant_id=tenant)
                memory: dict[str, Any] = {
                    "facts": {},
                    "application_draft": {
                        "course_id": str(cid),
                        "batch_id": str(batch),
                        "nonce": "synthetic",
                        "values": dict(initial),
                    },
                }
                before, started = calls, time.perf_counter()
                try:
                    reply = await applications.collect_application(db, lead, bot, memory, message)
                    values = memory["application_draft"]["values"]
                    ok = values == expected and not any("Submit" in b.text for b in reply.buttons)
                    rows.append(
                        {
                            "id": name,
                            "passed": ok,
                            "elapsed_ms": round((time.perf_counter() - started) * 1000),
                            "model_calls": calls - before,
                            "saved_fields": list(values),
                            "response": reply.text,
                        }
                    )
                except Exception as error:
                    rows.append({"id": name, "passed": False, "error_type": type(error).__name__})
                print(json.dumps(rows[-1]), flush=True)
    finally:
        provider_patch.stop()
    model_times = [int(r["elapsed_ms"]) for r in rows if r.get("model_calls")]
    return {
        "scope": "Synthetic English application collection; no database writes or sends",
        "cases": rows,
        "passed": sum(r["passed"] for r in rows),
        "total": len(rows),
        "live_model_turn_median_ms": statistics.median(model_times) if model_times else None,
        "latency_limits": "Small local sample, not a production percentile or speedup claim",
    }


def main() -> None:
    report = asyncio.run(evaluate())
    target = Path(__file__).resolve().parents[3] / "docs/event/CONVERSATION_EVALUATION_RESULTS.json"
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
