"""Environment-backed demo settings."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    telegram_bot_token: str | None
    openai_api_key: str | None
    openai_decisions_model: str
    openai_embedding_model: str
    database_path: Path
    rag_min_similarity: float
    rag_min_margin: float
    staff_username: str | None = None
    staff_password: str | None = None
    staff_session_secret: str | None = None
    staff_cookie_secure: bool = False
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    razorpay_webhook_secret: str | None = None
    telegram_webhook_secret: str | None = None


def get_settings() -> Settings:
    """Read configuration from environment without exposing secret values."""
    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN") or None,
        telegram_webhook_secret=os.getenv("TELEGRAM_WEBHOOK_SECRET") or None,
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_decisions_model=os.getenv("OPENAI_DECISIONS_MODEL", "gpt-6-luna"),
        openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        database_path=Path(os.getenv("DATABASE_PATH", "data/admitflow.sqlite3")),
        rag_min_similarity=float(os.getenv("RAG_MIN_SIMILARITY", "0.58")),
        rag_min_margin=float(os.getenv("RAG_MIN_MARGIN", "0.05")),
        staff_username=os.getenv("STAFF_USERNAME") or None,
        staff_password=os.getenv("STAFF_PASSWORD") or None,
        staff_session_secret=os.getenv("STAFF_SESSION_SECRET") or None,
        staff_cookie_secure=os.getenv("STAFF_COOKIE_SECURE", "false").casefold() == "true",
        razorpay_key_id=os.getenv("RAZORPAY_KEY_ID") or None,
        razorpay_key_secret=os.getenv("RAZORPAY_KEY_SECRET") or None,
        razorpay_webhook_secret=os.getenv("RAZORPAY_WEBHOOK_SECRET") or None,
    )
