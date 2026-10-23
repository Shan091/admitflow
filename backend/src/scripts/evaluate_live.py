"""Five bounded live embedding searches through the real authenticated staff API."""

import asyncio
import json
from pathlib import Path

import httpx2


async def evaluate() -> None:
    raw = await asyncio.to_thread(Path(".demo-credentials.json").read_text, encoding="utf-8")
    credentials = json.loads(raw)
    examples = [
        ("English", "Where is the demo campus?", True),
        ("Hindi", "डेमो कैंपस कहाँ है?", True),
        ("Hinglish", "Demo campus kahan hai?", True),
        ("Malayalam", "ഡെമോ ക്യാമ്പസ് എവിടെയാണ്?", True),
        ("Unsupported", "How do I repair a rocket engine?", False),
    ]
    results = []
    async with httpx2.AsyncClient(
        base_url="http://127.0.0.1:8000", timeout=40, headers={"X-AdmitFlow-Request": "1"}
    ) as client:
        login = await client.post("/api/staff/login", json=credentials)
        if login.status_code != 200:
            print(json.dumps({"status": "login_failed", "http_status": login.status_code}))
            return
        for language, query, expected in examples:
            response = await client.post("/api/knowledge/search", json={"query": query})
            matches = response.json().get("matches", [])
            results.append(
                {
                    "case": language,
                    "http_status": response.status_code,
                    "support_found": bool(matches),
                    "expected_support": expected,
                    "passed": response.status_code == 200 and bool(matches) == expected,
                }
            )
        await client.post("/api/staff/logout")
    print(
        json.dumps(
            {"cases": results, "scope": "synthetic retrieval, not language fluency"}, indent=2
        )
    )


if __name__ == "__main__":
    try:
        asyncio.run(evaluate())
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
