#!/usr/bin/env bash
set -euo pipefail
uv run uvicorn admitflow.main:app --reload --env-file .env --host 127.0.0.1 --port 8000
