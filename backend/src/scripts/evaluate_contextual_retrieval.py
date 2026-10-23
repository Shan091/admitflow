"""Bounded synthetic OpenAI reference resolution; no database writes or sends."""

import asyncio
import json
from pathlib import Path

from src.knowledge.retrieval import contextual_query


async def evaluate() -> dict[str, object]:
    hostel = [
        {"role": "user", "content": "Is hostel accommodation available?"},
        {"role": "assistant", "content": "Hostel accommodation is available on campus."},
    ]
    ambiguous = [{"role": "assistant", "content": "Nursing and commerce courses are available."}]
    cases = [
        ("en-reference", "Where is it?", hostel, "hostel"),
        ("hi-reference", "वह कहाँ है?", hostel, "hostel"),
        ("hinglish-reference", "Woh kahan hai?", hostel, "hostel"),
        ("ml-reference", "അത് എവിടെയാണ്?", hostel, "hostel"),
        ("ambiguous-course", "How much does that cost?", ambiguous, None),
        ("ambiguous-hi", "उसकी फीस कितनी है?", ambiguous, None),
        ("explicit-topic-change", "When is the library open?", hostel, "library"),
        ("off-topic-preserved", "Can I visit the moon?", hostel, "moon"),
    ]
    results = []
    for name, question, history, expected in cases:
        try:
            query = await contextual_query(question, history)
            passed = (
                query is None
                if expected is None
                else query is not None and expected in query.lower()
            )
            results.append({"case": name, "passed": passed, "clarification": query is None})
        except Exception as error:
            results.append({"case": name, "passed": False, "error_type": type(error).__name__})
    return {
        "scope": "Eight synthetic live query-resolution cases; no fluency claim or sends",
        "cases": results,
        "passed": sum(row["passed"] is True for row in results),
        "total": len(results),
    }


def main() -> None:
    report = asyncio.run(evaluate())
    target = Path(__file__).resolve().parents[3] / "docs/event/CONTEXTUAL_RETRIEVAL_RESULTS.json"
    target.write_bytes((json.dumps(report, indent=2) + "\n").encode())
    print(json.dumps(report, indent=2))
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
