"""Local read-only lead dashboard."""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


def _repository(request: Request) -> Any:
    return request.app.state.repository


@router.get("/", response_class=HTMLResponse)
def leads_page(request: Request) -> HTMLResponse:
    repository = _repository(request)
    return templates.TemplateResponse(
        request=request,
        name="leads.html",
        context={
            "leads": repository.list_leads(repository.tenant_id),
            "rag_ready": request.app.state.rag_ready,
        },
    )


@router.get("/leads/{lead_id}", response_class=HTMLResponse)
def lead_detail(request: Request, lead_id: int) -> HTMLResponse:
    repository = _repository(request)
    lead = repository.get_lead(lead_id)
    if lead is None or lead["tenant_id"] != repository.tenant_id:
        raise HTTPException(status_code=404, detail="Lead not found")
    return templates.TemplateResponse(
        request=request,
        name="lead_detail.html",
        context={
            "lead": lead,
            "messages": repository.list_messages(lead_id),
            "rag_ready": request.app.state.rag_ready,
        },
    )
