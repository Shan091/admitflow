"""Bounded synthetic live course-guidance scenarios; no database writes or sends."""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

from src.db.enums import RuleOperator
from src.db.models import Course, QualificationRule
from src.engine.guidance import (
    catalog_status,
    interpret_turn,
    merge_evidence,
    question_field,
    render_decision,
    request_decision,
    selection_question,
)
from src.engine.guidance_contracts import GuidanceDecision, GuidanceMemory, Note

NAMESPACE = uuid.UUID("a8ee4b25-78db-454f-9bf5-c5e5e905b2cc")


def fixture() -> tuple[list[Course], list[QualificationRule]]:
    courses = [
        Course(
            id=uuid.uuid5(NAMESPACE, name),
            tenant_id=NAMESPACE,
            name=name,
            description=description,
            application_fee=50000,
            is_active=True,
        )
        for name, description in [
            ("Data and Reporting", "Explore spreadsheets, data cleaning and practical dashboards."),
            (
                "Digital Content Production",
                "Explore visual storytelling and editing digital media.",
            ),
            ("Supply Chain Operations", "Explore inventory planning and coordinating deliveries."),
            (
                "Healthcare Office Skills",
                "Administrative records and communication, not clinical nursing.",
            ),
        ]
    ]
    rules = [
        QualificationRule(
            course_id=c.id, tenant_id=NAMESPACE, field=field, operator=RuleOperator.GTE, value=value
        )
        for c in courses
        for field, value in [("age", 18), ("marks", 50)]
    ]
    return courses, rules


def scenarios() -> list[dict[str, Any]]:
    return [
        {
            "id": "uncertain",
            "text": "I finished Class 12 science. I am 18 with 76 marks. "
            "I like explaining things to classmates, but I am not sure what to study.",
        },
        {
            "id": "decided",
            "text": "I have decided on Data and Reporting because I enjoy "
            "spreadsheets and making dashboards. I am 21 with 72 marks and finished Class 12. "
            "I don't want a quiz; please help me proceed.",
        },
        {
            "id": "unfamiliar-course",
            "text": "I finished Class 12 commerce, age 19, marks 65. "
            "I have only heard of BCom, but I enjoyed planning stock and coordinating deliveries "
            "for our school fair. I want to see less familiar options that fit that interest.",
        },
        {
            "id": "unavailable-interest",
            "text": "I am 20 with 80 marks and finished Class 12 biology. "
            "I only want marine biology and field research. If you don't offer it, please say so. "
            "I do not want an office or computing course as a substitute.",
        },
        {
            "id": "known-ineligible",
            "text": "I am 17 with marks 40 and want Data and Reporting. "
            "I enjoy spreadsheets. Do not pretend that I meet the requirements.",
        },
        {
            "id": "correction",
            "notes": [Note(topic="interest", evidence="I enjoy helping in healthcare")],
            "text": "Actually I no longer want healthcare. I prefer making dashboards and "
            "working with spreadsheets now. I am 21 with 70 marks and finished Class 12.",
        },
        {
            "id": "budget-refusal",
            "last": "What budget would work for you?",
            "text": "I prefer not to share my budget. "
            "I finished Class 12 and enjoy visual storytelling. "
            "I am 20 with 70 marks. Please don't ask about money again.",
        },
        {"id": "faq-interruption", "text": "Where is the campus?"},
        {
            "id": "confidence-not-ability",
            "text": "I am 21 with 70 marks and finished Class 12. "
            "I enjoy spreadsheets and have made a small dashboard, but I don't feel confident "
            "about advanced maths. Can we explore the data course without assuming I am incapable?",
        },
        {
            "id": "clinical-mismatch",
            "text": "I am 20 with 75 marks and finished Class 12 biology. "
            "I only want to become a registered nurse and work clinically with patients. "
            "Healthcare office administration would not meet that goal.",
        },
        {
            "id": "deeper",
            "deeper": True,
            "notes": [Note(topic="interest", evidence="I enjoy drawing")],
            "text": "I would like to explore this more deeply. I haven't tried design software "
            "yet, but I enjoy drawing stories. What should we explore next?",
        },
        {"id": "human-request", "text": "Can I speak to a human counsellor about my choices?"},
        {
            "id": "financial-priorities",
            "text": "I am 21 with 70 marks and finished Class 12 commerce. "
            "I enjoyed planning stock "
            "and coordinating deliveries at a school event. Salary and affordable study matter "
            "to me, but I know you cannot promise earnings. I would like to explore options.",
        },
    ]


