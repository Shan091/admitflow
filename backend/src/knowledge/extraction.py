"""Bounded extraction of institution reference documents; never execute uploads."""

import io
import re
import zipfile
from pathlib import PurePosixPath

SUPPORTED = {".pdf", ".docx", ".txt", ".md", ".csv"}
MAX_TEXT = 400_000


class ExtractionError(ValueError):
    """A safe, public error code rather than parser output containing document text."""


def validate_path(name: str) -> str:
    normalized = name.replace("\\", "/")
    parts = normalized.split("/")
    if (
        not normalized
        or len(normalized) > 500
        or normalized.startswith("/")
        or any(p in {"", ".", ".."} for p in parts)
        or any(ord(c) < 32 for c in normalized)
        or ":" in normalized
    ):
        raise ExtractionError("unsafe_path")
    return normalized


def extract_file(name: str, data: bytes) -> str:
    suffix = PurePosixPath(validate_path(name)).suffix.lower()
    if suffix not in SUPPORTED:
        raise ExtractionError("unsupported_type")
    if not data:
        raise ExtractionError("no_text")
    try:
        if suffix == ".pdf":
            import asyncio

            from src.knowledge.pdf_parser import parse_pdf

            text = asyncio.run(parse_pdf(data))
        elif suffix == ".docx":
            from docx import Document
            from docx.table import Table
            from docx.text.paragraph import Paragraph

            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                entries = archive.infolist()
                if (
                    len(entries) > 500
                    or sum(e.file_size for e in entries) > 32_000_000
                    or any(e.file_size > max(1, e.compress_size) * 200 for e in entries)
                ):
                    raise ExtractionError("archive_limit")
                if "word/document.xml" not in archive.namelist():
                    raise ExtractionError("invalid_document")
            document = Document(io.BytesIO(data))
            pieces = []
            for block in document.iter_inner_content():
                if isinstance(block, Paragraph):
                    style = block.style.style_id if block.style else ""
                    heading = re.fullmatch(r"Heading([1-6])", style or "", re.I)
                    pieces.append(("#" * int(heading[1]) + " " if heading else "") + block.text)
                elif isinstance(block, Table):
                    rows = [
                        "| "
                        + " | ".join(
                            c.text.replace("|", r"\|").replace("\n", "<br>") for c in row.cells
                        )
                        + " |"
                        for row in block.rows
                    ]
                    if rows:
                        rows.insert(1, "| " + " | ".join("---" for _ in block.rows[0].cells) + " |")
                        pieces.append("\n".join(rows))
            text = "\n\n".join(pieces)
        else:
            text = data.decode("utf-8-sig")
            if "\x00" in text:
                raise ExtractionError("invalid_text")
        text = "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").splitlines()).strip()
        if not text:
            raise ExtractionError("no_text")
        if len(text) > MAX_TEXT:
            raise ExtractionError("text_limit")
        return text
    except ExtractionError:
        raise
    except UnicodeDecodeError:
        raise ExtractionError("invalid_text") from None
    except Exception:
        raise ExtractionError("invalid_document") from None
