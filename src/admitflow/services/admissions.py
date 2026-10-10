"""Admissions flow orchestration with deterministic eligibility and fee answers."""

import re
from dataclasses import dataclass

from admitflow.adapters.sqlite import Repository
from admitflow.domain.pricing import format_inr_from_paise
from admitflow.domain.qualification import assess_eligibility
from admitflow.services.contracts import IntentRouter
from admitflow.services.retrieval import RetrievalService


@dataclass(frozen=True, slots=True)
class Reply:
    text: str
    buttons: tuple[tuple[str, str], ...] = ()


class AdmissionsService:
    def __init__(
        self,
        repository: Repository,
        tenant_id: str,
        retrieval: RetrievalService,
    ) -> None:
        self.repository = repository
        self.tenant_id = tenant_id
        self.retrieval = retrieval

    def start(self, telegram_user_id: str, username: str | None) -> tuple[int, Reply]:
        lead_id = self.repository.upsert_lead(self.tenant_id, telegram_user_id, username)
        courses = self.repository.list_courses(self.tenant_id)
        buttons = tuple((course.name, f"course:{course.id}") for course in courses)
        buttons += (("Just browsing", "browse"),)
        return lead_id, Reply(
            "Welcome to Demo Admissions Academy. This is fictional sample information. "
            "Use demo answers only; messages are saved locally. "
            "Choose a course or browse without applying.",
            buttons,
        )

    def browse(self, lead_id: int) -> Reply:
        self.repository.update_lead(lead_id, state="browsing")
        courses = self.repository.list_courses(self.tenant_id)
        descriptions = "\n".join(f"• {course.name}: {course.description}" for course in courses)
        return Reply(
            f"Here are the fictional sample courses:\n{descriptions}\n\n"
            "You can ask a question or select a course whenever you're ready."
        )

    def select_course(self, lead_id: int, course_id: str) -> Reply:
        course = self.repository.get_course(self.tenant_id, course_id)
        if course is None:
            return Reply(
                "That course is not available in this demo. Please choose a listed course."
            )
        self.repository.update_lead(
            lead_id,
            state="awaiting_grade12",
            selected_course_id=course.id,
            completed_grade12=None,
            marks_percent=None,
            eligible=None,
        )
        return Reply(
            f"You selected {course.name}. Have you completed Grade 12?",
            (("Yes", "grade12:yes"), ("No", "grade12:no")),
        )

    def answer_grade12(self, lead_id: int, completed: bool) -> Reply:
        lead = self.repository.get_lead(lead_id)
        if lead is None or not lead["selected_course_id"]:
            return Reply("Please select a course first with /start.")
        if not completed:
            self.repository.update_lead(
                lead_id,
                completed_grade12=False,
                eligible=False,
                state="not_eligible",
            )
            return Reply(
                "The sample requirements need Grade 12 completion, so you do not need to send "
                "marks. This is not a real admission decision."
            )
        self.repository.update_lead(
            lead_id,
            completed_grade12=completed,
            state="awaiting_marks",
        )
        return Reply("What was your overall Grade 12 percentage? Send a number from 0 to 100.")

    def answer_marks(self, lead_id: int, text: str) -> Reply:
        try:
            marks = float(text.strip().rstrip("%"))
        except ValueError:
            return Reply("Please send your overall percentage as a number from 0 to 100.")
        if not 0 <= marks <= 100:
            return Reply("Please send a percentage from 0 to 100.")
        lead = self.repository.get_lead(lead_id)
        if lead is None or not lead["selected_course_id"] or lead["completed_grade12"] is None:
            return Reply("Please select a course and answer the Grade 12 question first.")
        course = self.repository.get_course(self.tenant_id, str(lead["selected_course_id"]))
        if course is None:
            return Reply("The selected demo course is no longer available. Please start again.")
        result = assess_eligibility(
            completed_grade12=bool(lead["completed_grade12"]),
            marks_percent=marks,
            minimum_marks_percent=course.minimum_marks_percent,
        )
        state = "qualified" if result.eligible else "not_eligible"
        self.repository.update_lead(
            lead_id, marks_percent=marks, eligible=result.eligible, state=state
        )
        if result.eligible:
            return Reply(
                f"Your answers meet the sample requirements for {course.name}. "
                "This is not an admission decision; staff must confirm any real application."
            )
        return Reply(
            f"Based on the sample rules for {course.name}, {result.reason} "
            "This is not a real admission decision."
        )

    async def free_text(self, lead_id: int, text: str, intent_router: IntentRouter | None) -> Reply:
        lead = self.repository.get_lead(lead_id)
        if lead and lead["state"] == "awaiting_marks":
            return self.answer_marks(lead_id, text)
        if _is_refund_question(text):
            return Reply(
                "Refunds are not supported in this fictional demo. Please ask admissions "
                "staff about the institution's actual refund policy."
            )
        if _is_fee_question(text):
            if _is_unconfigured_fee_category(text):
                return Reply(
                    "The sample data only confirms the application fee. Tuition and "
                    "hostel/accommodation charges or inclusions are not confirmed; "
                    "please ask admissions staff."
                )
            course_id = (
                str(lead["selected_course_id"]) if lead and lead["selected_course_id"] else ""
            )
            if not course_id:
                courses = self.repository.list_courses(self.tenant_id)
                if len(courses) == 1:
                    course_id = courses[0].id
                else:
                    buttons = tuple((course.name, f"course:{course.id}") for course in courses)
                    return Reply("Which course's demo application fee do you mean?", buttons)
            fee = self.repository.get_fee_paise(self.tenant_id, course_id)
            course = self.repository.get_course(self.tenant_id, course_id)
            if fee is None or course is None:
                return Reply("I don't have a confirmed fee for that sample course.")
            return Reply(
                f"The sample application fee for {course.name} is "
                f"{format_inr_from_paise(fee)}. This fictional demo amount "
                "is stored in course data."
            )
        if intent_router is None:
            return Reply(
                "I can help you explore courses or check a sample FAQ. Send /start to begin."
            )
        try:
            route = await intent_router.route(text)
        except Exception:
            return Reply(
                "I couldn't classify that question just now. Please choose a course or try again."
            )
        if route == "knowledge_question":
            result = await self.retrieval.answer(self.tenant_id, text)
            if result is None:
                return Reply(
                    "I don't have a confirmed answer in the sample information. "
                    "Please ask the admissions team."
                )
            answer, source = result
            return Reply(f"{answer}\n\nSource: {source}")
        if route == "human_request":
            return Reply(
                "This demo cannot connect a live staff member yet. "
                "Please contact the institution directly."
            )
        if route == "course_browse":
            return self.browse(lead_id)
        return Reply(
            "I can help with the sample courses, eligibility, or FAQs. Send /start to see options."
        )


def _is_fee_question(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    price_terms = {
        "fee",
        "fees",
        "price",
        "cost",
        "tuition",
        "application fee",
        "charges",
        "ഫീസ്",
        "ചെലവ്",
        "शुल्क",
        "फीस",
        "कीमत",
        "kharcha",
        "fees kitna",
    }
    return any(term in normalized for term in price_terms)


def _is_unconfigured_fee_category(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    unconfigured_categories = {"hostel", "accommodation", "housing", "residence", "tuition"}
    return any(term in normalized for term in unconfigured_categories)


def _is_refund_question(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    return any(term in normalized for term in {"refund", "refundable", "chargeback"})
