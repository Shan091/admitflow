"""Markdown sections and table rows stay together within bounded evidence chunks."""

import re
from collections.abc import Iterator

from src.knowledge.extraction import ExtractionError

HEADING = re.compile(r"^(#{1,6})\s+\S")


def table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines) or "|" not in lines[index]:
        return False
    separator = lines[index + 1].strip().strip("|")
    return bool(separator) and all(
        re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in separator.split("|")
    )


def blocks(text: str) -> Iterator[tuple[str, str]]:
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if not lines[index].strip():
            index += 1
            continue
        start = index
        if HEADING.match(lines[index]):
            yield "heading", lines[index].strip()
            index += 1
        elif table_start(lines, index):
            index += 2
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                index += 1
            yield "table", "\n".join(lines[start:index])
        elif lines[index].lstrip().startswith(("```", "~~~")):
            fence = lines[index].lstrip()[:3]
            index += 1
            while index < len(lines):
                index += 1
                if lines[index - 1].lstrip().startswith(fence):
                    break
            yield "text", "\n".join(lines[start:index])
        else:
            index += 1
            while (
                index < len(lines)
                and lines[index].strip()
                and not HEADING.match(lines[index])
                and not table_start(lines, index)
                and not lines[index].lstrip().startswith(("```", "~~~"))
            ):
                index += 1
            yield "text", "\n".join(lines[start:index])


def text_parts(text: str, size: int, overlap: int) -> Iterator[str]:
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = max(text.rfind("\n", start, end), text.rfind(" ", start, end))
            if boundary > start + max(overlap, size // 2):
                end = boundary
        yield text[start:end].strip()
        if end == len(text):
            break
        start = max(start + 1, end - overlap)


def table_parts(table: str, size: int) -> Iterator[str]:
    lines = table.splitlines()
    header = "\n".join(lines[:2])
    if len(header) > size:
        raise ExtractionError("structure_limit")
    current = header
    for row in lines[2:]:
        if len(header) + len(row) + 1 > size:
            raise ExtractionError("structure_limit")
        if len(current) + len(row) + 1 > size:
            yield current
            current = header
        current += "\n" + row
    yield current


def semantic_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Keep section ancestry; repeat table headers instead of breaking row associations."""
    if chunk_size < 64 or not 0 <= overlap < chunk_size:
        raise ValueError("Invalid chunk size or overlap")
    result: list[str] = []
    headings: list[tuple[int, str]] = []
    pending = ""
    prefix = ""
    empty_heading = False
    for kind, content in blocks(text):
        if kind == "heading":
            if pending:
                result.append(prefix + pending)
                pending = ""
            level = len(content) - len(content.lstrip("#"))
            headings = [(n, value) for n, value in headings if n < level]
            headings.append((level, content))
            prefix = "\n".join(value for _, value in headings) + "\n\n"
            if len(prefix) >= chunk_size // 2:
                raise ExtractionError("structure_limit")
            empty_heading = True
            continue
        capacity = chunk_size - len(prefix)
        if len(content) > capacity:
            if pending:
                result.append(prefix + pending)
                pending = ""
            parts = (
                table_parts(content, capacity)
                if kind == "table"
                else text_parts(content, capacity, min(overlap, capacity // 3))
            )
            result.extend(prefix + part for part in parts if part)
        elif pending and len(pending) + len(content) + 2 > capacity:
            result.append(prefix + pending)
            pending = content
        else:
            pending = pending + "\n\n" + content if pending else content
        empty_heading = False
    if pending:
        result.append(prefix + pending)
    elif empty_heading:
        result.append(prefix.strip())
    return result
