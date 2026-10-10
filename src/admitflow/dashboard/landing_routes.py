"""Public submission landing page (served without authentication)."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

BOT_URL = "https://t.me/crea34bot"


@router.get("/welcome", response_class=HTMLResponse)
def landing(request: Request) -> Response:
    # Intentionally public: this page carries no lead data and must not require staff login.
    return templates.TemplateResponse(
        request=request,
        name="landing.html",
        context={"bot_url": BOT_URL},
    )
