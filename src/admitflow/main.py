"""FastAPI entrypoint and service composition."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from admitflow.adapters.openai import OpenAIAdapter
from admitflow.adapters.sqlite import Repository
from admitflow.adapters.telegram import (
    build_telegram_application,
    start_polling,
    stop_polling,
)
from admitflow.adapters.vector_store import VectorStore
from admitflow.config import Settings, get_settings
from admitflow.dashboard.routes import router as dashboard_router
from admitflow.services.admissions import AdmissionsService
from admitflow.services.retrieval import RetrievalService

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
        retrieval = RetrievalService(
            repository,
            vector_store,
            openai_adapter,
            app_settings.openai_embedding_model,
            app_settings.rag_min_similarity,
            app_settings.rag_min_margin,
        )
        try:
            await retrieval.index_seeded_faqs(repository.tenant_id)
        except Exception:
            logger.exception("FAQ indexing failed; retrieval remains unavailable until indexed")
        admissions = AdmissionsService(repository, repository.tenant_id, retrieval)
        app.state.repository = repository
        app.state.rag_ready = not repository.get_unembedded_faqs(
            repository.tenant_id, app_settings.openai_embedding_model
        )
        app.state.openai_adapter = openai_adapter
        app.state.admissions = admissions
        app.state.telegram_enabled = bool(app_settings.telegram_bot_token)
        telegram_application = None
        if app_settings.telegram_bot_token:
            telegram_application = build_telegram_application(
                app_settings.telegram_bot_token,
                repository,
                admissions,
                openai_adapter,
            )
            await start_polling(telegram_application)
        try:
            yield
        finally:
            if telegram_application is not None:
                await stop_polling(telegram_application)
            if openai_adapter is not None:
                await openai_adapter.close()

    app = FastAPI(title="AdmitFlow Demo", lifespan=lifespan)
    app.include_router(dashboard_router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
