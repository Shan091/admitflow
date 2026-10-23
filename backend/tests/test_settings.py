"""Tests for the settings singleton."""

from src.core.settings import Settings, get_settings


def test_get_settings_returns_settings_instance() -> None:
    settings = get_settings()
    assert isinstance(settings, Settings)


def test_get_settings_is_cached_singleton() -> None:
    # Same object every call — one shared config across the app.
    assert get_settings() is get_settings()


def test_defaults_boot_without_env() -> None:
    # App must boot with no .env present (DB/Redis wired in later tasks).
    settings = get_settings()
    assert settings.app_name == "AdmitFlow"
    assert settings.app_env in {"dev", "staging", "prod"}


def test_env_overrides_defaults(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("LLM_FAST_MODEL", "some-future-model-id")
    # Bypass the module-level cache to observe the override.
    fresh = Settings()
    assert fresh.app_env == "prod"
    assert fresh.llm_fast_model == "some-future-model-id"