async def evaluate() -> dict[str, object]:
    courses, rules = fixture()
    rows: list[dict[str, object]] = []
    for scenario in scenarios():
        state = GuidanceMemory(
            notes=scenario.get("notes", []),
            deeper=scenario.get("deeper", False),
            last_question=scenario.get("last"),
        )
        facts: dict[str, Any] = {}
        entries = [
            (c, *catalog_status(c, [r for r in rules if r.course_id == c.id], facts, True))
            for c in courses
        ]
        try:
            interpreted = await interpret_turn(scenario["text"], state, facts, rules, [])
            merge_evidence(
                state, interpreted, scenario["text"], facts=facts, expected={"age": 18, "marks": 50}
            )
            entries = [
                (c, *catalog_status(c, [r for r in rules if r.course_id == c.id], facts, True))
                for c in courses
            ]
            plan = (
                await request_decision(
                    scenario["text"], state, entries, facts, rules, [], complete=True
                )
                if interpreted.intent == "guidance"
                else GuidanceDecision(action="ask", stage=state.stage)
            )
            action = plan.action if interpreted.intent == "guidance" else interpreted.intent
            if interpreted.intent == "guidance":
                merge_evidence(
                    state, plan, scenario["text"], facts=facts, expected={"age": 18, "marks": 50}
                )
            entries = [
                (c, *catalog_status(c, [r for r in rules if r.course_id == c.id], facts, True))
                for c in courses
            ]
            text: str
            choices: list[uuid.UUID]
            if action in {"faq", "handoff", "qualification", "browse"}:
                text, choices = action, []
            else:
                text, choices = render_decision(
                    plan, state, entries, complete=True, student_text=scenario["text"]
                )
            ok = all(
                next(status for c, status, _ in entries if c.id == cid)
                not in {"not_eligible", "unavailable"}
                for cid in choices
            )
            key = scenario["id"]
            if key == "decided":
                ok &= courses[0].id in choices and plan.stage == "decided"
            if key == "unfamiliar-course":
                ok &= courses[2].id in choices
            if key in {"unavailable-interest", "clinical-mismatch"}:
                ok &= not choices and "could not verify" in text.lower()
            if key == "known-ineligible":
                ok &= not choices
            if key == "correction":
                ok &= not any("helping in healthcare" in n.evidence for n in state.notes)
            if key == "budget-refusal":
                ok &= not any(
                    w in (plan.question or "").lower() for w in ["budget", "money", "income"]
                )
            if key == "faq-interruption":
                ok &= action == "faq"
            if key == "human-request":
                ok &= action == "handoff"
            if key == "deeper":
                ok &= plan.action == "ask" and bool(plan.question)
            if key == "uncertain":
                ok &= plan.action in {"ask", "recommend"} and bool(state.notes)
            rows.append(
                {
                    "id": key,
                    "passed": bool(ok),
                    "action": action,
                    "stage": state.stage,
                    "question": selection_question(choices, entries)
                    if plan.action == "select"
                    else plan.question,
                    "matched_courses": [c.name for c in courses if c.id in choices],
                    "response": text,
                    "profile": state.model_dump(mode="json"),
                    "facts": facts,
                }
            )
        except Exception as error:
            rows.append({"id": scenario["id"], "passed": False, "error_type": type(error).__name__})
        print(
            json.dumps(
                {k: v for k, v in rows[-1].items() if k in {"id", "passed", "action", "error_type"}}
            ),
            flush=True,
        )
    return {
        "scope": "13 synthetic live OpenAI guidance scenarios; no psychometric validity or "
        "real-student outcome claim; no DB writes or Telegram sends",
        "cases": rows,
        "passed": sum(r["passed"] is True for r in rows),
        "total": len(rows),
    }


