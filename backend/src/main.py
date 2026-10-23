"""FastAPI application entry point.

Boots the API, manages the TaskIQ broker lifecycle, exposes a health check,
and provides a ``/debug`` router for worker verification (Task 3).
Domain routers (webhooks, dashboard REST) are wired in later tasks.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.core.settings import get_settings
from src.tasks.broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Start / stop the TaskIQ broker alongside the FastAPI process.

    The ``is_worker_process`` guard prevents the API process from pulling
    tasks off the queue — only the ``taskiq worker`` CLI does that.
    Startup is still needed so the API can *enqueue* tasks and query results.
    """
    if not broker.is_worker_process:
        await broker.startup()
    recovery = None
    integration_recovery = None
    if get_settings().database_url and get_settings().integration_recovery_enabled:
        from src.integrations.delivery import recovery_loop as integration_loop

        integration_recovery = asyncio.create_task(integration_loop())
    if get_settings().database_url and get_settings().knowledge_recovery_enabled:
        from src.knowledge.processing import recovery_loop

        recovery = asyncio.create_task(recovery_loop())
    try:
        yield
    finally:
        if integration_recovery:
            integration_recovery.cancel()
            await asyncio.gather(integration_recovery, return_exceptions=True)
        if recovery:
            recovery.cancel()
            await asyncio.gather(recovery, return_exceptions=True)
        if not broker.is_worker_process:
            await broker.shutdown()


def create_app() -> FastAPI:
    """Application factory — builds and configures the FastAPI instance."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Wire up routers
    from src.whatsapp.webhook import router as webhook_router

    application.include_router(webhook_router, prefix="/api/webhook")
    from src.knowledge.api import router as knowledge_router
    from src.knowledge.limits import UploadBodyLimit
    from src.payments.webhook import router as payments_router
    from src.staff.accounts import router as accounts_router
    from src.staff.analytics import router as analytics_router
    from src.staff.applications import router as applications_router
    from src.staff.auth import router as staff_router
    from src.staff.copilot import router as copilot_router
    from src.staff.exports import router as exports_router
    from src.staff.integrations import router as integrations_router
    from src.staff.leads import router as leads_router
    from src.staff.management import router as management_router
    from src.staff.notifications import router as notifications_router
    from src.staff.operations import router as staff_operations_router
    from src.staff.payments import router as staff_payments_router
    from src.staff.privacy import router as privacy_router

    application.add_middleware(UploadBodyLimit)
    application.include_router(staff_router)
    application.include_router(accounts_router)
    application.include_router(analytics_router)
    application.include_router(exports_router)
    application.include_router(integrations_router)
    application.include_router(notifications_router)
    application.include_router(leads_router)
    application.include_router(management_router)
    application.include_router(applications_router)
    application.include_router(payments_router)
    application.include_router(staff_payments_router)
    application.include_router(privacy_router)
    application.include_router(staff_operations_router)
    application.include_router(copilot_router)
    application.include_router(knowledge_router)

    # ------------------------------------------------------------------
    # System endpoints
    # ------------------------------------------------------------------
    @application.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        """Liveness probe used by the platform and smoke tests."""
        return {"status": "ok", "env": settings.app_env}

    @application.get("/ready", tags=["system"])
    async def ready() -> dict[str, str]:
        """Data-store readiness; never performs a paid model or Telegram request."""
        if not settings.database_url or not settings.redis_url:
            raise HTTPException(503, "Database and Redis must be configured.")
        from sqlalchemy import text

        from src.core.redis import get_redis
        from src.db.session import get_engine

        try:
            async with asyncio.timeout(5):
                async with get_engine().connect() as connection:
                    await connection.execute(text("SELECT 1"))
                await get_redis().ping()
        except Exception:
            raise HTTPException(503, "A required data store is unavailable.") from None
        return {"status": "ready", "scope": "database_and_redis"}

    # ------------------------------------------------------------------
    # Debug endpoints (verification of background worker — Task 3)
    # ------------------------------------------------------------------
    @application.get(
        "/debug/enqueue-ping", tags=["debug"], include_in_schema=settings.app_env == "dev"
    )
    async def enqueue_ping() -> dict[str, str]:
        """Enqueue a ``ping`` task and return the task ID.

        Use this to confirm the TaskIQ broker pipeline is operational:
        enqueue → Redis → worker → result backend.
        """
        if settings.app_env != "dev":
            raise HTTPException(404, "Not found")
        from src.tasks.processing import ping

        result = await ping.kiq("pong")
        return {"task_id": result.task_id}

    return application


app = create_app()
