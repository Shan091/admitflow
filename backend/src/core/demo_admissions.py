"""Explicit, institution-scoped development demos never authorise real admissions."""

from cryptography.fernet import InvalidToken
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import EncryptionKeyNotConfiguredError, decrypt_pii
from src.core.settings import get_settings
from src.db.models import Course, Institution
from src.payments.provider import Credentials


async def demo_fee(db: AsyncSession, course: Course) -> int | None:
    settings = get_settings()
    if (
        settings.app_env != "dev"
        or not settings.demo_admissions_enabled
        or settings.payments_live_enabled
        or not course.is_active
        or not course.is_reference
        or course.demo_application_fee is None
        or course.demo_application_fee < 100
    ):
        return None
    institution = await db.get(Institution, course.tenant_id)
    if (
        institution is None
        or institution.slug != settings.telegram_institution_code
        or not institution.razorpay_credentials_enc
    ):
        return None
    try:
        credentials = Credentials.model_validate_json(
            decrypt_pii(institution.razorpay_credentials_enc)
        )
    except (ValueError, InvalidToken, EncryptionKeyNotConfiguredError):
        return None
    return course.demo_application_fee if credentials.key_id.startswith("rzp_test_") else None
