#!/usr/bin/env bash
set -euo pipefail

UV_BIN="${UV_BIN:-uv}"
if ! command -v "$UV_BIN" >/dev/null 2>&1; then
  if command -v uv.exe >/dev/null 2>&1; then
    UV_BIN=uv.exe
  else
    echo "uv is required; install it or set UV_BIN to its executable." >&2
    exit 127
  fi
fi

"$UV_BIN" run ruff check .
"$UV_BIN" run ruff format --check .
"$UV_BIN" run mypy
"$UV_BIN" run pytest
