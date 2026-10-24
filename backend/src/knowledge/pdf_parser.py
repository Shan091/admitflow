"""Offline PDF child process with per-loop backpressure, memory and time limits."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from weakref import WeakKeyDictionary

import psutil

from src.core.settings import get_settings
from src.knowledge.extraction import MAX_TEXT, ExtractionError

_gates: WeakKeyDictionary[asyncio.AbstractEventLoop, asyncio.Semaphore] = WeakKeyDictionary()
SOURCE_ROOT = Path(__file__).resolve().parents[2]
WORKER_DIRECTORY = Path(__file__).resolve().parent
ERRORS = {
    "invalid_document",
    "password_protected",
    "page_limit",
    "text_limit",
    "ocr_required",
    "no_text",
    "parser_not_ready",
    "processing_timeout",
    "processing_limit",
    "layout_incomplete",
    "file_too_large",
}


def resident_memory(pid: int) -> int:
    """Include Windows venv redirector children and any parser subprocesses."""
    process = psutil.Process(pid)
    processes = [process, *process.children(recursive=True)]
    total = 0
    for item in processes:
        try:
            total += item.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return total


def kill_descendants(pid: int) -> None:
    try:
        children = psutil.Process(pid).children(recursive=True)
    except psutil.Error:
        return
    for child in reversed(children):
        try:
            child.kill()
            child.wait(timeout=2)
        except psutil.Error:
            pass


async def watch_memory(
    process: asyncio.subprocess.Process, limit: int, exceeded: asyncio.Event
) -> None:
    while process.returncode is None:
        try:
            if await asyncio.to_thread(resident_memory, process.pid) > limit:
                exceeded.set()
                await asyncio.to_thread(kill_descendants, process.pid)
                process.kill()
                return
        except (psutil.Error, ProcessLookupError):
            return
        await asyncio.sleep(0.1)


async def parse_pdf(data: bytes) -> str:
    settings = get_settings()
    if len(data) > settings.upload_max_bytes:
        raise ExtractionError("file_too_large")
    gate = _gates.setdefault(asyncio.get_running_loop(), asyncio.Semaphore(1))
    # Inherit OS/runtime paths only, never credentials or the application environment.
    inherited = {
        "PATH",
        "SystemRoot",
        "SYSTEMROOT",
        "WINDIR",
        "TEMP",
        "TMP",
        "HOME",
        "USERPROFILE",
        "LOCALAPPDATA",
        "APPDATA",
        "LANG",
        "LC_ALL",
        "LD_LIBRARY_PATH",
    }
    env = {key: value for key, value in os.environ.items() if key in inherited}
    env.update(
        {
            "PYTHONPATH": str(SOURCE_ROOT),
            "HF_HUB_OFFLINE": "1",
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    flags = 0
    if sys.platform == "win32":
        flags = subprocess.CREATE_NO_WINDOW
    assets = await asyncio.to_thread(settings.document_models_path.resolve)
    async with gate:
        try:
            async with asyncio.timeout(settings.document_parse_timeout_seconds):
                process = await asyncio.create_subprocess_exec(
                    sys.executable,
                    "-m",
                    "src.knowledge.pdf_worker",
                    "--assets",
                    str(assets),
                    "--max-bytes",
                    str(settings.upload_max_bytes),
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=env,
                    cwd=WORKER_DIRECTORY,
                    creationflags=flags,
                )
                exceeded = asyncio.Event()
                monitor = asyncio.create_task(
                    watch_memory(
                        process, settings.document_parse_max_memory_mb * 1024 * 1024, exceeded
                    )
                )
                try:
                    output, _ = await process.communicate(data)
                finally:
                    if process.returncode is None:
                        await asyncio.to_thread(kill_descendants, process.pid)
                        try:
                            process.kill()
                        except ProcessLookupError:
                            pass
                        await process.wait()
                    monitor.cancel()
                    await asyncio.gather(monitor, return_exceptions=True)
                if exceeded.is_set():
                    raise ExtractionError("processing_limit")
        except TimeoutError:
            raise ExtractionError("processing_timeout") from None
    try:
        payload = json.loads(output)
        if not isinstance(payload, dict):
            raise ValueError("Invalid parser response")
        if "error" in payload:
            code = payload["error"]
            raise ExtractionError(
                code if isinstance(code, str) and code in ERRORS else "invalid_document"
            )
        text = payload.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("No parser text")
        if len(text) > MAX_TEXT:
            raise ExtractionError("text_limit")
        return "\n".join(line.rstrip() for line in text.splitlines()).strip()
    except (ValueError, UnicodeDecodeError) as error:
        if isinstance(error, ExtractionError):
            raise
        raise ExtractionError("invalid_document") from None
