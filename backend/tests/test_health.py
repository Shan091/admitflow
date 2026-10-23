"""Tests for the FastAPI app: health check and Swagger UI."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_ok() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"


def test_docs_available() -> None:
    resp = client.get("/docs")
    assert resp.status_code == 200


def test_openapi_schema_served() -> None:
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert resp.json()["info"]["title"] == "AdmitFlow"
