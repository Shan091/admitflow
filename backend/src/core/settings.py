"""Application settings singleton.

Loads configuration from the environment (and an optional ``.env`` file) via
pydantic-settings. Access through :func:`get_settings`, which is cached so the
whole app shares one instance.

Model IDs are config-driven (ADR-007 "LLM efficiency"): the code references
*roles* (fast / fallback / nuance); the concrete version strings live only here
in settings, never in docs or business logic.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App ---
    app_name: str = "AdmitFlow"
    app_env: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = True
    log_level: str = "INFO"

    # --- Data stores (ADR-007) ---
    # Optional at this stage so the app boots before Task 2/3 wire them up.
    database_url: str | None = None
    redis_url: str | None = None

    # --- PII protection (SPEC §14 / security-and-production.md) ---
    # Optional so the app still boots without them; the helpers in
    # src/core/security.py fail loud if used while a key is unset. Generate the
    # Fernet key with:
    #   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    pii_encryption_key: str | None = None
    phone_hash_key: str | None = None

    # --- Meta WhatsApp (carry-over prerequisite #2, wired in Task 5/6) ---
    # Optional so the app still boots without them; the webhook and sender
    # fail loud if called while unset.
    meta_app_secret: str | None = None  # HMAC-SHA256 body verification
    whatsapp_verify_token: str | None = None  # GET challenge handshake
    whatsapp_access_token: str | None = None  # Graph API bearer token
    whatsapp_phone_number_id: str | None = None  # Sender phone number ID
    meta_graph_api_version: str = "v21.0"  # Graph API version prefix
    legacy_whatsapp_enabled: bool = False
    demo_credentials_path: Path = Path(".demo-credentials.json")

    # --- LLM model roles (config-driven; ADR-007) ---
    # Concrete version strings belong here, not in docs or code.
    llm_fast_model: str = "openai/gpt-4.1-mini"
    llm_fallback_model: str | None = None
    llm_nuance_model: str | None = None
    llm_embedding_model: str = "text-embedding-3-small"
    openai_api_key: SecretStr | None = None
    llm_timeout_seconds: int = Field(default=30, ge=5, le=60)
    telegram_bot_token: SecretStr | None = None
    telegram_institution_code: str = "demo"
    razorpay_key_id: SecretStr | None = None
    razorpay_key_secret: SecretStr | None = None
    razorpay_webhook_secret: SecretStr | None = None
    payments_live_enabled: bool = False
    followups_enabled: bool = True

    # Institution knowledge workspace and processing limits.
    staff_session_hours: int = Field(default=8, ge=1, le=24)
    staff_export_max_rows: int = Field(default=10000, ge=1, le=100000)
    integration_recovery_enabled: bool = True
    staff_allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    upload_max_bytes: int = Field(default=10 * 1024 * 1024, ge=1024)
    upload_batch_max_bytes: int = Field(default=30 * 1024 * 1024, ge=1024)
    upload_batch_files: int = Field(default=25, ge=1, le=100)
    ingestion_timeout_seconds: int = Field(default=180, ge=10, le=600)
    knowledge_min_similarity: float = Field(default=0.3, ge=0, le=1)
    knowledge_rerank_timeout_seconds: float = Field(default=8, ge=0.1, le=30)
    knowledge_recovery_enabled: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide :class:`Settings` singleton."""
    return Settings()
