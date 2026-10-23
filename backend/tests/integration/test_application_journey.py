"""Encrypted explicit application collection, replay safety and tenant-scoped staff review."""

import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest
from sqlalchemy import func, select

from src.core.security import decrypt_pii, encrypt_pii
from src.db.enums import LeadStatus, RuleOperator
from src.db.models import Application, Batch, Course, Lead, QualificationRule, TelegramBot
from src.engine.contracts import Event
from src.engine.journey import qualify, route
from src.telegram.callbacks import callback_data
from tests.integration.test_knowledge_workspace import signin
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_application_collection_is_explicit_encrypted_and_replay_safe(
    journey: dict[str, Any],
) -> None:
    async def exercise() -> uuid.UUID:
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            course = Course(
                tenant_id=tenant, name="Synthetic application course", application_fee=10000
            )
            bot = TelegramBot(
                tenant_id=tenant, telegram_bot_id=230, token_enc=encrypt_pii("synthetic-token")
            )
            db.add_all([course, bot])
            await db.flush()
            batch = Batch(
                tenant_id=tenant,
                course_id=course.id,
                name="Morning",
                capacity=10,
                seats_remaining=10,
            )
            db.add(batch)
            await db.flush()
            lead = Lead(tenant_id=tenant, current_course_id=course.id, current_batch_id=batch.id)
            db.add_all(
                [
                    lead,
                    QualificationRule(
                        tenant_id=tenant,
                        course_id=course.id,
                        field="age",
                        operator=RuleOperator.GTE,
                        value=18,
                    ),
                ]
            )
            await db.flush()
            memory: dict[str, Any] = {"facts": {"age": 21}}
            await qualify(db, lead, bot, memory, "", [])
            assert lead.status == LeadStatus.ADMISSION_READY
            counter = iter(range(1, 30))

            async def turn(text: str, callback: bool = False) -> Any:
                return await route(
                    db,
                    lead,
                    bot,
                    Event(
                        update_id=next(counter),
                        user_id=50,
                        chat_id=50,
                        message_id=1,
                        kind="callback" if callback else "text",
                        text=text,
                    ),
                    memory,
                )

            start = callback_data("apply", "start", lead.id, bot.id)
            reply = await turn(start, True)
            assert "full name" in reply.text.lower()
            await turn("Demo Student")
            invalid = await turn("tomorrow")
            assert "valid past date" in invalid.text
            for text in [
                "2005-01-01",
                "Demo Parent",
                "Synthetic test address",
                "Demo School",
            ]:
                reply = await turn(text)
            assert "review" in reply.text.lower()
            assert await db.scalar(select(func.count()).select_from(Application)) == 0
            await turn(callback_data("apply", "submit-expired", lead.id, bot.id), True)
            assert await db.scalar(select(func.count()).select_from(Application)) == 0
            submit = next(button.data for button in reply.buttons if "Submit" in button.text)
            reply = await turn(submit, True)
            assert "application" in reply.text.lower()
            await turn(submit, True)
            application = await db.scalar(select(Application).where(Application.lead_id == lead.id))
            assert (
                await db.scalar(
                    select(func.count())
                    .select_from(Application)
                    .where(Application.lead_id == lead.id)
                )
                == 1
            )
            assert "Demo Student" not in application.full_name_enc
            assert "Demo School" not in application.form_data_enc
            assert application.dob is None and application.previous_school is None
            assert "Demo School" in decrypt_pii(application.form_data_enc)
            assert lead.status == LeadStatus.PAYMENT_PENDING
            assert batch.seats_remaining == 10
            await turn("/courses")
            assert lead.status == LeadStatus.PAYMENT_PENDING
            await turn("Actually my age is 10")
            assert lead.status == LeadStatus.PAYMENT_PENDING
            assert memory["facts"]["age"] == 21
            await turn("/human")
            assert lead.status == LeadStatus.HANDED_OFF
            await db.commit()
            return application.id

    application_id = asyncio.run(exercise())
    client = journey["client"]
    signin(client)
    detail = client.get(f"/api/staff/applications/{application_id}")
    assert detail.status_code == 200, detail.text
    assert detail.json()["form"]["full_name"] == "Demo Student"
    requests = client.get("/api/staff/human-requests").json()
    request_id = next(
        item["id"] for item in requests if item["lead_id"] == detail.json()["lead_id"]
    )
    for action in ("acknowledge", "resolve", "resume"):
        assert (
            client.post(
                f"/api/staff/human-requests/{request_id}/{action}",
                headers={"X-AdmitFlow-Request": "1"},
            ).status_code
            == 200
        )
    assert (
        client.get(f"/api/staff/leads/{detail.json()['lead_id']}").json()["status"]
        == "payment_pending"
    )
    assert (
        client.post(
            f"/api/staff/applications/{application_id}/approve",
            headers={"X-AdmitFlow-Request": "1"},
        ).status_code
        == 409
    )
    signin(client, "second")
    assert client.get(f"/api/staff/applications/{application_id}").status_code == 404


def test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent(
    journey: dict[str, Any],
) -> None:
    async def seed() -> tuple[list[uuid.UUID], uuid.UUID]:
        tenant = journey["tenants"][0]
        async with journey["sessions"]() as db:
            course = Course(tenant_id=tenant, name="Synthetic one-seat course", application_fee=0)
            db.add(course)
            await db.flush()
            batch = Batch(
                tenant_id=tenant,
                course_id=course.id,
                name="Only intake",
                capacity=1,
                seats_remaining=1,
            )
            db.add(batch)
            await db.flush()
            ids = []
            for _ in range(2):
                lead = Lead(
                    tenant_id=tenant, current_course_id=course.id, current_batch_id=batch.id
                )
                db.add(lead)
                await db.flush()
                application = Application(
                    tenant_id=tenant,
                    lead_id=lead.id,
                    course_id=course.id,
                    batch_id=batch.id,
                    full_name_enc=encrypt_pii("Synthetic applicant"),
                )
                db.add(application)
                await db.flush()
                ids.append(application.id)
            await db.commit()
            return ids, batch.id

    ids, batch_id = asyncio.run(seed())
    client = journey["client"]
    signin(client)

    def approve(application_id: uuid.UUID) -> int:
        return client.post(
            f"/api/staff/applications/{application_id}/approve",
            headers={"X-AdmitFlow-Request": "1"},
        ).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(approve, ids))
    assert sorted(results) == [200, 409]
    winner = ids[results.index(200)]
    assert approve(winner) == 200

    async def verify() -> None:
        async with journey["sessions"]() as db:
            batch = await db.get(Batch, batch_id)
            assert batch.seats_remaining == 0

    asyncio.run(verify())
    signin(client, email="agent@example.test")
    assert approve(winner) == 403
    signin(client, "second")
    assert approve(winner) == 404
