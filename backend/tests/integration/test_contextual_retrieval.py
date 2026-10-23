"""Course metadata scopes stay tenant-owned through staff search and student FAQ."""

import asyncio
import json
import uuid
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock

import pytest

from src.db.models import Course, Lead
from src.engine.journey import answer_question
from src.knowledge.processing import process_upload
from src.knowledge.scope import question_courses
from tests.integration.test_knowledge_workspace import fake_embeddings, send, signin
from tests.integration.test_knowledge_workspace import workspace as workspace

pytestmark = pytest.mark.integration
HEADERS = {"X-AdmitFlow-Request": "1"}


def test_course_scope_authority_search_and_faq(workspace: dict[str, Any], monkeypatch) -> None:
    client = workspace["client"]
    tenant, foreign_tenant = workspace["tenants"]

    async def seed():
        async with workspace["sessions"]() as db:
            courses = [
                Course(
                    tenant_id=t, name=name, application_fee=1000 if name == "NursingXYZ" else 2000
                )
                for t, name in (
                    (tenant, "NursingXYZ"),
                    (tenant, "CommerceXYZ"),
                    (foreign_tenant, "ForeignXYZ"),
                )
            ]
            db.add_all(courses)
            await db.commit()
            return [course.id for course in courses]

    nursing, commerce, foreign = asyncio.run(seed())
    signin(client)
    files = send(
        client,
        [
            ("scope/general.txt", b"The hostel reception opens at 9 AM."),
            ("scope/nursing.txt", b"NursingXYZ hostel is beside the library."),
            ("scope/commerce.txt", b"CommerceXYZ hostel is near the bus stop."),
        ],
    )["accepted"]
    assert (
        client.patch(
            f"/api/knowledge/documents/{files[1]['id']}/scope",
            headers=HEADERS,
            json={"course_id": str(nursing)},
        ).status_code
        == 409
    )

    async def index():
        for file in files:
            await process_upload(tenant, uuid.UUID(file["id"]))

    asyncio.run(index())
    for file, course in zip(files[1:], (nursing, commerce), strict=True):
        assert (
            client.patch(
                f"/api/knowledge/documents/{file['id']}/scope",
                headers=HEADERS,
                json={"course_id": str(course)},
            ).status_code
            == 200
        )
    view = {row["id"]: row for row in client.get("/api/knowledge/documents").json()}
    assert view[files[1]["id"]]["course_id"] == str(nursing)
    assert (
        client.patch(
            f"/api/knowledge/documents/{files[1]['id']}/scope",
            headers=HEADERS,
            json={"course_id": str(foreign)},
        ).status_code
        == 404
    )
    for field in ("scope", "search"):
        path = (
            f"/api/knowledge/documents/{files[1]['id']}/scope"
            if field == "scope"
            else "/api/knowledge/search"
        )
        signin(client, "second")
        if field == "scope":
            response = client.patch(path, headers=HEADERS, json={"course_id": None})
        else:
            response = client.post(
                path, headers=HEADERS, json={"query": "hostel", "course_id": str(nursing)}
            )
        assert response.status_code == 404
    signin(client, email="agent@example.test")
    assert (
        client.patch(
            f"/api/knowledge/documents/{files[1]['id']}/scope",
            headers=HEADERS,
            json={"course_id": None},
        ).status_code
        == 403
    )
    signin(client)
    result = client.post(
        "/api/knowledge/search",
        headers=HEADERS,
        json={"query": "hostel", "course_id": str(nursing)},
    )
    assert result.status_code == 200
    assert {row["source"] for row in result.json()["matches"]} == {
        "scope/general.txt",
        "scope/nursing.txt",
    }

    async def quotation(messages, **kwargs):
        payload = json.loads(messages[-1]["content"])
        expected = "CommerceXYZ" if "CommerceXYZ" in payload["question"] else "NursingXYZ"
        other = "NursingXYZ" if expected == "CommerceXYZ" else "CommerceXYZ"
        passages = payload["passages"]
        assert all(other not in passage["text"] for passage in passages)
        index = next(i for i, p in enumerate(passages) if expected in p["text"])
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {
                                "supported": True,
                                "passage": index,
                                "quote": passages[index]["text"],
                            }
                        )
                    )
                )
            ]
        )

    monkeypatch.setattr("src.engine.journey.embed_chunks", fake_embeddings)
    monkeypatch.setattr("src.engine.journey.generate_completion", quotation)

    async def exercise():
        async with workspace["sessions"]() as db:
            lead = Lead(tenant_id=tenant, current_course_id=nursing)
            assert "scope/nursing.txt" in (await answer_question(db, lead, {}, "Hostel?")).text
            reply = await answer_question(db, lead, {}, "CommerceXYZ hostel?")
            assert "scope/commerce.txt" in reply.text
            assert lead.current_course_id == nursing
            fees = await answer_question(db, lead, {}, "CommerceXYZ application fee?")
            assert fees.text.startswith("CommerceXYZ:")
            assert "INR 20.00" in fees.text and "INR 10.00" not in fees.text
            assert lead.current_course_id == nursing
            selected = await db.get(Course, nursing)
            assert set(
                await question_courses(db, tenant, "NursingXYZ and CommerceXYZ hostels?", selected)
            ) == {nursing, commerce}
            db.add(Course(tenant_id=tenant, name="NursingXYZ", application_fee=3000))
            await db.flush()
            other = Lead(tenant_id=tenant, current_course_id=commerce)
            ambiguous = await answer_question(db, other, {}, "NursingXYZ application fee?")
            assert ambiguous.text.startswith("Which course or topic")
            known = await answer_question(db, lead, {}, "NursingXYZ application fee?")
            assert "INR 10.00" in known.text and "INR 30.00" not in known.text

    asyncio.run(exercise())


def test_ambiguous_context_asks_without_search_or_fact_mutation(workspace, monkeypatch) -> None:
    client = workspace["client"]
    signin(client)
    file = send(client, [("ambiguity.txt", b"The library is open in the morning.")])["accepted"][0]
    tenant = workspace["tenants"][0]
    asyncio.run(process_upload(tenant, uuid.UUID(file["id"])))
    history = [{"role": "assistant", "content": "Nursing and commerce courses are available."}]
    monkeypatch.setattr("src.engine.journey.recent_history", AsyncMock(return_value=history))
    embed = AsyncMock()
    monkeypatch.setattr("src.engine.journey.embed_chunks", embed)

    async def decide(*args, **kwargs):
        assert kwargs["response_format"].__name__ == "ResolvedQuestion"
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"query":"Which course fee?","needs_clarification":true}'
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", decide)

    async def exercise():
        async with workspace["sessions"]() as db:
            memory = {"facts": {"age": 21}}
            reply = await answer_question(db, Lead(tenant_id=tenant), memory, "What does it cost?")
            assert reply.text.startswith("Which course or topic")
            assert memory == {"facts": {"age": 21}}
            embed.assert_not_awaited()

    asyncio.run(exercise())