async def evaluate_dialogues() -> dict[str, object]:
    """Exercise persistent state, not just independent single-message answers."""
    courses, rules = fixture()
    dialogues = [
        (
            "changing-preference",
            False,
            [
                "I am 20 with 70 marks and finished Class 12. I enjoy spreadsheets and visual "
                "storytelling. I am comparing Data and Reporting with Digital Content Production.",
                "Actually I prefer visual storytelling; data is just a hobby. "
                "I would rather pursue Digital Content Production. No more alternatives please.",
                "Where is the campus?",
                "Let's return to Digital Content Production. I would like to proceed with it.",
            ],
        ),
        (
            "academic-corrections",
            False,
            [
                "I am 21 with 70 marks and finished Class 12. I enjoy spreadsheets and making "
                "dashboards. Please show me the Data and Reporting option.",
                "Actually my age is 17, not 21. I still enjoy making dashboards.",
                "I meant I'm 21, not 17. Please continue with the data option.",
            ],
        ),
        (
            "optional-depth",
            True,
            [
                "I am 20 with 70 marks and finished Class 12. I enjoy drawing stories, but "
                "have never tried design software. I want to explore my interests more deeply.",
                "I enjoyed arranging photos and telling a story for our community newsletter. "
                "I prefer creative work to keeping administrative records.",
                "That is enough exploration. Please show one or two suitable available courses "
                "now instead of asking more assessment questions.",
            ],
        ),
    ]
    results: list[dict[str, object]] = []
    for name, deeper, messages in dialogues:
        state = GuidanceMemory(deeper=deeper)
        facts: dict[str, Any] = {}
        history: list[dict[str, str]] = []
        turns: list[dict[str, object]] = []
        passed = True
        for i, message in enumerate(messages):
            try:
                entries = [
                    (c, *catalog_status(c, [r for r in rules if r.course_id == c.id], facts, True))
                    for c in courses
                ]
                interpreted = await interpret_turn(message, state, facts, rules, history)
                merge_evidence(
                    state, interpreted, message, facts=facts, expected={"age": 18, "marks": 50}
                )
                entries = [
                    (c, *catalog_status(c, [r for r in rules if r.course_id == c.id], facts, True))
                    for c in courses
                ]
                plan = (
                    await request_decision(
                        message, state, entries, facts, rules, history, complete=True
                    )
                    if interpreted.intent == "guidance"
                    else GuidanceDecision(action="ask", stage=state.stage)
                )
                action = plan.action if interpreted.intent == "guidance" else interpreted.intent
                choices: list[uuid.UUID] = []
                if action == "faq":
                    answer = "[FAQ delegated to approved institution knowledge]"
                else:
                    merge_evidence(
                        state, plan, message, facts=facts, expected={"age": 18, "marks": 50}
                    )
                    entries = [
                        (
                            c,
                            *catalog_status(
                                c, [r for r in rules if r.course_id == c.id], facts, True
                            ),
                        )
                        for c in courses
                    ]
                    answer, choices = render_decision(
                        plan, state, entries, complete=True, student_text=message
                    )
                    state.last_question = (
                        selection_question(choices, entries)
                        if plan.action == "select"
                        else plan.question
                    )
                    state.last_field = (
                        question_field(plan.question, plan.question_field, {"age": 18, "marks": 50})
                        if plan.action != "select"
                        else None
                    )
                    state.pending_course = (
                        choices[0] if plan.action == "select" and len(choices) == 1 else None
                    )
                    state.recommended_ids = choices
                ok = True
                if name == "changing-preference" and i in {1, 3}:
                    ok = courses[1].id in choices and courses[0].id not in choices
                if name == "changing-preference" and i == 2:
                    ok = action == "faq"
                if name == "academic-corrections" and i == 1:
                    ok = facts.get("age") == 17 and not choices
                if name == "academic-corrections" and i == 2:
                    ok = facts.get("age") == 21 and courses[0].id in choices
                if name == "optional-depth" and i == 2:
                    ok = plan.action in {"recommend", "select"} and courses[1].id in choices
                passed &= ok
                turns.append(
                    {
                        "student": message,
                        "action": action,
                        "response": answer,
                        "facts": dict(facts),
                        "stage": state.stage,
                        "passed": ok,
                    }
                )
                history.extend(
                    [{"role": "user", "content": message}, {"role": "assistant", "content": answer}]
                )
            except Exception as error:
                passed = False
                turns.append(
                    {"student": message, "passed": False, "error_type": type(error).__name__}
                )
        results.append({"id": name, "passed": passed, "turns": turns})
        print(json.dumps({"dialogue": name, "passed": passed}), flush=True)
    return {
        "scope": "Three synthetic multi-turn OpenAI conversations; no writes or sends",
        "cases": results,
        "passed": sum(r["passed"] is True for r in results),
        "total": len(results),
    }


def main() -> None:
    report = asyncio.run(evaluate())
    dialogues = asyncio.run(evaluate_dialogues())
    report["dialogues"] = dialogues
    target = Path(__file__).resolve().parents[3] / "docs/event/GUIDANCE_EVALUATION_RESULTS.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "total": report["total"]}))
    if report["passed"] != report["total"] or dialogues["passed"] != dialogues["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
