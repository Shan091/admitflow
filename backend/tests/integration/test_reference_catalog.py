"""Reference programmes remain tenant-scoped and cannot create applications or invoices."""

import asyncio

import pytest
from sqlalchemy import delete, select

from src.db.models import Batch, Course, Lead, TelegramBot
from src.engine.journey import courses, fee_information, select_course
from tests.integration.test_adaptive_guidance import setup_guidance as setup_guidance
from tests.integration.test_knowledge_workspace import workspace as workspace
from tests.integration.test_telegram_journey import journey as journey

pytestmark = pytest.mark.integration


def test_reference_catalogue_has_no_fake_seats_free_fee_or_application(setup_guidance):
    async def exercise():
        async with setup_guidance["sessions"]() as db:
            lid, bid, cid, *_ = setup_guidance["guidance_ids"]
            lead, bot, course = (
                await db.get(Lead, lid),
                await db.get(TelegramBot, bid),
                await db.get(Course, cid),
            )
            course.is_reference = True
            course.reference_url = "https://www.jainuniversity.ac.in/kochi/programs.php"
            await db.execute(delete(Batch).where(Batch.course_id == cid))
            await db.flush()
            memory = {"facts": {}}
            listing = await courses(db, lead, bot, memory)
            assert course.name in [b.text for b in listing.buttons]
            reply = await select_course(db, lead, bot, memory, cid)
            assert "Published programme" in reply.text
            assert lead.current_course_id is None and "application_draft" not in memory
            fee = await fee_information(db, lead, memory, [cid])
            assert "unverified" in fee.text.lower() and "INR 0" not in fee.text
            assert (await db.scalars(select(Batch).where(Batch.course_id == cid))).all() == []

    asyncio.run(exercise())
