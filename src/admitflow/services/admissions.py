"""Admissions flow orchestration with deterministic eligibility and fee answers."""

import hashlib
import json
import re
from dataclasses import dataclass, replace

from admitflow.adapters.sqlite import Repository
from admitflow.domain.discovery import (
    CourseMatch,
    has_sufficient_guidance_context,
    recommend_courses,
)
from admitflow.domain.models import Course, DiscoveryTurn, RetractedPreference
from admitflow.domain.pricing import format_inr_from_paise
from admitflow.domain.qualification import assess_eligibility
from admitflow.services.contracts import DiscoveryInterpreter, IntentRouter
from admitflow.services.retrieval import RetrievalService

_FIELD_CHOICES_PROMPT = "Which field interests you most?"
_EXPLORE_CHOICES_PROMPT = (
    "What kinds of topics or activities sound interesting? Pick one to start; "
    "you can skip or change it."
)


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
        discovery_interpreter: DiscoveryInterpreter | None = None,
    ) -> None:
        self.repository = repository
        self.tenant_id = tenant_id
        self.retrieval = retrieval
        self.discovery_interpreter = discovery_interpreter

    def start(self, telegram_user_id: str, username: str | None) -> tuple[int, Reply]:
        lead_id = self.repository.upsert_lead(self.tenant_id, telegram_user_id, username)
        processing = self.ai_processing_enabled(lead_id)
        language = self.preferred_language(lead_id)
        if not processing:
            return lead_id, self._tap_only_prompt(language)
        return lead_id, self._discovery_prompt(language)

    def preferred_language(self, lead_id: int) -> str:
        lead = self.repository.get_lead(lead_id)
        language = str(lead["preferred_language"]) if lead else "en"
        return language if language in {"en", "ml", "hi", "hinglish"} else "en"

    def ai_processing_enabled(self, lead_id: int) -> bool:
        facts = {
            str(item["fact_key"]): str(item["fact_value"])
            for item in self.repository.list_facts(lead_id)
        }
        if "openai_processing_enabled" in facts:
            return facts["openai_processing_enabled"] == "yes"
        # Respect opt-outs saved by older versions which used this consent-named fact.
        return facts.get("openai_processing_consent") != "no"

    def set_ai_processing_enabled(self, lead_id: int, enabled: bool) -> Reply:
        speaker_fact = next(
            (
                item
                for item in self.repository.list_facts(lead_id)
                if item["fact_key"] == "active_speaker"
            ),
            None,
        )
        speaker = str(speaker_fact["fact_value"]) if speaker_fact else "unknown"
        self.repository.save_fact(
            lead_id, "openai_processing_enabled", "yes" if enabled else "no", speaker
        )
        language = self.preferred_language(lead_id)
        if enabled:
            return self._discovery_prompt(language)
        return self._tap_only_prompt(language)

    async def choose_guidance_signal(
        self,
        lead_id: int,
        *,
        activity_slug: str | None = None,
        level: str | None = None,
    ) -> Reply:
        """Record a validated quick reply and continue the same adaptive turn policy."""
        if (activity_slug is None) == (level is None):
            return Reply("Choose one follow-up option so I can continue.")
        valid_levels = {
            "vocational_certificate",
            "diploma",
            "undergraduate",
            "postgraduate",
        }
        if level is not None and level not in valid_levels:
            return Reply("Please choose one of the listed sample education levels.")
        activities = {
            activity
            for course in self.repository.list_courses(self.tenant_id)
            for activity in course.activities
            if activity_slug is not None and _activity_slug(activity) == activity_slug
        }
        if activity_slug is not None and not activities:
            return Reply("That activity choice is not in the sample catalog. Please choose again.")
        turn = DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=(),
            education_level=level,
            interests=(),
            activities=tuple(sorted(activities)),
            unsure=False,
            correct_previous=False,
        )
        return await self._handle_discovery_turn(lead_id, turn, "")

    async def choose_guidance_goal(self, lead_id: int, goal_slug: str | None) -> Reply:
        """Accept only study goals present in the fictional course catalog."""
        if goal_slug is None:
            return self._present_guidance(lead_id)
        goals = {
            goal
            for course in self.repository.list_courses(self.tenant_id)
            for goal in course.learning_goals
            if _goal_slug(goal) == goal_slug
        }
        if not goals:
            return Reply("That study goal is not in the sample catalog. Please choose again.")
        turn = DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=(),
            education_level=None,
            interests=(),
            activities=(),
            unsure=False,
            correct_previous=False,
            learning_goals=tuple(sorted(goals)),
        )
        return await self._handle_discovery_turn(lead_id, turn, "")

    async def choose_guidance_language_support(
        self, lead_id: int, support_slug: str | None
    ) -> Reply:
        """Apply a listed language-support preference, or continue with it left open."""
        if support_slug is None:
            speaker = self._fact_value(lead_id, "active_speaker") or "student"
            if speaker != "student" and self._fact_value(
                lead_id, "language_support_preference_student"
            ):
                return Reply(
                    "I kept the learner's stated language-support preference. Please ask the "
                    "learner to choose whether to keep or widen it.",
                    (("Learner sharing now", "speaker:student"),),
                )
            _, _, _, _, previous_support = self._student_guidance_context(lead_id)
            interests, activities, level, goals, _ = self._student_guidance_context(lead_id)
            confirmed = self._fact_value(lead_id, "guidance_confirmed_signature")
            previous_signature = _guidance_signature(
                interests, activities, level, goals, previous_support
            )
            self.repository.delete_fact(lead_id, f"language_support_preference_{speaker}")
            self.repository.save_fact(
                lead_id,
                "guidance_language_prompted_signature",
                _guidance_signature(interests, activities, level, goals),
                "student",
            )
            if speaker == "student" and confirmed == previous_signature:
                self.repository.save_fact(
                    lead_id,
                    "guidance_confirmed_signature",
                    _guidance_signature(interests, activities, level, goals),
                    "student",
                )
            self.repository.update_lead(lead_id, discovery_step="guidance_confirmation")
            return self._present_guidance(lead_id)
        courses = self.repository.list_courses(self.tenant_id)
        interests, activities, level, goals, _ = self._student_guidance_context(lead_id)
        current_candidates = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            learning_goals=goals,
            level=None if level == "any" else level,
            limit=100,
        )
        supports = {
            support
            for match in current_candidates
            for support in match.course.language_support
            if _language_support_slug(support) == support_slug
        }
        if not supports:
            return Reply(
                "That support option is not listed in the sample catalog. Please choose again."
            )
        turn = DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=(),
            education_level=None,
            interests=(),
            activities=(),
            unsure=False,
            correct_previous=False,
            language_support_preference=next(iter(supports)),
        )
        return await self._handle_discovery_turn(lead_id, turn, "")

    async def choose_guidance_delivery_mode(self, lead_id: int, mode_slug: str | None) -> Reply:
        """Apply a delivery-format option shown for the current matching sample courses."""
        speaker = self._fact_value(lead_id, "active_speaker") or "student"
        if mode_slug is None:
            if speaker != "student" and self._fact_value(
                lead_id, "delivery_mode_preference_student"
            ):
                return Reply(
                    "I kept the learner's stated study-format preference. Please ask the learner "
                    "whether to keep it or leave format open.",
                    (("Learner sharing now", "speaker:student"),),
                )
            interests, activities, level, goals, language_support = self._student_guidance_context(
                lead_id
            )
            fact_key = f"delivery_mode_preference_{speaker}"
            previous_mode = self._fact_value(lead_id, fact_key)
            lead = self.repository.get_lead(lead_id)
            if previous_mode is None:
                base_signature = _guidance_signature(
                    interests, activities, level, goals, language_support
                )
                if (
                    lead is None
                    or lead["discovery_step"] != "guidance_delivery_mode"
                    or self._fact_value(lead_id, "guidance_delivery_mode_prompted_signature")
                    != base_signature
                ):
                    return self._present_guidance(lead_id)
            else:
                confirmed_signature = _guidance_signature(
                    interests, activities, level, goals, language_support, previous_mode
                )
                if (
                    lead is None
                    or lead["discovery_step"] != "results"
                    or self._fact_value(lead_id, "guidance_confirmed_signature")
                    != confirmed_signature
                ):
                    return self._present_guidance(lead_id)
            previous_signature = _guidance_signature(
                interests, activities, level, goals, language_support, previous_mode
            )
            base_signature = _guidance_signature(
                interests, activities, level, goals, language_support
            )
            confirmed = self._fact_value(lead_id, "guidance_confirmed_signature")
            self.repository.delete_fact(lead_id, fact_key)
            self.repository.save_fact(
                lead_id, "guidance_delivery_mode_prompted_signature", base_signature, "student"
            )
            if speaker == "student" and confirmed == previous_signature:
                self.repository.save_fact(
                    lead_id, "guidance_confirmed_signature", base_signature, "student"
                )
            self.repository.update_lead(lead_id, discovery_step="guidance_confirmation")
            return self._present_guidance(lead_id)

        lead = self.repository.get_lead(lead_id)
        if lead is None or lead["discovery_step"] != "guidance_delivery_mode":
            return self._present_guidance(lead_id)
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        expected_signature = _guidance_signature(
            interests, activities, level, goals, language_support
        )
        if (
            self._fact_value(lead_id, "guidance_delivery_mode_prompted_signature")
            != expected_signature
        ):
            return self._present_guidance(lead_id)
        courses = self.repository.list_courses(self.tenant_id)
        current_candidates = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            learning_goals=goals,
            language_support_preference=language_support,
            level=None if level == "any" else level,
            limit=100,
        )
        modes = {
            mode
            for match in current_candidates
            for mode in match.course.delivery_modes
            if _delivery_mode_slug(mode) == mode_slug
        }
        if not modes:
            return Reply("That format is not listed for these sample matches. Please choose again.")
        turn = DiscoveryTurn(
            intent="discovery",
            course_id=None,
            fields=(),
            education_level=None,
            interests=(),
            activities=(),
            unsure=False,
            correct_previous=False,
            delivery_mode_preference=next(iter(modes)),
        )
        return await self._handle_discovery_turn(lead_id, turn, "")

    async def confirm_guidance(self, lead_id: int, confirmation_token: str) -> Reply:
        """Accept only the currently pending summary, never a stale Telegram button."""
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        signature = _guidance_signature(
            interests,
            activities,
            level,
            goals,
            language_support,
            self._student_delivery_mode(lead_id),
        )
        pending = self._fact_value(lead_id, "guidance_pending_signature")
        if not pending:
            return Reply("That confirmation has expired. Your current course path is unchanged.")
        if (
            pending == signature
            and confirmation_token == _guidance_token(signature)
            and has_sufficient_guidance_context(
                interests=interests, activities=activities, level=level, learning_goals=goals
            )
        ):
            self.repository.save_fact(lead_id, "guidance_confirmed_signature", signature, "student")
            self.repository.delete_fact(lead_id, "guidance_pending_signature")
        return self._present_guidance(lead_id)

    async def revise_guidance(self, lead_id: int, confirmation_token: str) -> Reply:
        """Keep the learner's facts but ask what they want to correct or add."""
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        signature = _guidance_signature(
            interests,
            activities,
            level,
            goals,
            language_support,
            self._student_delivery_mode(lead_id),
        )
        pending = self._fact_value(lead_id, "guidance_pending_signature")
        if not pending:
            return Reply("That change prompt has expired. Your current course path is unchanged.")
        if pending != signature or confirmation_token != _guidance_token(signature):
            return self._present_guidance(lead_id)
        self.repository.delete_fact(lead_id, "guidance_pending_signature")
        self.repository.update_lead(lead_id, discovery_step="guidance_revision")
        return self._guidance_revision_prompt()

    @staticmethod
    def _guidance_revision_prompt() -> Reply:
        return Reply(
            "What should I change or add? You can correct an interest, activity, study goal, "
            "study level, or language-support preference, or mention another detail that matters.",
            (
                ("Choose a field", "path:field"),
                ("Browse sample courses", "path:browse"),
                ("Choose a known course", "path:course"),
            ),
        )

    def _fact_value(self, lead_id: int, key: str) -> str | None:
        fact = next(
            (item for item in self.repository.list_facts(lead_id) if item["fact_key"] == key),
            None,
        )
        return str(fact["fact_value"]) if fact else None

    def _retract_discovery_preferences(
        self,
        lead_id: int,
        speaker: str,
        retracted: tuple[RetractedPreference, ...],
        courses: list[Course],
    ) -> None:
        """Remove only exact, stored, catalog-valid preferences withdrawn this turn."""
        allowed_values: dict[str, set[str]] = {
            "field": {course.field for course in courses},
            "education_level": {
                "vocational_certificate",
                "diploma",
                "undergraduate",
                "postgraduate",
                "any",
            },
            "interest": {item for course in courses for item in course.interests},
            "activity": {item for course in courses for item in course.activities},
            "learning_goal": {item for course in courses for item in course.learning_goals},
            "language_support": {item for course in courses for item in course.language_support},
            "delivery_mode": {item for course in courses for item in course.delivery_modes},
        }
        pipe_facts = {
            "field": f"interest_fields_{speaker}",
            "interest": f"interest_terms_{speaker}",
            "activity": f"activity_terms_{speaker}",
            "learning_goal": f"learning_goals_{speaker}",
        }
        singleton_facts = {
            "education_level": f"education_level_{speaker}",
            "language_support": f"language_support_preference_{speaker}",
            "delivery_mode": f"delivery_mode_preference_{speaker}",
        }
        for preference in retracted:
            category = preference.category
            value = preference.value
            if category not in allowed_values or value not in allowed_values[category]:
                continue
            facts = {
                str(item["fact_key"]): str(item["fact_value"])
                for item in self.repository.list_facts(lead_id)
            }
            if category in pipe_facts:
                fact_key = pipe_facts[category]
                stored = facts.get(fact_key, "")
                if category == "field" and not stored:
                    stored = facts.get(f"interest_field_{speaker}", "")
                values = [item for item in stored.split("|") if item]
                if value not in values:
                    continue
                remaining = [item for item in values if item != value]
                if remaining:
                    self.repository.save_fact(lead_id, fact_key, "|".join(remaining), speaker)
                else:
                    self.repository.delete_fact(lead_id, fact_key)
                if category == "field":
                    if len(remaining) == 1:
                        self.repository.save_fact(
                            lead_id, f"interest_field_{speaker}", remaining[0], speaker
                        )
                    else:
                        self.repository.delete_fact(lead_id, f"interest_field_{speaker}")
                elif category == "activity" and facts.get(f"interest_activity_{speaker}") == value:
                    self.repository.delete_fact(lead_id, f"interest_activity_{speaker}")
            elif category in singleton_facts:
                fact_key = singleton_facts[category]
                if facts.get(fact_key) == value:
                    self.repository.delete_fact(lead_id, fact_key)
                    if category == "education_level" and speaker == "student":
                        self.repository.update_lead(lead_id, education_level=None)

    def _student_guidance_context(
        self, lead_id: int
    ) -> tuple[set[str], set[str], str | None, set[str], str | None]:
        facts = {
            str(item["fact_key"]): str(item["fact_value"])
            for item in self.repository.list_facts(lead_id)
        }
        interests = set(facts.get("interest_terms_student", "").split("|"))
        interests.update(facts.get("interest_fields_student", "").split("|"))
        if facts.get("interest_field_student"):
            interests.add(facts["interest_field_student"])
        activities = set(facts.get("activity_terms_student", "").split("|"))
        if facts.get("interest_activity_student"):
            activities.add(facts["interest_activity_student"])
        activities.discard("")
        interests.discard("")
        goals = set(facts.get("learning_goals_student", "").split("|"))
        goals.discard("")
        level = facts.get("education_level_student") or None
        language_support = facts.get("language_support_preference_student") or None
        return interests, activities, level, goals, language_support

    def _student_delivery_mode(self, lead_id: int) -> str | None:
        return self._fact_value(lead_id, "delivery_mode_preference_student") or None

    def _guidance_reflection(
        self,
        lead_id: int,
        interests: set[str],
        activities: set[str],
        level: str | None,
        goals: set[str],
        language_support: str | None,
        signature: str,
        delivery_mode: str | None = None,
    ) -> Reply:
        self.repository.save_fact(lead_id, "guidance_pending_signature", signature, "student")
        self.repository.update_lead(
            lead_id, discovery_step="guidance_confirmation", lifecycle_stage="discovering"
        )
        details = [f"you are interested in {', '.join(sorted(interests))}"]
        if activities:
            details.append(f"you enjoy {', '.join(sorted(activities))}")
        if goals:
            details.append(f"you hope to {', '.join(sorted(goals))}")
        if level == "any":
            details.append("you are open to all listed study levels")
        elif level:
            details.append(f"you are considering the {level.replace('_', ' ')} level")
        else:
            details.append("your study level is still open")
        if language_support:
            details.append(f"you prefer courses listing {language_support}")
        if delivery_mode:
            details.append(f"you prefer courses listing {delivery_mode.replace('_', ' ')} study")
        token = _guidance_token(signature)
        return Reply(
            f"Before I show options, I heard that {'; '.join(details)}. Did I get that right?",
            (
                ("Yes, show matching courses", f"guidance:confirm:{token}"),
                ("I'd like to change or add something", f"guidance:revise:{token}"),
            ),
        )

    def _clear_guidance_confirmation(self, lead_id: int) -> None:
        self.repository.delete_fact(lead_id, "guidance_pending_signature")
        self.repository.delete_fact(lead_id, "guidance_confirmed_signature")

    def _discovery_prompt(self, language: str = "en") -> Reply:
        copy = {
            "en": "This is fictional demo guidance, not an admissions decision. Typed messages "
            "and a few recent chat messages are sent to OpenAI to guide the conversation; "
            "messages are stored locally. Use "
            "demo text only, not real student or personal data. What are you "
            "thinking about studying, or what do you enjoy doing? You can type a course or "
            "interest in your own words, say you're not sure, or choose a shortcut. Most other "
            "demo replies remain in English; translated copy needs fluent-speaker review. Please "
            "use demo text only. You can turn OpenAI processing off at any time.",
            "hi": "यह काल्पनिक डेमो मार्गदर्शन है, प्रवेश निर्णय नहीं। आपके लिखे संदेश नमूना कोर्स "
            "मिलाने के लिए OpenAI को भेजे जाते हैं और स्थानीय रूप से सहेजे जाते हैं। Recent chat "
            "context may also be included. केवल डेमो "
            "जानकारी लिखें, असली छात्र या निजी जानकारी नहीं। आप क्या पढ़ने के बारे में सोच "
            "रहे हैं, या आपको क्या करना पसंद है? आप अपने शब्दों "
            "में कोर्स या रुचि लिख सकते हैं, कह सकते हैं कि अभी तय नहीं है, या नीचे विकल्प चुन सकते "
            "हैं। डेमो के ज़्यादातर जवाब अभी अंग्रेज़ी में हैं; अनुवाद की समीक्षा बाकी है। आप "
            "केवल डेमो जानकारी लिखें। OpenAI प्रोसेसिंग कभी भी बंद कर सकते हैं।",
            "ml": "ഇത് സാങ്കൽപ്പിക ഡെമോ മാർഗനിർദ്ദേശമാണ്, പ്രവേശന തീരുമാനം അല്ല. മാതൃകാ കോഴ്സുകൾ "
            "കണ്ടെത്താൻ നിങ്ങൾ ടൈപ്പ് ചെയ്യുന്ന സന്ദേശങ്ങൾ OpenAI-ലേക്ക് അയയ്ക്കുകയും പ്രാദേശികമായി "
            "സൂക്ഷിക്കുകയും ചെയ്യും. Recent chat context may also be included. ഡെമോ വിവരങ്ങൾ മാത്രം "
            "നൽകുക; യഥാർത്ഥ വ്യക്തിഗത വിവരങ്ങൾ "
            "നൽകരുത്. നിങ്ങൾ എന്താണ് "
            "പഠിക്കാൻ ആലോചിക്കുന്നത്, അല്ലെങ്കിൽ എന്ത് ചെയ്യാനാണ് ഇഷ്ടം? "
            "കോഴ്സോ താൽപര്യമോ നിങ്ങളുടെ വാക്കുകളിൽ ടൈപ്പ് ചെയ്യാം, ഉറപ്പില്ലെന്ന് പറയാം, അല്ലെങ്കിൽ "
            "താഴെയുള്ളൊരു വഴി തിരഞ്ഞെടുക്കാം. ഡെമോയുടെ മിക്ക മറുപടികളും ഇപ്പോൾ ഇംഗ്ലീഷിലാണ്; "
            "വിവർത്തനത്തിന് വിദഗ്ധ പരിശോധന വേണം. OpenAI പ്രോസസ്സിംഗ് എപ്പോൾ വേണമെങ്കിലും ഓഫ് "
            "ചെയ്യാം. ഡെമോ ടെക്സ്റ്റ് മാത്രം ഉപയോഗിക്കുക.",
            "hinglish": "Yeh fictional demo guidance hai, admission decision nahi. Sample courses "
            "match karne ke liye typed messages OpenAI ko bheje aur locally save kiye jaate hain. "
            "Recent chat context may also be included. "
            "Sirf demo text use karein; real student ya personal details nahi. Aap kya study "
            "karne ka soch rahe hain, ya aapko kya karna pasand hai? "
            "Course ya interest apne words mein likhein, unsure bol sakte hain, ya neeche shortcut "
            "chunein. Demo ke most replies abhi English mein hain; translation ko fluent speaker "
            "review karega. Sirf demo text use karein. OpenAI processing kabhi bhi off kar "
            "sakte hain.",
        }
        return Reply(
            copy.get(language, copy["en"]),
            (
                ("I know a course", "path:course"),
                ("I know the field", "path:field"),
                ("Help me explore", "path:explore"),
                ("Just browsing / ask a question", "path:browse"),
                ("I'm a parent/guardian", "speaker:parent"),
            ),
        )

    def _tap_only_prompt(self, language: str = "en") -> Reply:
        copy = {
            "en": (
                "OpenAI processing is off for this chat. I won't send typed messages to OpenAI. "
                "You can still explore or browse using the buttons below; avoid typing personal "
                "details because messages are stored locally.",
                "Explore by field",
                "Explore with choices",
                "Browse sample courses",
                "Choose a known course",
                "Turn on OpenAI processing",
            ),
            "hi": (
                "इस चैट में OpenAI प्रोसेसिंग बंद है। आपके लिखे संदेश OpenAI को नहीं भेजे जाएंगे। "
                "नीचे के बटनों से कोर्स देखें। निजी जानकारी न लिखें; संदेश स्थानीय रूप से सहेजे जाते "
                "हैं।",
                "विषय चुनें",
                "विकल्पों से खोजें",
                "नमूना कोर्स देखें",
                "कोर्स चुनें",
                "OpenAI प्रोसेसिंग चालू करें",
            ),
            "ml": (
                "ഈ ചാറ്റിൽ OpenAI പ്രോസസ്സിംഗ് ഓഫ് ആണ്. നിങ്ങൾ ടൈപ്പ് ചെയ്യുന്ന സന്ദേശങ്ങൾ OpenAI-ലേക്ക് "
                "അയയ്ക്കില്ല. താഴെയുള്ള ബട്ടണുകൾ ഉപയോഗിച്ച് കോഴ്സുകൾ കാണാം. സ്വകാര്യ വിവരങ്ങൾ "
                "നൽകരുത്; സന്ദേശങ്ങൾ പ്രാദേശികമായി സൂക്ഷിക്കും.",
                "മേഖല തിരഞ്ഞെടുക്കുക",
                "ഓപ്ഷനുകളിലൂടെ കണ്ടെത്തുക",
                "മാതൃകാ കോഴ്സുകൾ കാണുക",
                "കോഴ്സ് തിരഞ്ഞെടുക്കുക",
                "OpenAI പ്രോസസ്സിംഗ് ഓൺ ചെയ്യുക",
            ),
            "hinglish": (
                "Is chat mein OpenAI processing band hai. Aapke typed messages OpenAI ko nahi "
                "bheje jayenge. Neeche buttons se courses explore karein. Personal details mat "
                "bhejein; messages local database mein save hote hain.",
                "Field se explore karein",
                "Choices se explore karein",
                "Sample courses dekhein",
                "Course choose karein",
                "OpenAI processing chalu karein",
            ),
        }
        text, field, explore, browse, course, enable = copy.get(language, copy["en"])
        return Reply(
            text,
            (
                (field, "path:field"),
                (explore, "path:explore"),
                (browse, "path:browse"),
                (course, "path:course"),
                (enable, "ai:processing:on"),
            ),
        )

    def begin_path(self, lead_id: int, path: str) -> Reply:
        self._clear_guidance_confirmation(lead_id)
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
            return self._field_choices(lead_id, _FIELD_CHOICES_PROMPT, "field")
        if path == "explore":
            return self._field_choices(lead_id, _EXPLORE_CHOICES_PROMPT, "explore")
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

    def _field_choices(self, lead_id: int, prompt: str, step: str = "field") -> Reply:
        self.repository.update_lead(lead_id, discovery_step=step)
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

    def _unsure_exploration_reply(self, lead_id: int) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        activity_by_field: dict[str, str] = {}
        for course in courses:
            if course.field and course.activities:
                activity_by_field.setdefault(course.field, course.activities[0])
        activity_buttons = tuple(
            (
                f"{field.replace('/', ' & ').title()}: {_activity_label(activity)}",
                f"guidance:activity:{_activity_slug(activity)}",
            )
            for field, activity in sorted(activity_by_field.items())
        )
        fields = sorted({course.field for course in courses if course.field})
        field_buttons = tuple(
            (field.replace("/", " & ").replace("-", " ").title(), f"field:{field}")
            for field in fields
        )
        self.repository.update_lead(lead_id, discovery_step="guidance_unsure")
        return Reply(
            "No need to know a course name yet. What do you enjoy doing or learning about in "
            "class or outside school? Pick an example or tell me in your own words.",
            activity_buttons
            + field_buttons
            + (("Browse sample courses", "path:browse"), ("Pause for now", "discovery:pause")),
        )

    def _uncertainty_recovery_reply(self, lead_id: int) -> Reply:
        self.repository.update_lead(lead_id, discovery_step="guidance_unsure_support")
        return Reply(
            "You don't need to decide now. You can browse examples without choosing, pick a field "
            "to explore, or pause for now. No course will be suggested "
            "until you share something to guide it.",
            (
                ("Browse sample courses", "path:browse"),
                ("Choose a field to explore", "path:field"),
                ("Pause for now", "discovery:pause"),
            ),
        )

    def recommend_field(self, lead_id: int, field: str) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        selected = next((course.field for course in courses if course.field == field), None)
        if selected is None:
            return Reply(
                "That field isn't part of this fictional catalog, so I can't recommend a course "
                "in it. I can show the fields that are offered or help you find the closest "
                "sample option.",
                (
                    ("Choose an offered field", "path:explore"),
                    ("Browse sample courses", "path:browse"),
                ),
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
        existing_field = self._fact_value(lead_id, f"interest_field_{speaker}")
        if existing_field != selected and speaker == "student":
            self._clear_guidance_confirmation(lead_id)
        self.repository.delete_fact(lead_id, f"guidance_unsure_count_{speaker}")
        self.repository.save_fact(lead_id, f"interest_fields_{speaker}", selected, speaker)
        self.repository.save_fact(lead_id, f"interest_field_{speaker}", selected, speaker)
        if speaker == "parent":
            return Reply(
                "I've recorded that as the parent's preference. To keep the student's goals first, "
                "please ask the learner to choose or confirm their own field before I "
                "recommend courses.",
                (("Learner sharing now", "speaker:student"),),
            )
        self.repository.update_lead(lead_id, discovery_step="guidance_signal")
        return self._present_guidance(lead_id)

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
        active = next(
            (
                fact["fact_value"]
                for fact in self.repository.list_facts(lead_id)
                if fact["fact_key"] == "active_speaker"
            ),
            "student",
        )
        speaker = str(active)
        selected_level = None if level == "any" else level
        if speaker == "student":
            self.repository.delete_fact(lead_id, f"guidance_unsure_count_{speaker}")
            lead = self.repository.get_lead(lead_id)
            current_level = (
                str(lead["education_level"]) if lead and lead["education_level"] else None
            )
            if current_level != selected_level:
                self._clear_guidance_confirmation(lead_id)
            self.repository.update_lead(
                lead_id, education_level=selected_level, discovery_step="guidance_signal"
            )
        self.repository.save_fact(lead_id, f"education_level_{speaker}", level, speaker)
        if speaker == "parent":
            return Reply(
                "I've recorded that as the parent's preferred study level. The learner's own "
                "preference should guide course recommendations; ask them to share or confirm it.",
                (("Learner sharing now", "speaker:student"),),
            )
        return self._present_guidance(lead_id)

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
        if activity:
            self.repository.save_fact(lead_id, "interest_activity_student", activity, "student")
        self.repository.update_lead(lead_id, discovery_step="results")
        return self._present_guidance(lead_id)

    def show_guidance_matches(self, lead_id: int) -> Reply:
        """Return the current confirmed comparison set, refreshing it if it became stale."""
        lead = self.repository.get_lead(lead_id)
        if lead is None:
            return Reply("Send /start to begin a new demo conversation.")
        if lead["discovery_step"] != "results" or not self._guidance_is_currently_confirmed(
            lead_id
        ):
            self.repository.delete_fact(lead_id, "guidance_confirmed_signature")
            return self._present_guidance(lead_id)
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        return self._guidance_recommendation_reply(
            lead_id,
            self.repository.list_courses(self.tenant_id),
            interests,
            activities,
            level,
            goals,
            language_support,
            self._student_delivery_mode(lead_id),
        )

    def explore_guidance_course(self, lead_id: int, course_id: str) -> Reply:
        """Show verified sample details without treating interest as course selection."""
        lead = self.repository.get_lead(lead_id)
        if lead is None:
            return Reply("Send /start to begin a new demo conversation.")
        matches = self._current_guidance_matches(lead_id)
        is_current = lead["discovery_step"] == "results" and self._guidance_is_currently_confirmed(
            lead_id
        )
        match = next(
            (item for item in matches if item.course.id == course_id),
            None,
        )
        if not is_current or match is None:
            self.repository.delete_fact(lead_id, "guidance_confirmed_signature")
            return self._present_guidance(lead_id)

        course = match.course
        study_formats = (
            ", ".join(mode.replace("_", " ") for mode in course.delivery_modes) or "not specified"
        )
        details = (
            f"Fictional sample details — {course.name}\n"
            f"Level: {course.education_level.replace('_', ' ')}\n"
            f"Field: {course.field}\n"
            f"About: {course.description}\n"
            f"Why it matched: {'; '.join(match.reasons)}\n"
            f"Sample prerequisites: {'; '.join(course.prerequisites)}\n"
            f"Teaching medium: {course.medium}\n"
            f"Listed language support: {', '.join(course.language_support) or 'not specified'}\n"
            f"Listed study formats: {study_formats}\n"
            f"Sample application fee: {format_inr_from_paise(course.application_fee_paise)}\n\n"
            "This is fictional sample catalog data, not an admission decision or a promise of "
            "availability. You can compare the other matches before choosing whether to continue."
        )
        action_label = (
            "Check sample eligibility"
            if course.education_level == "undergraduate" and course.minimum_marks_percent > 0
            else "Explore this sample course"
        )
        return Reply(
            details,
            (
                (action_label, f"guidance:continue:{course.id}"),
                ("Back to matching courses", "guidance:matches"),
            ),
        )

    def continue_guidance_course(self, lead_id: int, course_id: str) -> Reply:
        """Continue only a current match into supported qualification or sample exploration."""
        lead = self.repository.get_lead(lead_id)
        if lead is None:
            return Reply("Send /start to begin a new demo conversation.")
        if lead["discovery_step"] != "results":
            return Reply(
                "That course comparison has expired. Your current course path is unchanged."
            )
        matches = self._current_guidance_matches(lead_id)
        if not self._guidance_is_currently_confirmed(lead_id) or course_id not in {
            item.course.id for item in matches
        }:
            self.repository.delete_fact(lead_id, "guidance_confirmed_signature")
            return self._present_guidance(lead_id)
        return self.select_course(lead_id, course_id)

    def _current_guidance_matches(self, lead_id: int) -> list[CourseMatch]:
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        return recommend_courses(
            self.repository.list_courses(self.tenant_id),
            interests=interests,
            activities=activities,
            learning_goals=goals,
            language_support_preference=language_support,
            delivery_mode_preference=self._student_delivery_mode(lead_id),
            level=None if level == "any" else level,
            limit=3,
        )

    def _guidance_is_currently_confirmed(self, lead_id: int) -> bool:
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        signature = _guidance_signature(
            interests,
            activities,
            level,
            goals,
            language_support,
            self._student_delivery_mode(lead_id),
        )
        return self._fact_value(lead_id, "guidance_confirmed_signature") == signature

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
        if step == "field":
            return self._field_choices(lead_id, _FIELD_CHOICES_PROMPT, "field")
        if step == "explore":
            return self._field_choices(lead_id, _EXPLORE_CHOICES_PROMPT, "explore")
        if step == "level":
            return self._level_choices(lead_id)
        if step == "activity":
            return self._activity_choices(lead_id)
        if step == "guidance_signal":
            return self._present_guidance(lead_id)
        if step == "guidance_unsure":
            return self._unsure_exploration_reply(lead_id)
        if step == "guidance_unsure_support":
            return self._uncertainty_recovery_reply(lead_id)
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
        if step == "guidance_confirmation":
            context = self._student_guidance_context(lead_id)
            if not has_sufficient_guidance_context(
                interests=context[0],
                activities=context[1],
                level=context[2],
                learning_goals=context[3],
            ):
                self.repository.delete_fact(lead_id, "guidance_pending_signature")
                self.repository.update_lead(lead_id, discovery_step="explore")
                return self._field_choices(lead_id, _EXPLORE_CHOICES_PROMPT, "explore")
            delivery_mode = self._student_delivery_mode(lead_id)
            signature = _guidance_signature(*context, delivery_mode)
            return self._guidance_reflection(lead_id, *context, signature, delivery_mode)
        if step == "guidance_goal":
            return self._guidance_goal_prompt(lead_id)
        if step == "guidance_language_support":
            return self._guidance_language_support_prompt(lead_id)
        if step == "guidance_delivery_mode":
            return self._guidance_delivery_mode_prompt(lead_id)
        if step == "guidance_revision":
            return self._guidance_revision_prompt()
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
        processing = self.ai_processing_enabled(lead_id)
        if not processing:
            return self._tap_only_prompt(language)
        return self._discovery_prompt(language)

    def language_menu(self, lead_id: int | None = None) -> Reply:
        language = self.preferred_language(lead_id) if lead_id is not None else "en"
        messages = {
            "en": "Choose a demo language. Most replies are currently English; other copy "
            "needs fluent-speaker review.",
            "hi": "डेमो की भाषा चुनें। ज़्यादातर जवाब अभी अंग्रेज़ी में हैं; बाकी अनुवाद की समीक्षा बाकी है।",
            "ml": "ഡെമോ ഭാഷ തിരഞ്ഞെടുക്കുക. മിക്ക മറുപടികളും ഇപ്പോൾ ഇംഗ്ലീഷിലാണ്; മറ്റ് വിവർത്തനങ്ങൾ പരിശോധിക്കണം.",
            "hinglish": "Demo language chunein. Most replies abhi English mein hain; baaki copy "
            "ko fluent speaker review karega.",
        }
        return Reply(
            messages.get(language, messages["en"]),
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
            "I've added a staff handoff to the demo dashboard. Live contact and response-time "
            "details are not configured."
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
        self._clear_guidance_confirmation(lead_id)
        self.repository.save_fact(lead_id, "course_choice_student", course.id, "student")
        if course.education_level != "undergraduate" or course.minimum_marks_percent <= 0:
            eligibility_limit_explained = any(
                fact["fact_key"] == "eligibility_limit_explained" for fact in facts
            )
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
            if not eligibility_limit_explained:
                self.repository.save_fact(lead_id, "eligibility_limit_explained", "true")
            limitation = (
                "\n\nI can show these sample facts, but this demo has no eligibility rules "
                "configured for this study level, so I can't confirm eligibility or admission. "
                "Would you like to keep exploring or compare other courses?"
                if not eligibility_limit_explained
                else "\n\nWould you like to explore another course or browse the sample catalog?"
            )
            return Reply(
                f"{course.name} is a fictional {course.education_level.replace('_', ' ')} sample. "
                f"Sample prerequisites: {'; '.join(course.prerequisites)}. "
                f"Sample medium: {course.medium}. Sample language support: "
                f"{', '.join(course.language_support) or 'not specified'}.{limitation}",
                (
                    ("Explore another course", "path:explore"),
                    ("Browse sample courses", "path:browse"),
                ),
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
        if _is_ai_opt_out(text):
            return self.set_ai_processing_enabled(lead_id, False)
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
                return Reply(
                    "The sample data only confirms application fees. Tuition and "
                    "hostel/accommodation charges aren't listed, so I won't guess or treat them "
                    "as included. I can show the confirmed application fee or browse course "
                    "details.",
                    (("Browse sample courses", "path:browse"),),
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
                return Reply(
                    "Language requirements depend on the course. I can help you weigh the "
                    "trade-offs, but the sample catalog only lists teaching medium and discussion "
                    "support; it doesn't set proficiency rules. Choose a course to see those "
                    "listed sample facts.",
                    (("Browse sample courses", "path:browse"),),
                )
            support = ", ".join(course.language_support) or "not specified in the sample catalog"
            return Reply(
                f"For this fictional sample, the listed medium for {course.name} is "
                f"{course.medium}, and listed discussion support is {support}. The sample catalog "
                "does not specify a required proficiency level or guarantee an accommodation. "
                "I can help compare the listed options, but I won't infer those requirements."
            )
        if _is_accommodation_question(text):
            return Reply(
                "The fictional sample mentions a hostel, but actual availability, eligibility, "
                "pricing, and terms aren't confirmed, so I won't guess. I can still help compare "
                "sample courses or answer questions covered by the demo information.",
                (("Browse sample courses", "path:browse"),),
            )
        if self._fact_value(lead_id, "guidance_pending_signature") and _is_guidance_confirmation(
            text
        ):
            pending = self._fact_value(lead_id, "guidance_pending_signature")
            return await self.confirm_guidance(lead_id, _guidance_token(pending or ""))
        if not self.ai_processing_enabled(lead_id):
            return self._tap_only_prompt()
        if self.discovery_interpreter is not None:
            try:
                turn = await self.discovery_interpreter.extract_discovery(
                    text,
                    self.repository.list_courses(self.tenant_id),
                    self._ai_conversation_context(lead_id, text),
                )
            except Exception:
                return Reply(
                    "I couldn't understand that safely just now. You can continue with the "
                    "buttons, browse sample courses, or try a shorter message.",
                    (("Choose a path", "menu:start"), ("Browse courses", "path:browse")),
                )
            return await self._handle_discovery_turn(lead_id, turn, text)
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
                    "I couldn't find a reliable answer in the fictional demo information, so I "
                    "won't guess. Try rephrasing, ask about a listed course, or browse the sample "
                    "catalog.",
                    (("Browse sample courses", "path:browse"),),
                )
            answer, source = result
            return Reply(f"{answer}\n\nSource: {source}")
        if route == "human_request":
            if _is_explicit_staff_request(text):
                return self.handoff(lead_id, "Student requested a staff member.")
            route = "conversation"
        if route == "course_browse":
            return self.browse(lead_id)
        return Reply(
            "I can help with the sample courses, eligibility, or FAQs. Send /start to see options."
        )

    async def _handle_discovery_turn(self, lead_id: int, turn: DiscoveryTurn, text: str) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        speaker_fact = next(
            (f for f in self.repository.list_facts(lead_id) if f["fact_key"] == "active_speaker"),
            None,
        )
        speaker = str(speaker_fact["fact_value"]) if speaker_fact else "student"
        if turn.intent == "staff_request":
            if _is_explicit_staff_request(text):
                return self.handoff(lead_id, "Student requested a staff member.")
            turn = replace(turn, intent="conversation")
        elif _is_assistant_identity_question(text) or _is_simple_greeting(text):
            turn = replace(turn, intent="conversation")
        if turn.intent == "out_of_scope":
            return self._noninformative_turn_reply(lead_id, turn.intent, turn.assistant_message)
        if turn.intent == "knowledge_question":
            result = await self.retrieval.answer(self.tenant_id, text)
            if result is None:
                return Reply(
                    "I couldn't find a reliable answer in the fictional demo information, so I "
                    "won't guess. Try rephrasing, ask about a listed course, or browse the sample "
                    "catalog.",
                    (("Browse sample courses", "path:browse"),),
                )
            answer, source = result
            return Reply(f"{answer}\n\nSource: {source}")
        if turn.intent == "course_lookup" and turn.course_id:
            if speaker == "parent":
                self.repository.save_fact(lead_id, "course_choice_parent", turn.course_id, "parent")
                return Reply(
                    "I've recorded this as the parent's course suggestion. Please ask the learner "
                    "to confirm it.",
                    (("Learner wants to explore this", f"course:confirm:{turn.course_id}"),),
                )
            return self.select_course(lead_id, turn.course_id)
        if turn.intent == "course_lookup" and not turn.course_id:
            return Reply(
                "I couldn't match that wording to an exact course in the fictional catalog. "
                "Try its full name, choose a field, or browse.",
                (("Choose a course", "path:course"), ("Browse courses", "path:browse")),
            )
        if not _has_discovery_signal(turn):
            return self._noninformative_turn_reply(lead_id, turn.intent, turn.assistant_message)

        if turn.correct_previous:
            self._retract_discovery_preferences(
                lead_id, speaker, turn.retracted_preferences, courses
            )
        if (
            turn.fields
            or turn.education_level
            or turn.interests
            or turn.activities
            or turn.learning_goals
            or turn.language_support_preference
            or turn.delivery_mode_preference
            or turn.retracted_preferences
        ):
            self.repository.delete_fact(lead_id, f"guidance_unsure_count_{speaker}")
        if speaker == "student" and (
            turn.correct_previous
            or turn.fields
            or turn.education_level
            or turn.interests
            or turn.activities
            or turn.learning_goals
            or turn.language_support_preference
            or turn.delivery_mode_preference
            or turn.retracted_preferences
        ):
            self.repository.delete_fact(lead_id, "guidance_confirmed_signature")
        has_new_or_retracted_preference = bool(
            turn.fields
            or turn.education_level
            or turn.interests
            or turn.activities
            or turn.learning_goals
            or turn.language_support_preference
            or turn.delivery_mode_preference
            or turn.retracted_preferences
        )
        speaker_suffix = f"_{speaker}"
        has_saved_preferences = any(
            str(fact["fact_key"]).endswith(speaker_suffix)
            and str(fact["fact_key"]).startswith(
                (
                    "interest_field_",
                    "interest_fields_",
                    "education_level_",
                    "interest_terms_",
                    "activity_terms_",
                    "interest_activity_",
                    "learning_goals_",
                    "language_support_preference_",
                    "delivery_mode_preference_",
                )
            )
            for fact in self.repository.list_facts(lead_id)
        )
        if turn.correct_previous and has_saved_preferences and not has_new_or_retracted_preference:
            if speaker == "student":
                self._clear_guidance_confirmation(lead_id)
                self.repository.update_lead(
                    lead_id, discovery_step="guidance_revision", lifecycle_stage="discovering"
                )
            return self._with_ai_conversation_copy(
                self._guidance_revision_prompt(), turn.assistant_message
            )
        if turn.fields:
            fields_key = f"interest_fields_{speaker}"
            existing_fields = (
                ""
                if turn.correct_previous
                else next(
                    (
                        f["fact_value"]
                        for f in self.repository.list_facts(lead_id)
                        if f["fact_key"] == fields_key
                    ),
                    "",
                )
            )
            merged_fields = dict.fromkeys(
                [*(item for item in existing_fields.split("|") if item), *turn.fields]
            )
            self.repository.save_fact(lead_id, fields_key, "|".join(merged_fields), speaker)
            if len(merged_fields) == 1:
                self.repository.save_fact(
                    lead_id, f"interest_field_{speaker}", next(iter(merged_fields)), speaker
                )
            else:
                self.repository.delete_fact(lead_id, f"interest_field_{speaker}")
        if turn.education_level and turn.education_level != "any":
            self.repository.save_fact(
                lead_id, f"education_level_{speaker}", turn.education_level, speaker
            )
            if speaker == "student":
                self.repository.update_lead(lead_id, education_level=turn.education_level)
        elif turn.education_level == "any" and turn.correct_previous:
            self.repository.delete_fact(lead_id, f"education_level_{speaker}")
            if speaker == "student":
                self.repository.update_lead(lead_id, education_level=None)
        if turn.interests:
            interests_key = f"interest_terms_{speaker}"
            existing_interests = (
                ""
                if turn.correct_previous
                else next(
                    (
                        f["fact_value"]
                        for f in self.repository.list_facts(lead_id)
                        if f["fact_key"] == interests_key
                    ),
                    "",
                )
            )
            self.repository.save_fact(
                lead_id,
                interests_key,
                "|".join(
                    dict.fromkeys(
                        [*(item for item in existing_interests.split("|") if item), *turn.interests]
                    )
                ),
                speaker,
            )
        if turn.activities:
            activities_key = f"activity_terms_{speaker}"
            existing_activities = (
                ""
                if turn.correct_previous
                else next(
                    (
                        f["fact_value"]
                        for f in self.repository.list_facts(lead_id)
                        if f["fact_key"] == activities_key
                    ),
                    "",
                )
            )
            self.repository.save_fact(
                lead_id,
                activities_key,
                "|".join(
                    dict.fromkeys(
                        [
                            *(item for item in existing_activities.split("|") if item),
                            *turn.activities,
                        ]
                    )
                ),
                speaker,
            )
        if turn.learning_goals:
            goals_key = f"learning_goals_{speaker}"
            existing_goals = (
                ""
                if turn.correct_previous
                else next(
                    (
                        f["fact_value"]
                        for f in self.repository.list_facts(lead_id)
                        if f["fact_key"] == goals_key
                    ),
                    "",
                )
            )
            allowed_goals = {goal for course in courses for goal in course.learning_goals}
            merged_goals = dict.fromkeys(
                [
                    *(item for item in existing_goals.split("|") if item),
                    *(item for item in turn.learning_goals if item in allowed_goals),
                ]
            )
            if merged_goals:
                self.repository.save_fact(lead_id, goals_key, "|".join(merged_goals), speaker)
        if turn.language_support_preference:
            allowed_supports = {
                support for course in courses for support in course.language_support
            }
            if turn.language_support_preference in allowed_supports:
                self.repository.save_fact(
                    lead_id,
                    f"language_support_preference_{speaker}",
                    turn.language_support_preference,
                    speaker,
                )
        if turn.delivery_mode_preference:
            allowed_modes = {mode for course in courses for mode in course.delivery_modes}
            if turn.delivery_mode_preference in allowed_modes:
                self.repository.save_fact(
                    lead_id,
                    f"delivery_mode_preference_{speaker}",
                    turn.delivery_mode_preference,
                    speaker,
                )
        if speaker == "parent" and (
            turn.fields
            or turn.interests
            or turn.activities
            or turn.education_level
            or turn.learning_goals
            or turn.language_support_preference
            or turn.delivery_mode_preference
            or turn.retracted_preferences
        ):
            return self._with_ai_conversation_copy(
                Reply(
                    "I've recorded those as the parent's preferences. The learner's own interests "
                    "should guide recommendations; invite them to share or confirm their "
                    "preferences.",
                    (("Learner sharing now", "speaker:student"),),
                ),
                turn.assistant_message,
            )
        current_interests, current_activities, _, current_goals, _ = self._student_guidance_context(
            lead_id
        )
        if turn.unsure and not (
            turn.fields
            or turn.interests
            or turn.activities
            or turn.learning_goals
            or current_interests
            or current_activities
            or current_goals
        ):
            if speaker == "parent":
                return self._with_ai_conversation_copy(
                    Reply(
                        "It's okay if the learner is unsure. Invite them to share what they enjoy "
                        "or have tried; their own interests should guide the suggestions.",
                        (
                            ("Learner sharing now", "speaker:student"),
                            ("Browse sample courses", "path:browse"),
                        ),
                    ),
                    turn.assistant_message,
                )
            count_fact = f"guidance_unsure_count_{speaker}"
            try:
                previous_count = int(self._fact_value(lead_id, count_fact) or "0")
            except ValueError:
                previous_count = 0
            count = min(previous_count + 1, 2)
            self.repository.save_fact(lead_id, count_fact, str(count), speaker)
            if count == 1:
                reply = self._unsure_exploration_reply(lead_id)
            else:
                reply = self._uncertainty_recovery_reply(lead_id)
            return self._with_ai_conversation_copy(reply, turn.assistant_message)
        lead = self.repository.get_lead(lead_id)
        if (
            lead
            and lead["discovery_step"] == "guidance_revision"
            and not (
                turn.correct_previous
                or turn.fields
                or turn.education_level
                or turn.interests
                or turn.activities
                or turn.learning_goals
                or turn.language_support_preference
                or turn.delivery_mode_preference
            )
        ):
            return self._with_ai_conversation_copy(
                self._guidance_revision_prompt(), turn.assistant_message
            )
        reply = self._present_guidance(lead_id)
        current_lead = self.repository.get_lead(lead_id)
        if current_lead and current_lead["discovery_step"] != "results":
            return self._with_ai_conversation_copy(reply, turn.assistant_message)
        return reply

    def _noninformative_turn_reply(
        self, lead_id: int, intent: str, assistant_message: str | None = None
    ) -> Reply:
        """Keep the saved guidance intact while replying naturally to this interruption."""
        lead = self.repository.get_lead(lead_id)
        pending = self._fact_value(lead_id, "guidance_pending_signature")
        if (
            lead
            and lead["discovery_step"] == "guidance_confirmation"
            and pending
            and not self._pending_guidance_matches_current(lead_id, pending)
        ):
            pending = None
        if lead and lead["discovery_step"] == "guidance_confirmation" and pending:
            return self._with_ai_conversation_copy(
                Reply(
                    "Got it. Your earlier course preferences are still here whenever you'd like "
                    "to continue, adjust them, or look through sample courses.",
                    (
                        (
                            "Continue with my current answers",
                            f"guidance:confirm:{_guidance_token(pending)}",
                        ),
                        ("Change or add answers", f"guidance:revise:{_guidance_token(pending)}"),
                        ("Browse sample courses", "path:browse"),
                    ),
                ),
                assistant_message,
            )
        fallback = (
            "Hi! I'm AdmitFlow's AI course-guidance assistant for a fictional course catalog. "
            "What are you curious about studying?"
            if intent == "conversation"
            else "I can help explore the fictional course catalog. What would you like to know?"
        )
        return self._with_ai_conversation_copy(
            Reply(
                fallback,
                (
                    ("Browse sample courses", "path:browse"),
                    ("Choose a course-guidance path", "menu:start"),
                ),
            ),
            assistant_message,
        )

    @staticmethod
    def _with_ai_conversation_copy(reply: Reply, assistant_message: str | None) -> Reply:
        """Use model-authored copy while retaining app-owned buttons and transitions."""
        if not assistant_message:
            return reply
        message = assistant_message.strip()
        if not message or len(message) > 700:
            return reply
        return Reply(message, reply.buttons)

    def _ai_conversation_context(self, lead_id: int, current_text: str) -> dict[str, object]:
        """Build bounded, identifier-free context from demo chat and allowlisted saved facts."""
        messages = self.repository.list_messages(lead_id)
        if (
            messages
            and messages[-1]["direction"] == "inbound"
            and messages[-1]["body"] == current_text
        ):
            messages = messages[:-1]
        recent = [
            {
                "role": "user" if item["direction"] == "inbound" else "assistant",
                "content": str(item["body"])[-800:],
            }
            for item in messages[-8:]
        ]
        safe_prefixes = (
            "interest_field_",
            "interest_fields_",
            "education_level_",
            "interest_terms_",
            "activity_terms_",
            "interest_activity_",
            "learning_goals_",
            "language_support_preference_",
            "delivery_mode_preference_",
            "course_choice_parent",
        )
        saved_profile = [
            {"fact": str(item["fact_key"]), "value": str(item["fact_value"])}
            for item in self.repository.list_facts(lead_id)
            if str(item["fact_key"]).startswith(safe_prefixes)
        ]
        lead = self.repository.get_lead(lead_id)
        active_speaker = next(
            (
                str(item["fact_value"])
                for item in self.repository.list_facts(lead_id)
                if item["fact_key"] == "active_speaker"
            ),
            "student",
        )
        selected_course_name = None
        if lead and lead["selected_course_id"]:
            selected_course = self.repository.get_course(
                self.tenant_id, str(lead["selected_course_id"])
            )
            selected_course_name = selected_course.name if selected_course else None
        return {
            "recent_conversation": recent,
            "saved_catalog_preferences": saved_profile,
            "active_speaker": active_speaker,
            "guidance_stage": str(lead["discovery_step"]) if lead else "new",
            "selected_course": selected_course_name,
            "response_language": self.preferred_language(lead_id),
        }

    def _pending_guidance_matches_current(self, lead_id: int, pending: str) -> bool:
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        signature = _guidance_signature(
            interests,
            activities,
            level,
            goals,
            language_support,
            self._student_delivery_mode(lead_id),
        )
        return pending == signature

    def _present_guidance(self, lead_id: int) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        delivery_mode = self._student_delivery_mode(lead_id)
        if interests or activities:
            if not has_sufficient_guidance_context(
                interests=interests,
                activities=activities,
                level=level,
                learning_goals=goals,
            ):
                self.repository.delete_fact(lead_id, "guidance_pending_signature")
                self.repository.update_lead(lead_id, discovery_step="guidance_signal")
                if interests:
                    candidate_courses = recommend_courses(
                        courses, interests=interests, activities=set(), limit=10
                    )
                    activity_choices = tuple(
                        (
                            _activity_label(activity),
                            f"guidance:activity:{_activity_slug(activity)}",
                        )
                        for activity in dict.fromkeys(
                            activity
                            for match in candidate_courses
                            for activity in match.course.activities
                        )
                    )[:3]
                    return Reply(
                        "You mentioned "
                        f"{', '.join(sorted(interests))}. What would you like to do or learn "
                        "more about in that area? You can choose an example or tell me your "
                        "study level.",
                        activity_choices
                        + tuple(
                            (label, f"guidance:level:{value}")
                            for label, value in (
                                ("Certificate / vocational", "vocational_certificate"),
                                ("Diploma", "diploma"),
                                ("Undergraduate", "undergraduate"),
                                ("Postgraduate", "postgraduate"),
                            )
                        ),
                    )
                return Reply(
                    f"You mentioned {', '.join(sorted(activities))}. What topics would you "
                    "like to explore through those activities? You can choose a field or describe "
                    "one in your own words.",
                    tuple(
                        (field.replace("/", " & ").title(), f"field:{field}")
                        for field in sorted({course.field for course in courses})
                    ),
                )
            if not goals and not language_support:
                candidates = recommend_courses(
                    courses,
                    interests=interests,
                    activities=activities,
                    level=None if level == "any" else level,
                    limit=100,
                )
                goal_options = tuple(
                    dict.fromkeys(
                        goal for match in candidates for goal in match.course.learning_goals
                    )
                )
                base_signature = _guidance_signature(interests, activities, level)
                asked_signature = self._fact_value(lead_id, "guidance_goal_prompted_signature")
                mode_was_asked = (
                    self._fact_value(lead_id, "guidance_delivery_mode_prompted_signature")
                    == base_signature
                )
                needs_goal = len(candidates) > 3 and len(goal_options) > 1
                if needs_goal and asked_signature != base_signature and not mode_was_asked:
                    self.repository.save_fact(
                        lead_id,
                        "guidance_goal_prompted_signature",
                        base_signature,
                        "student",
                    )
                    self.repository.update_lead(lead_id, discovery_step="guidance_goal")
                    return self._goal_question_reply(goal_options)
            if not language_support:
                candidates = recommend_courses(
                    courses,
                    interests=interests,
                    activities=activities,
                    learning_goals=goals,
                    level=None if level == "any" else level,
                    limit=100,
                )
                support_options = tuple(
                    dict.fromkeys(
                        support for match in candidates for support in match.course.language_support
                    )
                )
                teaching_media = {match.course.medium for match in candidates}
                base_signature = _guidance_signature(interests, activities, level, goals)
                asked_signature = self._fact_value(lead_id, "guidance_language_prompted_signature")
                goal_was_asked = self._fact_value(
                    lead_id, "guidance_goal_prompted_signature"
                ) == _guidance_signature(interests, activities, level)
                if (
                    len(candidates) > 3
                    and len(teaching_media) == 1
                    and len(support_options) > 1
                    and asked_signature != base_signature
                    and not goal_was_asked
                ):
                    self.repository.save_fact(
                        lead_id,
                        "guidance_language_prompted_signature",
                        base_signature,
                        "student",
                    )
                    self.repository.update_lead(lead_id, discovery_step="guidance_language_support")
                    return self._language_support_question(candidates, support_options)
            if not delivery_mode:
                candidates = recommend_courses(
                    courses,
                    interests=interests,
                    activities=activities,
                    learning_goals=goals,
                    language_support_preference=language_support,
                    level=None if level == "any" else level,
                    limit=100,
                )
                modes = tuple(
                    mode
                    for mode in ("in_person", "online", "hybrid")
                    if any(mode in match.course.delivery_modes for match in candidates)
                )
                base_signature = _guidance_signature(
                    interests, activities, level, goals, language_support
                )
                asked_signature = self._fact_value(
                    lead_id, "guidance_delivery_mode_prompted_signature"
                )
                goal_was_asked = self._fact_value(
                    lead_id, "guidance_goal_prompted_signature"
                ) == _guidance_signature(interests, activities, level)
                language_was_asked = self._fact_value(
                    lead_id, "guidance_language_prompted_signature"
                ) == _guidance_signature(interests, activities, level, goals)
                mode_was_asked = (
                    self._fact_value(lead_id, "guidance_delivery_mode_prompted_signature")
                    == base_signature
                )
                if (
                    len(candidates) > 3
                    and len(modes) > 1
                    and asked_signature != base_signature
                    and not goal_was_asked
                    and not mode_was_asked
                    and not language_was_asked
                ):
                    self.repository.save_fact(
                        lead_id,
                        "guidance_delivery_mode_prompted_signature",
                        base_signature,
                        "student",
                    )
                    self.repository.update_lead(lead_id, discovery_step="guidance_delivery_mode")
                    return self._delivery_mode_question(modes)
            signature = _guidance_signature(
                interests, activities, level, goals, language_support, delivery_mode
            )
            confirmed = self._fact_value(lead_id, "guidance_confirmed_signature")
            if confirmed == signature:
                return self._guidance_recommendation_reply(
                    lead_id,
                    courses,
                    interests,
                    activities,
                    level,
                    goals,
                    language_support,
                    delivery_mode,
                )
            return self._guidance_reflection(
                lead_id,
                interests,
                activities,
                level,
                goals,
                language_support,
                signature,
                delivery_mode,
            )
        self.repository.delete_fact(lead_id, "guidance_pending_signature")
        self.repository.update_lead(lead_id, discovery_step="guidance_signal")
        return Reply(
            "I have not got enough detail to suggest a course yet. What topic or activity would "
            "you like to explore? You can mention a study level too.",
            (("Choose a field", "path:field"), ("Browse sample courses", "path:browse")),
        )

    def _guidance_goal_prompt(self, lead_id: int) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        interests, activities, level, goals, _ = self._student_guidance_context(lead_id)
        if goals:
            return self._present_guidance(lead_id)
        candidates = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            level=None if level == "any" else level,
            limit=100,
        )
        goal_options = tuple(
            dict.fromkeys(goal for match in candidates for goal in match.course.learning_goals)
        )
        if len(candidates) <= 3 or len(goal_options) <= 1:
            return self._present_guidance(lead_id)
        return self._goal_question_reply(goal_options)

    def _guidance_language_support_prompt(self, lead_id: int) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        if language_support:
            return self._present_guidance(lead_id)
        candidates = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            learning_goals=goals,
            level=None if level == "any" else level,
            limit=100,
        )
        support_options = tuple(
            dict.fromkeys(
                support for match in candidates for support in match.course.language_support
            )
        )
        if (
            len(candidates) <= 3
            or len({match.course.medium for match in candidates}) != 1
            or len(support_options) <= 1
        ):
            return self._present_guidance(lead_id)
        return self._language_support_question(candidates, support_options)

    def _guidance_delivery_mode_prompt(self, lead_id: int) -> Reply:
        courses = self.repository.list_courses(self.tenant_id)
        interests, activities, level, goals, language_support = self._student_guidance_context(
            lead_id
        )
        if self._student_delivery_mode(lead_id):
            return self._present_guidance(lead_id)
        expected_signature = _guidance_signature(
            interests, activities, level, goals, language_support
        )
        if (
            self._fact_value(lead_id, "guidance_delivery_mode_prompted_signature")
            != expected_signature
        ):
            return self._present_guidance(lead_id)
        candidates = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            learning_goals=goals,
            language_support_preference=language_support,
            level=None if level == "any" else level,
            limit=100,
        )
        modes = tuple(
            mode
            for mode in ("in_person", "online", "hybrid")
            if any(mode in match.course.delivery_modes for match in candidates)
        )
        if len(candidates) <= 3 or len(modes) <= 1:
            return self._present_guidance(lead_id)
        return self._delivery_mode_question(modes)

    @staticmethod
    def _delivery_mode_question(modes: tuple[str, ...]) -> Reply:
        labels = {"in_person": "In person", "online": "Online", "hybrid": "Hybrid"}
        buttons = tuple(
            (labels[mode], f"guidance:mode:{mode}") for mode in modes[:3] if mode in labels
        ) + (("Leave format open", "guidance:mode:open"),)
        return Reply(
            "The sample catalog lists different study formats for these courses. Does in-person, "
            "online, or hybrid study matter to you, or should I leave format open? These are "
            "sample catalog labels, not a promise about a specific schedule or access needs.",
            buttons,
        )

    @staticmethod
    def _language_support_question(
        candidates: list[CourseMatch], support_options: tuple[str, ...]
    ) -> Reply:
        media = {match.course.medium for match in candidates}
        prefix = (
            f"The catalog lists {next(iter(media))} as the teaching medium for these courses. "
            if len(media) == 1
            else "The catalog lists different teaching media for these courses. "
        )
        buttons = tuple(
            (support, f"guidance:language:{_language_support_slug(support)}")
            for support in support_options[:3]
        ) + (("Leave language open", "guidance:language:open"),)
        return Reply(
            prefix
            + "Recorded language support differs. Would one listed support option matter to you, "
            "or should I leave language open? This is your preference; I won't assume your "
            "language ability.",
            buttons,
        )

    @staticmethod
    def _goal_question_reply(goal_options: tuple[str, ...]) -> Reply:
        buttons = tuple(
            (goal.capitalize(), f"guidance:goal:{_goal_slug(goal)}") for goal in goal_options[:3]
        ) + (("Skip this question", "guidance:goal:skip"),)
        return Reply(
            "What would you most like to learn or be able to do through your studies? "
            "Choose an example or answer in your own words.",
            buttons,
        )

    def _guidance_recommendation_reply(
        self,
        lead_id: int,
        courses: list[Course],
        interests: set[str],
        activities: set[str],
        level: str | None,
        goals: set[str],
        language_support: str | None,
        delivery_mode: str | None = None,
    ) -> Reply:
        matches = recommend_courses(
            courses,
            interests=interests,
            activities=activities,
            learning_goals=goals,
            language_support_preference=language_support,
            delivery_mode_preference=delivery_mode,
            level=None if level == "any" else level,
            limit=3,
        )
        if not matches:
            if delivery_mode:
                return Reply(
                    "No complete matching sample course lists "
                    f"{delivery_mode.replace('_', ' ')} study. Would you like to leave format "
                    "open and see other matches, or browse the catalog?",
                    (
                        ("Leave format open", "guidance:mode:open"),
                        ("Browse sample courses", "path:browse"),
                    ),
                )
            if language_support:
                return Reply(
                    "No complete matching sample course lists "
                    f"{language_support}. Would you like to leave language open and see the "
                    "other matches, or browse the catalog?",
                    (
                        ("Leave language open", "guidance:language:open"),
                        ("Browse sample courses", "path:browse"),
                    ),
                )
            self.repository.update_lead(lead_id, discovery_step="guidance_revision")
            return Reply(
                "I couldn't find a complete sample course that matches all those preferences. "
                "I can broaden the search if you change or remove a preference, or show every "
                "sample course so you can compare them.",
                (
                    ("Change my preferences", "path:explore"),
                    ("Browse sample courses", "path:browse"),
                ),
            )
        self.repository.update_lead(
            lead_id, discovery_step="results", lifecycle_stage="discovering"
        )
        summaries = "\n".join(
            f"• {match.course.name} ({match.course.education_level.replace('_', ' ')}): "
            f"{', '.join(match.reasons)}. Teaching medium listed: {match.course.medium}; "
            f"language support listed: "
            f"{', '.join(match.course.language_support) or 'not specified'}. "
            f"Study format listed: "
            f"{', '.join(match.course.delivery_modes).replace('_', ' ') or 'not specified'}. "
            f"Sample entry: {'; '.join(match.course.prerequisites)}."
            for match in matches
        )
        return Reply(
            "Based on what you confirmed, here are matching fictional sample courses:\n"
            f"{summaries}\n\nThese are examples, not an admission decision. Which would you "
            "like to explore?",
            tuple((match.course.name, f"guidance:course:{match.course.id}") for match in matches),
        )


