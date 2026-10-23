"""Discovery Node (Task 12).

Presents available courses as WhatsApp interactive lists/buttons.
Handles course selection and batch routing.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.enums import LeadStatus
from src.db.models.catalog import Batch, Course
from src.engine.state import EngineState
from src.whatsapp.sender import WhatsAppSender


async def present_courses(
    state: EngineState,
    db: AsyncSession,
    sender: WhatsAppSender,
    phone_number: str,
) -> EngineState:
    """Fetch active courses with available batches and present to user.

    Only shows courses that have at least one active batch with seats > 0.
    """
    query = (
        select(Course)
        .where(Course.tenant_id == state.tenant_id)
        .where(Course.is_active.is_(True))
        .join(Batch, Batch.course_id == Course.id)
        .where(Batch.is_active.is_(True))
        .where(Batch.seats_remaining > 0)
        .distinct()
    )
    result = await db.execute(query)
    courses = result.scalars().all()

    if not courses:
        await sender.send_text(
            to=phone_number,
            text="Currently, there are no open courses for enrollment. Please check back later.",
        )
        return state

    if len(courses) <= 3:
        buttons = [{"id": f"course_{c.id}", "title": c.name[:20]} for c in courses]
        await sender.send_buttons(
            to=phone_number,
            text="Please select a course to explore:",
            buttons=buttons,
        )
    else:
        rows = [{"id": f"course_{c.id}", "title": c.name[:24]} for c in courses[:10]]
        sections = [{"title": "Available Courses", "rows": rows}]
        await sender.send_list(
            to=phone_number,
            text="Please select a course to explore:",
            button_text="View Courses",
            sections=sections,
        )

    # Transition state to discovering if allowed
    if state.status != LeadStatus.DISCOVERING:
        try:
            state.transition_to(LeadStatus.DISCOVERING)
        except Exception:
            # If transition is not allowed, we leave it as is
            pass

    return state
