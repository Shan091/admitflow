#!/usr/bin/env bash
# AdmitFlow backend — local quality gate. Mirrors .github/workflows/ci.yml exactly.
# Run from the backend/ directory:  bash scripts/verify.sh
#
# This is the "definition of done" floor for every change. If this is red,
# the change is not done. CI runs the identical steps, so green here == green there.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> ruff (lint)"
uv run ruff check .

echo "==> ruff (format check)"
uv run ruff format --check .

echo "==> mypy (strict)"
uv run mypy

echo "==> pytest"
uv run pytest

echo
echo "OK — all quality gates green."
