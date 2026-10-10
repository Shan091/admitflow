"""FastAPI entrypoint and service composition."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from admitflow.adapters.openai import OpenAIAdapter
from admitflow.adapters.razorpay import RazorpayAdapter
from admitflow.adapters.sqlite import Repository
from admitflow.adapters.telegram import (
    build_telegram_application,
    start_application,
    stop_application,
)
from admitflow.adapters.vector_store import VectorStore
from admitflow.config import Settings, get_settings
from admitflow.dashboard.payment_routes import router as payment_router
from admitflow.dashboard.routes import router as dashboard_router
from admitflow.dashboard.telegram_routes import router as telegram_router
from admitflow.services.admissions import AdmissionsService
from admitflow.services.payments import PaymentService
from admitflow.services.retrieval import RetrievalService, embedding_index_key

load_dotenv()
logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        repository = Repository(app_settings.database_path)
        repository.initialize()
        repository.seed_catalog()
        openai_adapter = (
            OpenAIAdapter(
                app_settings.openai_api_key,
                app_settings.openai_decisions_model,
                app_settings.openai_embedding_model,
            )
            if app_settings.openai_api_key
            else None
        )
        vector_store = VectorStore(repository)
        embedding_key = embedding_index_key(app_settings.openai_embedding_model)
        retrieval = RetrievalService(
            repository,
            vector_store,
            openai_adapter,
            embedding_key,
            app_settings.rag_min_similarity,
            app_settings.rag_min_margin,
        )
        try:
            await retrieval.index_seeded_faqs(repository.tenant_id)
        except Exception:
            logger.exception("FAQ indexing failed; retrieval remains unavailable until indexed")
        admissions = AdmissionsService(repository, repository.tenant_id, retrieval, openai_adapter)
        payment_service = None
        key_id = app_settings.razorpay_key_id
        if (
            key_id
            and key_id.startswith("rzp_test_")
            and app_settings.razorpay_key_secret
            and app_settings.razorpay_webhook_secret
        ):
            payment_service = PaymentService(
                repository,
                repository.tenant_id,
                RazorpayAdapter(key_id, app_settings.razorpay_key_secret),
                app_settings.razorpay_webhook_secret,
            )
        elif any(
            (
                app_settings.razorpay_key_id,
                app_settings.razorpay_key_secret,
                app_settings.razorpay_webhook_secret,
            )
        ):
            logger.warning(
                "Razorpay payments disabled; configure a complete test-mode credential set "
                "with an rzp_test_ key ID"
            )
        app.state.repository = repository
        app.state.rag_ready = not repository.get_unembedded_faqs(
            repository.tenant_id, embedding_key
        )
        app.state.openai_adapter = openai_adapter
        app.state.admissions = admissions
        app.state.payment_service = payment_service
        app.state.telegram_enabled = bool(
            app_settings.telegram_bot_token and app_settings.telegram_webhook_secret
        )
        telegram_application = None
        if app_settings.telegram_bot_token and app_settings.telegram_webhook_secret:
            telegram_application = build_telegram_application(
                app_settings.telegram_bot_token,
                repository,
                admissions,
                openai_adapter,
                payment_service,
            )
            await start_application(telegram_application)
        elif app_settings.telegram_bot_token:
            logger.warning(
                "Telegram bot disabled; configure TELEGRAM_WEBHOOK_SECRET to enable webhook mode"
            )
        app.state.telegram_application = telegram_application
        try:
            yield
        finally:
            if telegram_application is not None:
                await stop_application(telegram_application)
            if openai_adapter is not None:
                await openai_adapter.close()

    app = FastAPI(title="AdmitFlow Demo", lifespan=lifespan)
    app.state.settings = app_settings
    app.include_router(dashboard_router)
    app.include_router(payment_router)
    app.include_router(telegram_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
