"""Verify the isolated local Compose stack without external API calls or sends."""

import argparse
import asyncio
import json
import subprocess
from pathlib import Path

import httpx2
from websockets.asyncio.client import connect

ROOT = Path(__file__).resolve().parents[2]


def compose(*args: str) -> str:
    result = subprocess.run(
        ["docker", "compose", "--project-name", "admitflow-local", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode:
        # Some commands read credentials privately. Never echo command output on failure.
        raise RuntimeError("A Compose verification command failed")
    return result.stdout


async def seed_credentials() -> dict[str, str]:
    return json.loads(
        await asyncio.to_thread(
            compose,
            "run",
            "--rm",
            "--no-deps",
            "--entrypoint",
            ".venv/bin/python",
            "bootstrap",
            "-c",
            "from pathlib import Path; "
            "print(Path('/run/admitflow/.demo-credentials.json').read_text())",
        )
    )


async def verify(restart: bool = False) -> dict[str, bool]:
    credentials = await seed_credentials()
    checks: dict[str, bool] = {}
    if restart:
        await asyncio.to_thread(compose, "stop")
        await asyncio.to_thread(compose, "up", "-d", "--wait")
        checks["restart_preserves_credentials"] = credentials == await seed_credentials()
    base = "http://127.0.0.1:13000"
    async with httpx2.AsyncClient(base_url=base, timeout=20, trust_env=False) as client:
        checks["frontend"] = (await client.get("/")).status_code == 200
        login = await client.post(
            "/api/staff/login", json=credentials, headers={"X-AdmitFlow-Request": "1"}
        )
        checks["authenticated_proxy"] = login.status_code == 200
        me = await client.get("/api/staff/me")
        checks["synthetic_institution"] = me.json().get("institution") == "AdmitFlow Demo Institute"
        checks["legacy_ingress_disabled"] = (
            await client.post("/api/webhook", json={})
        ).status_code == 404
        cookie = "; ".join(f"{key}={value}" for key, value in client.cookies.items())
        async with connect(
            "ws://127.0.0.1:13000/api/staff/notifications/ws",
            origin=base,
            additional_headers={"Cookie": cookie},
            open_timeout=10,
            proxy=None,
        ) as socket:
            snapshot = json.loads(await asyncio.wait_for(socket.recv(), 10))
            checks["authenticated_websocket"] = isinstance(snapshot.get("items"), list)
        await client.post("/api/staff/logout", headers={"X-AdmitFlow-Request": "1"})
    async with httpx2.AsyncClient(trust_env=False) as client:
        ready = await client.get("http://127.0.0.1:18000/ready")
        checks["data_store_readiness"] = ready.status_code == 200
    result = await asyncio.to_thread(
        compose,
        "exec",
        "-T",
        "api",
        ".venv/bin/python",
        "-c",
        """
import asyncio
from src.tasks.broker import broker
from src.tasks.processing import ping
async def main():
    await broker.startup()
    try:
        task = await ping.kiq('isolated-compose-smoke')
        result = await task.wait_result(timeout=20)
        assert result.return_value == {'result': 'isolated-compose-smoke'}
        print('queue-result-confirmed')
    finally:
        await broker.shutdown()
asyncio.run(main())
""",
    )
    checks["real_worker_queue_roundtrip"] = "queue-result-confirmed" in result
    result = await asyncio.to_thread(
        compose,
        "exec",
        "-T",
        "scheduler",
        ".venv/bin/python",
        "-m",
        "src.scripts.scheduler",
        "--once",
    )
    checks["scheduler_sweep"] = "Expired conversation histories removed: 0" in result
    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--restart", action="store_true", help="Stop/start this isolated stack first"
    )
    args = parser.parse_args()
    try:
        checks = asyncio.run(verify(restart=args.restart))
        report = {"scope": "isolated Compose; no provider calls or sends", "checks": checks}
        print(json.dumps(report, indent=2))
        if not all(checks.values()):
            raise SystemExit(1)
        (ROOT / "docs/event/COMPOSE_RESULTS.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}))
        raise SystemExit(1) from None
