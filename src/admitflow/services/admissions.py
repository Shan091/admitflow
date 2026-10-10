"""Admissions flow orchestration with deterministic eligibility and fee answers."""

import re
from dataclasses import dataclass

from admitflow.adapters.sqlite import Repository
from admitflow.domain.discovery import recommend_courses
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
        buttons = (
            ("I know the course", "path:course"),
            ("I know the field", "path:field"),
            ("Help me explore", "path:explore"),
            ("Just browsing / ask a question", "path:browse"),
            ("🌐 Change language", "language:menu"),
            ("I'm a parent/guardian", "speaker:parent"),
        )
        return lead_id, Reply(
            "Welcome to Demo Admissions Academy. This is fictional sample information. "
            "Use demo answers only; messages are saved locally. "
            "What would be most useful? You can switch paths or language at any time. Demo copy.",
            buttons,
        )

    def begin_path(self, lead_id: int, path: str) -> Reply:
        self.repository.update_lead(
            lead_id,
            discovery_path=path,
            discovery_step=path,
            lifecycle_stage="discovering",
            readiness_status="exploring",
        )
        self.repository.save_fact(lead_id, "discovery_path", path)
        if path == "course":
            courses = self.repository.list_courses(self.tenant_id)
            return Reply(
                "Choose a course. These are fictional sample offerings.",
                tuple((course.name, f"course:{course.id}") for course in courses),
            )
        if path == "field":
            return self._field_choices(lead_id, "Which field interests you most?")
        if path == "explore":
            return self._field_choices(
                lead_id,
                "What kinds of topics or activities sound interesting? Pick one to start; "
                "you can skip or change it.",
            )
        return self.browse(lead_id)

    def choose_speaker(self, lead_id: int, speaker: str) -> Reply:
        if speaker not in {"student", "parent"}:
            return Reply("Please choose student or parent/guardian.")
        self.repository.save_fact(lead_id, "active_speaker", speaker, speaker)
        if speaker == "parent":
            return Reply(
                "I'll record preferences you share as the parent's. The learner's own interests "
                "should guide recommendations; invite them to share their view before I "
                "suggest courses.",
                (("Learner sharing now", "speaker:student"), ("Choose a path", "menu:start")),
            )
        return Reply(
            "I'll use the learner's own interests as the basis for recommendations.",
            (("Choose a path", "menu:start"),),
        )

    def confirm_parent_course(self, lead_id: int, course_id: str) -> Reply:
        self.repository.save_fact(lead_id, "active_speaker", "student", "student")
        return self.select_course(lead_id, course_id)

    def _field_choices(self, lead_id: int, prompt: str) -> Reply:
        self.repository.update_lead(lead_id, discovery_step="field")
        courses = self.repository.list_courses(self.tenant_id)
        fields = sorted({course.field for course in courses if course.field})
        buttons = tuple(
            (field.replace("/", " & ").replace("-", " ").title(), f"field:{field}")
            for field in fields
        )
        return Reply(
            prompt,
            buttons + (("Skip / browse all", "path:browse"), ("Pause for now", "discovery:pause")),
        )

    def recommend_field(self, lead_id: int, field: str) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        selected = next((course.field for course in courses if course.field == field), None)
        if selected is None:
            return self.handoff(
                lead_id, "The requested field is not present in the sample catalog."
            )
        speaker_fact = next(
            (
                fact
                for fact in self.repository.list_facts(lead_id)
                if fact["fact_key"] == "active_speaker"
            ),
            None,
        )
        speaker = str(speaker_fact["fact_value"]) if speaker_fact else "student"
        existing_field = next(
            (
                fact
                for fact in self.repository.list_facts(lead_id)
                if fact["fact_key"] == f"interest_field_{speaker}"
            ),
            None,
        )
        if existing_field is None or existing_field["fact_value"] != selected:
            self.repository.delete_fact(lead_id, "interest_activity_student")
            self.repository.delete_fact(lead_id, f"education_level_{speaker}")
            self.repository.update_lead(lead_id, education_level=None)
        self.repository.save_fact(lead_id, f"interest_field_{speaker}", selected, speaker)
        if speaker == "parent":
            return Reply(
                "I've recorded that as the parent's preference. To keep the student's goals first, "
                "please ask the learner to choose or confirm their own field before I "
                "recommend courses.",
                (("Learner sharing now", "speaker:student"),),
            )
        self.repository.update_lead(lead_id, discovery_step="level")
        return self._level_choices(lead_id)

    def _level_choices(self, lead_id: int) -> Reply:
        self.repository.update_lead(lead_id, discovery_step="level")
        levels = (
            ("Certificate / vocational", "vocational_certificate"),
            ("Diploma", "diploma"),
            ("Undergraduate", "undergraduate"),
            ("Postgraduate", "postgraduate"),
            ("Show all levels", "any"),
        )
        buttons = tuple((label, f"level:{value}") for label, value in levels)
        return Reply(
            "Which study level are you considering? You can skip this and compare across levels.",
            buttons
            + (("Back to fields", "discovery:back_field"), ("Pause for now", "discovery:pause")),
        )

    def choose_level(self, lead_id: int, level: str) -> Reply:
        valid_levels = {"vocational_certificate", "diploma", "undergraduate", "postgraduate", "any"}
        if level not in valid_levels:
            return Reply("Please choose one of the listed sample education levels.")
        lead_before = self.repository.get_lead(lead_id)
        previous_level = (
            str(lead_before["education_level"])
            if lead_before and lead_before["education_level"]
            else None
        )
        selected_level = None if level == "any" else level
        if previous_level != selected_level:
            self.repository.delete_fact(lead_id, "interest_activity_student")
        self.repository.update_lead(
            lead_id,
            education_level=selected_level,
            discovery_step="activity",
        )
        active = next(
            (
                fact
                for fact in self.repository.list_facts(lead_id)
                if fact["fact_key"] == "active_speaker"
            ),
            None,
        )
        speaker = str(active["fact_value"]) if active else "student"
        self.repository.save_fact(lead_id, f"education_level_{speaker}", level, speaker)
        return self._activity_choices(lead_id)

    def _activity_choices(self, lead_id: int) -> Reply:
        facts = self.repository.list_facts(lead_id)
        field_fact = next(
            (fact for fact in facts if fact["fact_key"] == "interest_field_student"), None
        )
        lead = self.repository.get_lead(lead_id)
        if field_fact is None:
            return self._field_choices(lead_id, "Which field would you like to explore?")
        courses = self.repository.list_courses(self.tenant_id)
        level = str(lead["education_level"]) if lead and lead["education_level"] else None
        activities = sorted(
            {
                activity
                for course in courses
                if course.field == field_fact["fact_value"]
                and (level is None or level == "any" or course.education_level == level)
                for activity in course.activities
            }
        )
        buttons = tuple(
            (_activity_label(activity), f"activity:{_activity_slug(activity)}")
            for activity in activities
        )
        self.repository.update_lead(lead_id, discovery_step="activity")
        return Reply(
            "Which activity sounds most interesting? Pick one or skip.",
            buttons
            + (
                ("Skip this question", "activity:skip"),
                ("Back", "discovery:back_level"),
                ("Pause for now", "discovery:pause"),
            ),
        )

    def choose_activity(self, lead_id: int, slug: str) -> Reply:
        activity: str | None = None
        if slug != "skip":
            facts = self.repository.list_facts(lead_id)
            selected_field = next(
                (
                    fact["fact_value"]
                    for fact in facts
                    if fact["fact_key"] == "interest_field_student"
                ),
                None,
            )
            lead = self.repository.get_lead(lead_id)
            selected_level = (
                str(lead["education_level"]) if lead and lead["education_level"] else None
            )
            activity = next(
                (
                    item
                    for course in self.repository.list_courses(self.tenant_id)
                    if (selected_field is None or course.field == selected_field)
                    and (selected_level is None or course.education_level == selected_level)
                    for item in course.activities
                    if _activity_slug(item) == slug
                ),
                None,
            )
            if activity is None:
                return Reply(
                    "That activity choice is not in the sample catalog. Please choose again."
                )
            self.repository.save_fact(lead_id, "interest_activity_student", activity, "student")
        self.repository.update_lead(lead_id, discovery_step="results")
        return self._recommendation_results(lead_id, activity)

    def _recommendation_results(self, lead_id: int, activity: str | None = None) -> Reply:
        facts = self.repository.list_facts(lead_id)
        field_fact = next(
            (fact for fact in facts if fact["fact_key"] == "interest_field_student"), None
        )
        if field_fact is None:
            return self._field_choices(lead_id, "Which field would you like to explore?")
        lead = self.repository.get_lead(lead_id)
        level = str(lead["education_level"]) if lead and lead["education_level"] else None
        matches = recommend_courses(
            self.repository.list_courses(self.tenant_id),
            interests={str(field_fact["fact_value"])},
            activities={activity} if activity else set(),
            level=level,
            limit=3,
        )
        if not matches:
            return self.handoff(
                lead_id, "No complete sample course matched the learner's selections."
            )
        buttons = tuple((item.course.name, f"course:{item.course.id}") for item in matches)
        summaries = "\n".join(
            f"• {item.course.name} ({item.course.education_level.replace('_', ' ')}): "
            f"{', '.join(item.reasons)}. "
            f"Sample entry: {'; '.join(item.course.prerequisites)}. "
            f"Sample medium: {item.course.medium}. "
            f"Sample language support: "
            f"{', '.join(item.course.language_support) or 'not specified'}."
            for item in matches
        )
        self.repository.update_lead(lead_id, discovery_step="results")
        return Reply(
            "Here are sample options from the catalog, based on the field you chose:\n"
            f"{summaries}\n\n"
            "These are examples, not an admission decision. Which would you like to explore?",
            buttons,
        )

    def pause_discovery(self, lead_id: int) -> Reply:
        self.repository.update_lead(lead_id, lifecycle_stage="paused")
        return Reply(
            "Paused. Your selected demo facts are saved locally; send /resume when you want "
            "to continue."
        )

    def resume_discovery(self, lead_id: int) -> Reply:
        lead = self.repository.get_lead(lead_id)
        if lead is None:
            return Reply("Send /start to begin a new demo conversation.")
        step = str(lead.get("discovery_step") or "")
        self.repository.update_lead(lead_id, lifecycle_stage="discovering")
        if step in {"field", "explore"}:
            return self._field_choices(lead_id, "Let's continue. Which field interests you?")
        if step == "level":
            return self._level_choices(lead_id)
        if step == "activity":
            return self._activity_choices(lead_id)
        if step == "results":
            fact = next(
                (
                    item
                    for item in self.repository.list_facts(lead_id)
                    if item["fact_key"] == "interest_activity_student"
                ),
                None,
            )
            return self._recommendation_results(lead_id, str(fact["fact_value"]) if fact else None)
        if step == "course":
            return self.begin_path(lead_id, "course")
        return self.browse(lead_id)

    def back_to_field(self, lead_id: int) -> Reply:
        return self._field_choices(lead_id, "Which field interests you?")

    def back_to_level(self, lead_id: int) -> Reply:
        return self._level_choices(lead_id)

    def choose_language(self, lead_id: int, language: str) -> Reply:
        labels = {"en": "English", "ml": "Malayalam", "hi": "Hindi", "hinglish": "Hinglish"}
        if language not in labels:
            return Reply("Please choose one of the listed demo languages.")
        self.repository.update_lead(lead_id, preferred_language=language)
        self.repository.save_fact(lead_id, "preferred_language", language)
        # The short demo flow is localized incrementally; unreviewed strings stay visibly marked.
        welcome = {
            "en": "English preference saved. Most demo replies are still in English; language "
            "copy is incomplete and needs fluent-speaker review.",
            "ml": "മലയാളം ഭാഷാ മുൻഗണന സേവ് ചെയ്തു. ഡെമോ മറുപടികളിൽ ഭൂരിഭാഗവും ഇപ്പോഴും ഇംഗ്ലീഷിലാണ്; "
            "മലയാളം പകർപ്പിന് ഭാഷാ വിദഗ്ധരുടെ പരിശോധന വേണം.",
            "hi": "हिंदी भाषा प्राथमिकता सहेजी गई। डेमो के ज़्यादातर जवाब अभी अंग्रेज़ी में हैं; "
            "हिंदी पाठ की समीक्षा ज़रूरी है।",
            "hinglish": "Hinglish preference save ho gayi. Demo ke most replies abhi English mein "
            "hain; translated copy ko fluent speaker se review karna baaki hai.",
        }[language]
        return Reply(
            welcome, (("Start / change path", "menu:start"), ("Choose language", "language:menu"))
        )

    def language_menu(self) -> Reply:
        return Reply(
            "Choose a demo language. Most replies are currently English; localized copy needs "
            "fluent-speaker review.",
            (
                ("English", "language:en"),
                ("മലയാളം", "language:ml"),
                ("हिन्दी", "language:hi"),
                ("Hinglish", "language:hinglish"),
            ),
        )

    def handoff(self, lead_id: int, reason: str) -> Reply:
        self.repository.update_lead(
            lead_id,
            lifecycle_stage="handed_off",
            readiness_status="needs_staff",
            handoff_status="pending",
        )
        self.repository.save_fact(lead_id, "handoff_reason", reason)
        return Reply(
            "I couldn't confirm a suitable option from the fictional catalog. I've flagged this "
            "conversation for staff in the demo dashboard. Live contact and response-time details "
            "are not configured."
        )

    def browse(self, lead_id: int) -> Reply:
        self.repository.update_lead(
            lead_id, state="browsing", lifecycle_stage="discovering", readiness_status="exploring"
        )
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
        facts = self.repository.list_facts(lead_id)
        active = next((fact for fact in facts if fact["fact_key"] == "active_speaker"), None)
        speaker = str(active["fact_value"]) if active else "student"
        if speaker == "parent":
            self.repository.save_fact(lead_id, "course_choice_parent", course.id, "parent")
            return Reply(
                f"I've recorded {course.name} as the parent's suggestion. The learner's own "
                "choice should guide the next step. Ask them to confirm if they want "
                "to explore it.",
                (("Learner wants to explore this", f"course:confirm:{course.id}"),),
            )
        self.repository.save_fact(lead_id, "course_choice_student", course.id, "student")
        if course.education_level != "undergraduate" or course.minimum_marks_percent <= 0:
            self.repository.update_lead(
                lead_id,
                state="browsing",
                lifecycle_stage="discovering",
                readiness_status="considering",
                selected_course_id=course.id,
                completed_grade12=None,
                marks_percent=None,
                eligible=None,
            )
            handoff = self.handoff(
                lead_id, f"Staff confirmation needed for sample course {course.id}"
            )
            return Reply(
                f"{course.name} is a fictional {course.education_level.replace('_', ' ')} sample. "
                f"Sample prerequisites: {'; '.join(course.prerequisites)}. "
                f"Sample medium: {course.medium}. Sample language support: "
                f"{', '.join(course.language_support) or 'not specified'}.\n\n{handoff.text}"
            )
        self.repository.update_lead(
            lead_id,
            state="awaiting_grade12",
            lifecycle_stage="qualifying",
            readiness_status="considering",
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
            lead_id,
            marks_percent=marks,
            eligible=result.eligible,
            state=state,
            lifecycle_stage="admission_ready" if result.eligible else "qualifying",
        )
        if result.eligible:
            return Reply(
                f"Your answers meet the sample requirements for {course.name}. "
                "This is not an admission decision; staff must confirm any real application. "
                "Would you like to continue with the fictional demo application fee?",
                (("Continue to demo fee", "payment:yes"), ("Browse courses", "path:browse")),
            )
        return Reply(
            f"Based on the sample rules for {course.name}, {result.reason} "
            "This is not a real admission decision."
        )

    async def free_text(self, lead_id: int, text: str, intent_router: IntentRouter | None) -> Reply:
        lead = self.repository.get_lead(lead_id)
        if lead and lead["state"] == "awaiting_marks":
            return self.answer_marks(lead_id, text)
        if _is_deletion_request(text):
            handoff = self.handoff(lead_id, "Student asked staff to delete their local data.")
            return Reply(
                "I've recorded your request for staff-mediated deletion of your local "
                "demo profile, "
                "messages, and payment record. Staff must review and perform the deletion. "
                f"{handoff.text}"
            )
        if _is_refund_question(text):
            handoff = self.handoff(
                lead_id, "Student asked about a refund policy not configured in the demo."
            )
            return Reply(
                "Refunds are not supported in this fictional demo, and the institution's real "
                f"refund policy is not confirmed. {handoff.text}"
            )
        if _is_fee_question(text):
            if _is_unconfigured_fee_category(text):
                handoff = self.handoff(
                    lead_id,
                    "Student asked about tuition/hostel charges absent from the sample catalog.",
                )
                return Reply(
                    "The sample data only confirms the application fee. Tuition and "
                    "hostel/accommodation charges or inclusions are not confirmed; "
                    f"{handoff.text}"
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
        if _is_language_concern(text):
            course_id = (
                str(lead["selected_course_id"]) if lead and lead["selected_course_id"] else ""
            )
            course = self.repository.get_course(self.tenant_id, course_id) if course_id else None
            if course is None:
                handoff = self.handoff(
                    lead_id,
                    "Language of instruction and support depend on the specific course; "
                    "catalog confirmation needed.",
                )
                return Reply(
                    "UNESCO's general guidance discusses how multilingual education can support "
                    "inclusive, equitable learning. That is not evidence that learning a new "
                    "language will improve any one student's outcome, and it does not confirm "
                    "the medium or proficiency rules for a course. The learner can weigh that "
                    "trade-off and choose; select a course to see its fictional sample facts.\n\n"
                    f"{handoff.text}"
                )
            handoff = self.handoff(
                lead_id,
                f"Student asked about course language requirements for {course.id}; "
                "exact proficiency rule is not seeded.",
            )
            support = ", ".join(course.language_support) or "not specified in the sample catalog"
            return Reply(
                f"For this fictional sample, the listed medium for {course.name} is "
                f"{course.medium}, and listed discussion support is {support}. The sample catalog "
                "does not confirm a required proficiency level or formal accommodation, so staff "
                "need to verify those details. UNESCO describes multilingual education as a way "
                "to support more inclusive, equitable learning; that general guidance does not "
                "promise an outcome for this course or student. Source: "
                "https://www.unesco.org/en/articles/languages-matter-global-guidance-multilingual-education\n\n"
                f"{handoff.text}"
            )
        if _is_accommodation_question(text):
            handoff = self.handoff(
                lead_id,
                "Student asked about hostel/accommodation availability not confirmed "
                "in sample facts.",
            )
            return Reply(
                "The fictional sample mentions a hostel, but actual availability, eligibility, "
                "pricing, and terms are not confirmed. "
                f"{handoff.text}"
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
                handoff = self.handoff(
                    lead_id, "Question could not be answered from confirmed sample information."
                )
                return Reply(
                    f"I don't have a confirmed answer in the sample information. {handoff.text}"
                )
            answer, source = result
            return Reply(f"{answer}\n\nSource: {source}")
        if route == "human_request":
            return self.handoff(lead_id, "Student requested a staff member.")
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


def _is_language_concern(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    return any(
        term in normalized
        for term in {
            "language",
            "english",
            "malayalam",
            "hindi",
            "hinglish",
            "language barrier",
            "ഭാഷ",
            "ഇംഗ്ലീഷ്",
            "भाषा",
            "अंग्रेज़ी",
            "bhasha",
        }
    )


def _is_deletion_request(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    return any(
        phrase in normalized
        for phrase in {
            "delete my data",
            "delete my conversation",
            "delete my profile",
            "remove my data",
            "erase my data",
            "forget my data",
            "delete this chat",
            "clear my information",
        }
    )


def _is_accommodation_question(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    return any(
        term in normalized for term in {"hostel", "accommodation", "dormitory", "residence hall"}
    )


def _activity_slug(activity: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", activity.casefold()).strip("-")


def _activity_label(activity: str) -> str:
    return activity[:1].upper() + activity[1:]
