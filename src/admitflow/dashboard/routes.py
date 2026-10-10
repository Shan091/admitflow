"""Local read-only lead dashboard."""

import hmac
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from admitflow.dashboard.auth import SESSION_COOKIE, SESSION_MAX_AGE, create_session, verify_session

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


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
    response = templates.TemplateResponse(
        request=request,
        name="leads.html",
        context={
            "leads": repository.list_leads(repository.tenant_id),
            "rag_ready": request.app.state.rag_ready,
            "staff_authenticated": True,
        },
    )
    response.headers["Cache-Control"] = "no-store"
    return response


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
