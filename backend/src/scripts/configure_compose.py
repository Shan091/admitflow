"""Create private isolated local Compose configuration without copying live secrets."""

import argparse
import os
import secrets
from pathlib import Path

from cryptography.fernet import Fernet


def configure(target: Path) -> None:
    password = secrets.token_urlsafe(32)
    content = (
        "# Isolated local synthetic stack. Do not use this file for production.\n"
        "APP_ENV=dev\nDEBUG=false\nLOG_LEVEL=INFO\n"
        f"POSTGRES_PASSWORD={password}\n"
        f"DATABASE_URL=postgresql+asyncpg://admitflow:{password}@postgres:5432/admitflow\n"
        "REDIS_URL=redis://redis:6379/0\n"
        f"PII_ENCRYPTION_KEY={Fernet.generate_key().decode()}\n"
        f"PHONE_HASH_KEY={secrets.token_urlsafe(32)}\n"
        'STAFF_ALLOWED_ORIGINS=["http://localhost:13000","http://127.0.0.1:13000"]\n'
        "DEMO_CREDENTIALS_PATH=/run/admitflow/.demo-credentials.json\n"
        "TELEGRAM_INSTITUTION_CODE=demo\nTELEGRAM_BOT_TOKEN=\nOPENAI_API_KEY=\n"
        "PAYMENTS_LIVE_ENABLED=false\nLEGACY_WHATSAPP_ENABLED=false\n"
    )
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[3] / ".env")
    args = parser.parse_args()
    try:
        configure(args.output)
    except FileExistsError:
        parser.exit(1, "Configuration already exists; nothing was overwritten.\n")
    print("Private local Compose configuration created. No live credentials were copied.")


if __name__ == "__main__":
    main()
