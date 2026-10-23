"""Keep development-only throttle state independent across database test cases."""

import pytest

from src.staff import throttle


@pytest.fixture(autouse=True)
def isolated_local_login_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    # Preserve throttling within each case; unrelated synthetic clients must not
    # inherit the account's ten-attempt window from earlier test cases.
    monkeypatch.setattr(throttle, "_local", {})
