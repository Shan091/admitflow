"""Synthetic adaptive guidance through the real composer; no database or Telegram I/O."""

import asyncio
import json
import time
from pathlib import Path
from typing import Any

from src.db.enums import RuleOperator
from src.db.models import Course, Lead, QualificationRule, TelegramBot
from src.engine.contracts import Reply
from src.engine.guidance import catalog_status, interpret_turn, merge_evidence, request_decision
from src.engine.guidance_contracts import GuidanceMemory
from src.engine.guidance_interaction import INTERVIEW_PROBE, compose_reply, consume_answer
from src.scripts.evaluate_guidance import NAMESPACE
from src.telegram.callbacks import parse_callback


async def evaluate() -> dict[str, Any]:
    cases = [
        (
            "interest-first-novice",
            "Beginner Web Development",
            "Learn to create web pages and simple interactive websites from the beginning.",
            [
                "i like to study the tech industry",
                "like web development",
                "some",
                "I finished Class 12 science. My age is 20 and marks 70.",
                "I want to learn to create websites. Please show the suitable course now.",
            ],
        ),
        (
            "background-first-uncertain",
            "Digital Content Production",
            "Explore visual storytelling, creating graphics and editing digital media.",
            [
                "I finished Class 12 commerce. My age is 19 and marks 65. "
                "I am unsure what to study.",
                "[tap]",
                "I like drawing and creating pictures, but haven't tried design software.",
                "I want a course where I can explore visual storytelling. Show the options now.",
            ],
        ),
        (
            "specific-field-absent",
            "Digital Skills Foundation",
            "A synthetic introductory programme for the admissions demonstration.",
            [
                "I want to study web development, not general office skills. "
                "I finished Class 12 science, age 20, marks 70. "
                "If you do not have a verified web course, please tell me honestly.",
            ],
        ),
    ]
    rows = []
    expected = {"age": 18, "marks": 50}
    for name, title, description, messages in cases:
        course = Course(
            id=NAMESPACE,
            tenant_id=NAMESPACE,
            name=title,
            description=description,
            is_active=True,
            application_fee=0,
        )
        rules = [
            QualificationRule(
                tenant_id=NAMESPACE,
                course_id=course.id,
                field=field,
                operator=RuleOperator.GTE,
                value=value,
            )
            for field, value in expected.items()
        ]
        state = GuidanceMemory()
        facts: dict[str, Any] = {}
        memory: dict[str, Any] = {}
        lead, bot = Lead(id=NAMESPACE, tenant_id=NAMESPACE), TelegramBot(id=NAMESPACE)
        history: list[dict[str, str]] = []
        turns = []
        choices_seen = False
        last_reply: Reply | None = None
        passed = True
        for message in messages:
            if message == "[tap]":
                contextual = [
                    b
                    for b in (last_reply.buttons if last_reply else [])
                    if b.data.startswith("answer:")
                ]
                if contextual:
                    picked = contextual[0]
                    _, target = parse_callback(picked.data, lead.id, bot.id)
                    message = consume_answer(memory, target) or "Not sure yet"
                else:
                    message = "I care about enjoying what I learn."
            memory.pop("guidance_answers", None)
            before_notes, before_facts = list(state.notes), dict(facts)
            started = time.perf_counter()
            try:
                interpretation = await interpret_turn(message, state, facts, rules, history)
                merge_evidence(state, interpretation, message, facts=facts, expected=expected)
                entries = [(course, *catalog_status(course, rules, facts, True))]
                plan = await request_decision(
                    message, state, entries, facts, rules, history, complete=True
                )
                merge_evidence(state, plan, message, facts=facts, expected=expected)
                entries = [(course, *catalog_status(course, rules, facts, True))]
                if state.notes != before_notes or facts != before_facts:
                    state.questions_since_direction = 0
                reply = compose_reply(
                    plan, state, entries, expected, message, memory, lead, bot, complete=True
                )
                last_reply = reply
                choices_seen |= any(b.data.startswith("answer:") for b in reply.buttons)
                ok = not INTERVIEW_PROBE.search(reply.text) and lead.current_course_id is None
                if message == "some":
                    ok &= "marks" not in facts and "age" not in facts
                if name == "specific-field-absent":
                    ok &= not state.recommended_ids and "not verify a suitable course" in reply.text
                if "show" in message.lower() and name != "specific-field-absent":
                    ok &= course.id in state.recommended_ids
                passed &= bool(ok)
                turns.append(
                    {
                        "student": message,
                        "response": reply.text,
                        "options": [b.text for b in reply.buttons],
                        "facts": dict(facts),
                        "passed": bool(ok),
                        "elapsed_ms": round((time.perf_counter() - started) * 1000),
                    }
                )
                history.extend(
                    [
                        {"role": "user", "content": message},
                        {"role": "assistant", "content": reply.text},
                    ]
                )
            except Exception as error:
                passed = False
                turns.append(
                    {"student": message, "passed": False, "error_type": type(error).__name__}
                )
        if name != "specific-field-absent":
            passed &= choices_seen
        rows.append(
            {"id": name, "passed": passed, "contextual_choices_seen": choices_seen, "turns": turns}
        )
        print(json.dumps({"id": name, "passed": passed}), flush=True)
    return {
        "scope": "Synthetic OpenAI dialogue through production response composition; "
        "no database writes, Telegram sends, psychometric validity or outcome claim",
        "cases": rows,
        "passed": sum(r["passed"] for r in rows),
        "total": len(rows),
    }


def main() -> None:
    result = asyncio.run(evaluate())
    path = Path(__file__).resolve().parents[3] / "docs/event/SUPPORTIVE_GUIDANCE_RESULTS.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