def _has_discovery_signal(turn: DiscoveryTurn) -> bool:
    """Whether this turn adds a learner preference, correction, or explicit uncertainty."""
    return bool(
        turn.correct_previous
        or turn.fields
        or turn.education_level
        or turn.interests
        or turn.activities
        or turn.learning_goals
        or turn.language_support_preference
        or turn.delivery_mode_preference
        or turn.retracted_preferences
        or turn.unsure
    )


def _guidance_signature(
    interests: set[str],
    activities: set[str],
    level: str | None,
    learning_goals: set[str] | None = None,
    language_support_preference: str | None = None,
    delivery_mode_preference: str | None = None,
) -> str:
    context = {
        "interests": sorted(item.casefold() for item in interests),
        "activities": sorted(item.casefold() for item in activities),
        "level": level,
        "learning_goals": sorted(item.casefold() for item in learning_goals or set()),
        "language_support_preference": (
            language_support_preference.casefold() if language_support_preference else None
        ),
        "delivery_mode_preference": (
            delivery_mode_preference.casefold() if delivery_mode_preference else None
        ),
    }
    return hashlib.sha256(json.dumps(context, sort_keys=True).encode("utf-8")).hexdigest()


def _guidance_token(signature: str) -> str:
    return signature[:12]


def _is_guidance_confirmation(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold()).strip()
    return normalized in {
        "yes",
        "yes show",
        "yes show me",
        "yes show courses",
        "yes that sounds right",
        "that sounds right",
        "sounds right",
        "looks right",
        "correct show options",
        "show options",
        "show courses",
        "go ahead",
        "haan",
        "haan dikhao",
        "haan sahi hai",
        "sahi hai",
        "हाँ",
        "हां",
        "हाँ सही है",
        "हां सही है",
        "हाँ विकल्प दिखाएँ",
        "അതെ",
        "ശരിയാണ്",
        "അതെ ശരിയാണ്",
        "ഓപ്ഷനുകൾ കാണിക്കൂ",
    }


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


