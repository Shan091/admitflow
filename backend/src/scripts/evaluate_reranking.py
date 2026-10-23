"""Live synthetic OpenAI ranking check; no database writes or message delivery."""

import asyncio
import json
import time
import uuid
from pathlib import Path

from src.db.models import DocumentChunk
from src.knowledge.reranking import rerank


async def evaluate() -> dict[str, object]:
    tenant = uuid.uuid4()
    candidates = [
        DocumentChunk(id=uuid.uuid4(), tenant_id=tenant, content=text, chunk_index=i)
        for i, text in enumerate(
            [
                "The cafeteria serves lunch at noon.",
                "Annual tuition is INR 45000.",
                "Hostel accommodation is available on campus.",
                "The library is open from 9 AM to 5 PM.",
            ]
        )
    ]
    cases = [
        ("en", "Is hostel accommodation available?"),
        ("hi", "क्या हॉस्टल की सुविधा उपलब्ध है?"),
        ("hinglish", "Hostel accommodation available hai?"),
        ("ml", "ഹോസ്റ്റൽ സൗകര്യം ലഭ്യമാണോ?"),
    ]
    results = []
    for language, query in cases:
        started = time.monotonic()
        ranked = await rerank(query, candidates, tenant, top_k=1)
        results.append(
            {
                "language": language,
                "passed": bool(ranked) and ranked[0].id == candidates[2].id,
                "elapsed_ms": round((time.monotonic() - started) * 1000),
            }
        )
    return {
        "scope": "Four synthetic ranking cases, original relevant passage at baseline rank 3; "
        "not a fluency or production latency claim. No writes or sends.",
        "provider": "configured OpenAI roles; no fine-tuning",
        "cases": results,
        "passed": sum(row["passed"] is True for row in results),
        "total": len(results),
    }


def main() -> None:
    report = asyncio.run(evaluate())
    target = Path(__file__).resolve().parents[3] / "docs/event/RERANKING_RESULTS.json"
    target.write_bytes((json.dumps(report, indent=2) + "\n").encode())
    print(json.dumps(report, indent=2))
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
