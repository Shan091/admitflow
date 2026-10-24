"""Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload."""

import asyncio
import json
from pathlib import Path

import httpx2


async def verify() -> dict[str, bool]:
    credentials = json.loads(
        await asyncio.to_thread(Path(".demo-credentials.json").read_text, encoding="utf-8")
    )
    if credentials.get("institution") != "demo":
        raise RuntimeError("Only the configured synthetic demo is supported")
    checks: dict[str, bool] = {}
    upload_id = None
    async with httpx2.AsyncClient(
        base_url="http://127.0.0.1:8000",
        timeout=40,
        headers={"X-AdmitFlow-Request": "1"},
        trust_env=False,
    ) as client:
        response = await client.post("/api/staff/login", json=credentials)
        response.raise_for_status()
        try:
            response = await client.post(
                "/api/knowledge/documents",
                files={
                    "files": (
                        "synthetic-verification/structured-prospectus.pdf",
                        await asyncio.to_thread(
                            Path("tests/fixtures/structured-prospectus.pdf").read_bytes
                        ),
                    ),
                },
            )
            response.raise_for_status()
            row = response.json()["accepted"][0]
            if row["duplicate"]:
                raise RuntimeError("Existing fixture retained; refusing to modify it")
            upload_id = row["id"]
            async with asyncio.timeout(180):
                while True:
                    response = await client.get("/api/knowledge/documents")
                    response.raise_for_status()
                    row = next(r for r in response.json() if r["id"] == upload_id)
                    if row["status"] == "ready":
                        checks["actual_queue_docling_openai_publication"] = row["chunk_count"] > 0
                        break
                    if row["status"] == "failed":
                        raise RuntimeError("Synthetic document indexing failed")
                    await asyncio.sleep(2)
            for programme, amount in (("Nursing", "45000"), ("Commerce", "35000")):
                response = await client.post(
                    "/api/knowledge/search",
                    json={
                        "query": f"What is the {programme} Programme annual tuition?",
                    },
                )
                response.raise_for_status()
                matches = [r for r in response.json()["matches"] if r["document_id"] == upload_id]
                checks[f"{programme.lower()}_table_evidence"] = any(
                    f"### {programme} Programme" in r["text"]
                    and f"INR {amount}" in r["text"]
                    and "| Tuition" in r["text"]
                    for r in matches
                )
        finally:
            if upload_id:
                response = await client.delete(f"/api/knowledge/documents/{upload_id}")
                response.raise_for_status()
                checks["own_upload_removed"] = True
            await client.post("/api/staff/logout")
    return checks


if __name__ == "__main__":
    try:
        checks = asyncio.run(verify())
        report = {"scope": "synthetic live PDF/OpenAI; no Telegram sends", "checks": checks}
        print(json.dumps(report, indent=2))
        Path("../docs/event/DOCUMENT_PIPELINE_RESULTS.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        if not all(checks.values()):
            raise SystemExit(1)
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
        raise SystemExit(1) from None