def _is_simple_greeting(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold()).strip()
    return normalized in {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}


def _is_assistant_identity_question(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold()).strip()
    return normalized in {
        "what are you",
        "who are you",
        "are you a bot",
        "are you ai",
        "are you human",
        "what can you do",
        "who made you",
    }


def _is_explicit_staff_request(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold()).strip()
    if normalized in {"staff", "human", "counsellor", "counselor", "admissions officer"}:
        return True
    requests = (
        "talk to",
        "talk with",
        "speak to",
        "speak with",
        "connect me to",
        "connect me with",
        "let me talk to",
        "i want to talk to",
    )
    targets = ("staff", "human", "person", "counsellor", "counselor", "admissions officer")
    return any(request in normalized for request in requests) and any(
        target in normalized for target in targets
    )


def _is_language_concern(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold())
    medium_terms = {"english", "hindi", "malayalam", "hinglish"}
    if any(
        phrase in normalized for phrase in {"medium of instruction", "teaching medium", "taught in"}
    ) or ("medium" in normalized.split() and bool(medium_terms & set(normalized.split()))):
        return True
    if any(
        phrase in normalized
        for phrase in (
            "changed my mind",
            "don t want",
            "no longer",
            "not anymore",
            "remove",
            "retract",
            "withdraw",
            "drop",
            "instead of",
        )
    ):
        return False
    if normalized.startswith(
        ("i want ", "i need ", "i prefer ", "i would like ", "i d like ", "my preference ")
    ):
        return False
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


