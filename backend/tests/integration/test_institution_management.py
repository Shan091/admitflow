"""Real database management: administrator writes, role/tenant boundaries and input validation."""

from typing import Any

import pytest

from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


def test_catalog_writes_validate_rules_capacity_and_ownership(workspace: dict[str, Any]) -> None:
    client = workspace["client"]
    signin(client)
    body = {
        "name": "Managed synthetic course",
        "description": "Synthetic management acceptance",
        "application_fee": 10000,
        "is_active": True,
        "batches": [{"name": "Morning", "capacity": 20, "seats_remaining": 15}],
        "rules": [{"field": "age", "operator": ">=", "value": 18}],
    }
    response = client.post("/api/staff/catalog", json=body, headers=HEADERS)
    assert response.status_code == 201, response.text
    course_id = response.json()["id"]
    details = client.get(f"/api/staff/catalog/{course_id}").json()
    assert details["batches"][0]["capacity"] == 20
    assert details["rules"][0]["value"] == 18
    assert client.post("/api/staff/catalog", json=body).status_code == 403
    bad = {**body, "batches": [{"name": "Overfull", "capacity": 10, "seats_remaining": 11}]}
    assert (
        client.put(f"/api/staff/catalog/{course_id}", json=bad, headers=HEADERS).status_code == 422
    )
    bad = {**body, "rules": [{"field": "age", "operator": ">=", "value": "eighteen"}]}
    assert (
        client.put(f"/api/staff/catalog/{course_id}", json=bad, headers=HEADERS).status_code == 422
    )
    signin(client, email="agent@example.test")
    assert client.get(f"/api/staff/catalog/{course_id}").status_code == 200
    assert (
        client.put(f"/api/staff/catalog/{course_id}", json=body, headers=HEADERS).status_code == 403
    )
    signin(client, "second")
    assert client.get(f"/api/staff/catalog/{course_id}").status_code == 404
    assert client.delete(f"/api/staff/catalog/{course_id}", headers=HEADERS).status_code == 404
    signin(client)
    updated = {**body, "name": "Updated course", "batches": details["batches"]}
    assert (
        client.put(f"/api/staff/catalog/{course_id}", json=updated, headers=HEADERS).status_code
        == 200
    )
    assert client.delete(f"/api/staff/catalog/{course_id}", headers=HEADERS).status_code == 200
    assert client.get(f"/api/staff/catalog/{course_id}").json()["is_active"] is False


def test_settings_validate_timezone_hours_and_tenant_scope(workspace: dict[str, Any]) -> None:
    client = workspace["client"]
    signin(client)
    original = client.get("/api/staff/settings")
    assert original.status_code == 200
    body = {
        "name": "Synthetic managed institution",
        "timezone": "Asia/Kolkata",
        "business_hours": {"mon": {"start": "09:00", "end": "17:00"}},
        "reengagement_delay_days": 3,
        "retention_days": 180,
    }
    assert (
        client.put(
            "/api/staff/settings", json={**body, "timezone": "Invalid/Zone"}, headers=HEADERS
        ).status_code
        == 422
    )
    assert (
        client.put(
            "/api/staff/settings",
            json={**body, "business_hours": {"mon": {"start": "17:00", "end": "09:00"}}},
            headers=HEADERS,
        ).status_code
        == 422
    )
    assert client.put("/api/staff/settings", json=body, headers=HEADERS).status_code == 200
    assert client.get("/api/staff/settings").json()["name"] == body["name"]
    signin(client, "second")
    assert client.get("/api/staff/settings").json()["name"] != body["name"]
    signin(client, email="agent@example.test")
    assert client.put("/api/staff/settings", json=body, headers=HEADERS).status_code == 403


def test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(
    workspace: dict[str, Any],
) -> None:
    client = workspace["client"]
    signin(client)
    body = {
        "code": "test-offer",
        "discount_type": "percent",
        "amount": 10,
        "max_uses": 20,
        "is_active": True,
    }
    created = client.post("/api/staff/discounts", json=body, headers=HEADERS)
    assert created.status_code == 201, created.text
    discount_id = created.json()["id"]
    assert created.json()["code"] == "TEST-OFFER"
    assert created.json()["uses_count"] == 0
    assert client.post("/api/staff/discounts", json=body, headers=HEADERS).status_code == 409
    assert (
        client.put(
            f"/api/staff/discounts/{discount_id}", json={**body, "amount": 101}, headers=HEADERS
        ).status_code
        == 422
    )
    assert (
        client.put(
            f"/api/staff/discounts/{discount_id}", json={**body, "uses_count": 0}, headers=HEADERS
        ).status_code
        == 422
    )
    signin(client, "second")
    assert client.get("/api/staff/discounts").json() == []
    assert (
        client.put(f"/api/staff/discounts/{discount_id}", json=body, headers=HEADERS).status_code
        == 404
    )
    signin(client, email="agent@example.test")
    assert client.delete(f"/api/staff/discounts/{discount_id}", headers=HEADERS).status_code == 403
    signin(client)
    assert client.delete(f"/api/staff/discounts/{discount_id}", headers=HEADERS).status_code == 200
    assert client.get("/api/staff/discounts").json()[0]["is_active"] is False
