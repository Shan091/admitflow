"""Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics."""

import argparse
import io
import json
import logging
import math
import re
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

from pypdf import PdfReader

from src.knowledge.extraction import MAX_TEXT, ExtractionError


def preflight_pdf(data: bytes) -> int:
    reader = PdfReader(io.BytesIO(data))
    if reader.is_encrypted:
        raise ExtractionError("password_protected")
    if not reader.pages:
        raise ExtractionError("no_text")
    if len(reader.pages) > 100:
        raise ExtractionError("page_limit")
    size = 0
    for page in reader.pages:
        unit = float(page.get("/UserUnit", 1))
        dimensions = (float(page.mediabox.width) * unit, float(page.mediabox.height) * unit)
        if any(not math.isfinite(value) or not 0 < value <= 2000 for value in dimensions):
            raise ExtractionError("page_limit")
        content = page.get_contents()
        if content is not None and len(content.get_data()) > 8_000_000:
            raise ExtractionError("page_limit")
        text = page.extract_text() or ""
        if not text.strip():
            raise ExtractionError("ocr_required")
        size += len(text)
        if size > MAX_TEXT:
            raise ExtractionError("text_limit")
    return len(reader.pages)


def convert_pdf(data: bytes, assets: Path) -> str:
    pages = preflight_pdf(data)
    try:
        marker = json.loads((assets / ".ready.json").read_text(encoding="utf-8"))
        if marker["package"] != version("docling-slim") or not marker["files"]:
            raise ValueError("Asset version mismatch")
        if any(not (assets / name).is_file() for name in marker["files"]):
            raise ValueError("Incomplete assets")
    except (OSError, KeyError, ValueError):
        raise ExtractionError("parser_not_ready") from None

    from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
    from docling.datamodel.base_models import ConversionStatus, DocumentStream, InputFormat
    from docling.datamodel.pipeline_options import (
        HeadingHierarchyOptions,
        PdfPipelineOptions,
        TableFormerMode,
        TableStructureOptions,
    )
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling_core.types.doc.common.content_layer import ContentLayer

    options = PdfPipelineOptions(
        artifacts_path=assets,
        do_ocr=False,
        do_table_structure=True,
        document_timeout=90,
        enable_remote_services=False,
        allow_external_plugins=False,
        generate_page_images=False,
        generate_picture_images=False,
        generate_parsed_pages=True,
        heading_hierarchy_options=HeadingHierarchyOptions(enabled=True),
        accelerator_options=AcceleratorOptions(num_threads=2, device=AcceleratorDevice.CPU),
    )
    options.table_structure_options = TableStructureOptions(mode=TableFormerMode.ACCURATE)
    converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)},
    )
    result = converter.convert(DocumentStream(name="reference.pdf", stream=io.BytesIO(data)))
    if result.status != ConversionStatus.SUCCESS or len(result.document.pages) != pages:
        raise ExtractionError("layout_incomplete")
    text = result.document.export_to_markdown(
        included_content_layers=set(ContentLayer),
        image_placeholder="",
        escape_underscores=False,
    ).strip()
    if not re.search(r"[^\W_]", text):
        raise ExtractionError("no_text")
    if len(text) > MAX_TEXT:
        raise ExtractionError("text_limit")
    return text


def main() -> None:
    logging.basicConfig(level=logging.CRITICAL, force=True)
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, required=True)
    args = parser.parse_args()
    try:
        data = sys.stdin.buffer.read(args.max_bytes + 1)
        if len(data) > args.max_bytes:
            raise ExtractionError("file_too_large")
        result = {"text": convert_pdf(data, args.assets)}
    except Exception as error:
        result = {"error": str(error) if isinstance(error, ExtractionError) else "invalid_document"}
    sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
    main()
