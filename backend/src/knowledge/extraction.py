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
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted:
                raise ExtractionError("password_protected")
            if len(reader.pages) > 100:
                raise ExtractionError("page_limit")
            pieces = []
            size = 0
            for page in reader.pages:
                content = page.get_contents()
                if content is not None and len(content.get_data()) > 8_000_000:
                    raise ExtractionError("page_limit")
                piece = page.extract_text() or ""
                if not piece.strip():
                    # Do not silently index only the readable half of a mixed scan.
                    raise ExtractionError("ocr_required")
                size += len(piece)
                if size > MAX_TEXT:
                    raise ExtractionError("text_limit")
                pieces.append(piece)
            text = "\n\n".join(pieces)
        elif suffix == ".docx":
            from docx import Document

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
            pieces = [p.text for p in document.paragraphs]
            pieces.extend(
                " | ".join(c.text for c in row.cells)
                for table in document.tables
                for row in table.rows
            )
            text = "\n".join(pieces)
        else:
            text = data.decode("utf-8-sig")
            if "\x00" in text:
                raise ExtractionError("invalid_text")
        text = re.sub(r"[ \t]+", " ", text).strip()
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
