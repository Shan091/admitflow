"""Untrusted PDF parsing is bounded, offline and separate from admission workers."""

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.knowledge.extraction import ExtractionError
from src.knowledge.pdf_parser import parse_pdf


class Process:
    pid = 2147483000

    def __init__(self, mode="success"):
        self.mode = mode
        self.returncode = None
        self.killed = asyncio.Event()

    async def communicate(self, input):
        if self.mode == "success":
            self.returncode = 0
            return json.dumps({"text": "# Course\n\nTuition is INR 45000."}).encode(), b""
        await self.killed.wait()
        return b"private parser output", b"private parser error"

    def kill(self):
        self.returncode = -9
        self.killed.set()

    async def wait(self):
        return self.returncode


@pytest.fixture
def settings(monkeypatch):
    monkeypatch.setattr(
        "src.knowledge.pdf_parser.get_settings",
        lambda: SimpleNamespace(
            document_models_path=Path("synthetic-models"),
            document_parse_timeout_seconds=0.05,
            document_parse_max_memory_mb=2048,
            upload_max_bytes=10 * 1024 * 1024,
        ),
    )


async def test_pdf_child_does_not_inherit_credentials(monkeypatch, settings):
    captured = []

    async def spawn(*args, **kwargs):
        captured.append(kwargs)
        return Process()

    monkeypatch.setenv("OPENAI_API_KEY", "synthetic-parser-secret")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "synthetic-parser-token")
    monkeypatch.setattr("asyncio.create_subprocess_exec", spawn)
    assert "INR 45000" in await parse_pdf(b"synthetic")
    assert "OPENAI_API_KEY" not in captured[0]["env"]
    assert "TELEGRAM_BOT_TOKEN" not in captured[0]["env"]
    assert captured[0]["env"]["HF_HUB_OFFLINE"] == "1"


@pytest.mark.parametrize("mode", ["timeout", "cancel"])
async def test_timed_out_or_cancelled_parser_is_killed(monkeypatch, settings, mode):
    process = Process("blocked")
    started = asyncio.Event()

    async def spawn(*args, **kwargs):
        started.set()
        return process

    monkeypatch.setattr("asyncio.create_subprocess_exec", spawn)
    task = asyncio.create_task(parse_pdf(b"synthetic"))
    await started.wait()
    if mode == "cancel":
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    else:
        with pytest.raises(ExtractionError, match="processing_timeout"):
            await task
    assert process.killed.is_set()


async def test_memory_limit_kills_parser_without_exposing_its_output(monkeypatch, settings):
    process = Process("blocked")

    async def spawn(*args, **kwargs):
        return process

    monkeypatch.setattr("asyncio.create_subprocess_exec", spawn)
    monkeypatch.setattr(
        "src.knowledge.pdf_parser.psutil.Process",
        lambda pid: SimpleNamespace(
            memory_info=lambda: SimpleNamespace(rss=1024),
            children=lambda recursive: [
                SimpleNamespace(
                    memory_info=lambda: SimpleNamespace(rss=3 * 1024 * 1024 * 1024),
                    kill=lambda: None,
                    wait=lambda timeout: None,
                )
            ],
        ),
    )
    with pytest.raises(ExtractionError, match="processing_limit"):
        await parse_pdf(b"synthetic")
    assert process.killed.is_set()
