"""Local read-only lead dashboard."""

import hmac
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from admitflow.dashboard.auth import (
    SESSION_COOKIE,
    SESSION_MAX_AGE,
    create_delete_demo_data_token,
    create_session,
    verify_session,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
DELETE_DEMO_DATA_CONFIRMATION = "DELETE ALL DEMO DATA"


def _repository(request: Request) -> Any:
    return request.app.state.repository


def _staff_authenticated(request: Request) -> bool:
    settings = request.app.state.settings
    return verify_session(
        request.cookies.get(SESSION_COOKIE),
        settings.staff_username,
        settings.staff_session_secret,
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> Response:
    if _staff_authenticated(request):
        return RedirectResponse("/", status_code=303)
    settings = request.app.state.settings
    configured = bool(
        settings.staff_username and settings.staff_password and settings.staff_session_secret
    )
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"configured": configured, "error": None},
    )


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request) -> Response:
    settings = request.app.state.settings
    if not (settings.staff_username and settings.staff_password and settings.staff_session_secret):
        raise HTTPException(status_code=503, detail="Staff login is not configured")
    try:
        fields = parse_qs((await request.body()).decode("utf-8"))
        username = fields.get("username", [""])[0]
        password = fields.get("password", [""])[0]
    except UnicodeDecodeError:
        username, password = "", ""
    username_matches = hmac.compare_digest(username.encode(), settings.staff_username.encode())
    password_matches = hmac.compare_digest(password.encode(), settings.staff_password.encode())
    valid = username_matches and password_matches
    if not valid:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"configured": True, "error": "The username or password is incorrect."},
            status_code=401,
        )
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        create_session(settings.staff_username, settings.staff_session_secret),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=settings.staff_cookie_secure,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/logout")
def logout() -> RedirectResponse:
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, samesite="lax")
    return response


@router.get("/", response_class=HTMLResponse)
def leads_page(request: Request) -> Response:
    if not _staff_authenticated(request):
        return RedirectResponse("/login", status_code=303)
    repository = _repository(request)
    settings = request.app.state.settings
    session_cookie = request.cookies.get(SESSION_COOKIE, "")
    csrf_token = create_delete_demo_data_token(session_cookie, settings.staff_session_secret)
    response = templates.TemplateResponse(
        request=request,
        name="leads.html",
        context={
            "leads": repository.list_leads(repository.tenant_id),
            "rag_ready": request.app.state.rag_ready,
            "staff_authenticated": True,
            "delete_demo_data_csrf_token": csrf_token,
            "reset_complete": request.query_params.get("reset") == "complete",
            "reset_rejected": request.query_params.get("reset") == "not-deleted",
        },
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@router.post("/admin/delete-all-demo-data")
async def delete_all_demo_data(request: Request) -> RedirectResponse:
    if not _staff_authenticated(request):
        return RedirectResponse("/login", status_code=303)
    settings = request.app.state.settings
    session_cookie = request.cookies.get(SESSION_COOKIE, "")
    if not session_cookie or not settings.staff_session_secret:
        return RedirectResponse("/login", status_code=303)
    try:
        fields = parse_qs((await request.body()).decode("utf-8"))
    except UnicodeDecodeError:
        fields = {}
    confirmation = fields.get("confirmation", [""])[0]
    csrf_token = fields.get("csrf_token", [""])[0]
    expected_token = create_delete_demo_data_token(session_cookie, settings.staff_session_secret)
    confirmation_matches = hmac.compare_digest(confirmation, DELETE_DEMO_DATA_CONFIRMATION)
    token_matches = hmac.compare_digest(csrf_token, expected_token)
    if not confirmation_matches or not token_matches:
        return RedirectResponse("/?reset=not-deleted", status_code=303)
    _repository(request).delete_all_demo_data()
    return RedirectResponse("/?reset=complete", status_code=303)


@router.get("/leads/{lead_id}", response_class=HTMLResponse)
def lead_detail(request: Request, lead_id: int) -> Response:
    if not _staff_authenticated(request):
        return RedirectResponse("/login", status_code=303)
    repository = _repository(request)
    lead = repository.get_lead(lead_id)
    if lead is None or lead["tenant_id"] != repository.tenant_id:
        raise HTTPException(status_code=404, detail="Lead not found")
    response = templates.TemplateResponse(
        request=request,
        name="lead_detail.html",
        context={
            "lead": lead,
            "messages": repository.list_messages(lead_id),
            "payment": repository.get_payment_for_lead(repository.tenant_id, lead_id),
            "rag_ready": request.app.state.rag_ready,
            "staff_authenticated": True,
        },
    )
    response.headers["Cache-Control"] = "no-store"
    return response