def _is_ai_opt_out(text: str) -> bool:
    normalized = re.sub(r"[^\w]+", " ", text.casefold()).strip()
    return any(
        phrase in normalized
        for phrase in {
            "stop ai",
            "turn off ai",
            "disable ai",
            "stop openai",
            "turn off openai",
            "revoke ai consent",
            "revoke consent",
            "do not send to openai",
            "do not send openai",
            "dont send to openai",
            "dont send openai",
            "don't send to openai",
            "don t send to openai",
            "don t send openai",
            "no ai processing",
            "openai processing band karo",
            "openai processing band karein",
            "ai band karo",
            "consent wapas lo",
            "meri consent wapas lo",
            "openai प्रोसेसिंग बंद करें",
            "एआई बंद करें",
            "मेरी सहमति वापस लें",
            "openai പ്രോസസ്സിംഗ് ഓഫ് ചെയ്യുക",
            "ai ഓഫ് ചെയ്യുക",
            "സമ്മതം പിൻവലിക്കുക",
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


def _goal_slug(goal: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", goal.casefold()).strip("-")


def _language_support_slug(support: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", support.casefold()).strip("-")


def _delivery_mode_slug(mode: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", mode.casefold()).strip("_")


def _activity_label(activity: str) -> str:
    return activity[:1].upper() + activity[1:]
