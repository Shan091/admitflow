"""Low-effort answers and a bounded escape from interview-style discovery."""

import re
import uuid
from typing import TYPE_CHECKING, Any

from src.db.models import Lead, TelegramBot
from src.engine.contracts import Reply
from src.engine.guidance_contracts import GuidanceDecision, GuidanceMemory

if TYPE_CHECKING:
    from src.engine.guidance import Catalog

INTERVIEW_PROBE = re.compile(
    r"\b(?:describe|tell me (?:more )?about)\b.{0,100}"
    r"\b(?:project|portfolio|technolog|framework)\w*|"
    r"\b(?:what|which)\b.{0,70}\b(?:technolog|framework)\w*.{0,50}\b(?:use|used)\b|"
    r"\bprojects?\b.{0,50}\b(?:worked on|have (?:you )?built)\b",
    re.I,
)
STAFF_OFFER = re.compile(
    r"\b(?:ask|contact|talk|speak|connect|request|meet)\b.{0,40}"
    r"\b(?:staff|human|counsell?or|admissions (?:team|office))\b|"
    r"\b(?:staff|human)\s+(?:help|review|support)\b",
    re.I,
)


def needs_progress(plan: GuidanceDecision, state: GuidanceMemory) -> bool:
    if plan.action != "ask" or not plan.question or plan.question_field:
        return False
    if plan.outside_interests:
        return False
    return bool(INTERVIEW_PROBE.search(plan.question)) or state.questions_since_direction >= (
        3 if state.deeper else 2
    )


def answer_labels(plan: GuidanceDecision) -> list[str]:
    from src.engine.guidance import checked_text

    if plan.action != "ask" or not plan.question or plan.question_field:
        return []
    labels: list[str] = []
    for label in plan.answer_options:
        if (
            label.startswith("/")
            or "\n" in label
            or STAFF_OFFER.search(label)
            or label.casefold() in {s.casefold() for s in labels}
        ):
            continue
        try:
            checked_text(label)
        except ValueError:
            continue
        labels.append(label)
    if labels and not any(re.search(r"not sure|unsure|don't know", s, re.I) for s in labels):
        labels = [*labels[:3], "Not sure yet"]
    return labels[:4]


def consume_answer(memory: dict[str, Any], target: str) -> str | None:
    offer = memory.get("guidance_answers", {})
    nonce, _, index = target.rpartition("-")
    options = offer.get("options", [])
    if nonce != offer.get("nonce") or not index.isascii() or not index.isdecimal():
        return None
    if int(index) >= len(options):
        return None
    memory.pop("guidance_answers", None)
    return str(options[int(index)])


def add_response_controls(
    plan: GuidanceDecision,
    state: GuidanceMemory,
    memory: dict[str, Any],
    lead: Lead,
    bot: TelegramBot,
    reply: Reply,
    *,
    has_courses: bool,
) -> Reply:
    from src.engine.journey import button

    if not has_courses and needs_progress(plan, state):
        state.last_question = "What would help you most now?"
        state.last_field, state.pending_course, state.questions_since_direction = None, None, 0
        intro = (
            "No need to explain technical projects. We can explore your options together."
            if INTERVIEW_PROBE.search(plan.question or "")
            else "Let's take a useful next step at your pace."
        )
        return Reply(
            text=intro + "\n\n" + state.last_question,
            buttons=[
                button("Browse available courses", "courses", "all", lead, bot),
                button("Explore interests further", "guide", "deeper", lead, bot),
            ],
        )
    if has_courses or plan.action == "recommend" or plan.outside_interests:
        state.questions_since_direction = 0
    elif plan.question and not plan.question_field:
        state.questions_since_direction += 1
    labels = answer_labels(plan) if not has_courses else []
    if labels:
        nonce = uuid.uuid4().hex[:12]
        memory["guidance_answers"] = {"nonce": nonce, "options": labels}
        reply.buttons = [
            button(label, "answer", f"{nonce}-{i}", lead, bot) for i, label in enumerate(labels)
        ]
        if not memory.get("guidance_choice_hint_shown"):
            reply.text += "\n\nYou can also type your own answer."
            memory["guidance_choice_hint_shown"] = True
    return reply


def compose_reply(
    plan: GuidanceDecision,
    state: GuidanceMemory,
    entries: "Catalog",
    expected: dict[str, Any],
    text: str,
    memory: dict[str, Any],
    lead: Lead,
    bot: TelegramBot,
    *,
    complete: bool,
) -> Reply:
    """Compose the same verified response for inbox processing and provider evaluations."""
    from src.engine.guidance import (
        literal_quote,
        question_field,
        render_decision,
        selection_question,
    )
    from src.engine.journey import button

    if plan.action in {"recommend", "select"} and plan.matches:
        preference_notes = "\n".join(
            note.evidence
            for note in state.notes
            if note.topic in {"interest", "strength", "value", "goal", "decision"}
        )
        matches = [m for m in plan.matches if literal_quote(m.student_evidence, preference_notes)]
        if not matches:
            plan.response = ""
            if plan.action == "recommend":
                plan.action = "ask"
                plan.question = (
                    plan.question or "What kinds of activities would you enjoy learning?"
                )
        plan.matches = matches
    field = question_field(plan.question, plan.question_field, expected)
    if (
        plan.action == "ask"
        and field
        and field == state.last_field
        and state.last_question
        and not plan.matches
    ):
        plan.response = "We can return to entry details when you're ready."
        plan.question = "Would you like to keep exploring, or check entry requirements now?"
        plan.question_field = None
        plan.answer_options = ["Keep exploring", "Check entry requirements"]
    content, ids = render_decision(plan, state, entries, complete=complete, student_text=text)
    state.last_question = (
        selection_question(ids, entries) if plan.action == "select" else plan.question
    )
    state.last_field = (
        question_field(plan.question, plan.question_field, expected)
        if plan.action != "select"
        else None
    )
    plan.question_field = state.last_field
    state.recommended_ids = ids
    state.pending_course = ids[0] if plan.action == "select" and len(ids) == 1 else None
    state.turns += 1
    buttons = [
        button(next(c.name for c, _, _ in entries if c.id == cid), "course", cid.hex, lead, bot)
        for cid in ids
    ]
    if ids and not state.deeper:
        buttons.append(button("Explore my interests further", "guide", "deeper", lead, bot))
    return add_response_controls(
        plan, state, memory, lead, bot, Reply(text=content, buttons=buttons), has_courses=bool(ids)
    )
