"""Cohort dates use institution-local calendar boundaries and explicit denominators."""

from datetime import UTC, date, datetime

import pytest

from src.staff.analytics import bucket_dates, percent, period_window


def test_calendar_window_includes_the_whole_local_day_across_dst():
    period = period_window("America/New_York", date(2026, 11, 1), date(2026, 11, 1))
    assert period.start_at == datetime(2026, 11, 1, 4, tzinfo=UTC)
    assert period.end_at == datetime(2026, 11, 2, 5, tzinfo=UTC)
    assert len(bucket_dates(period.start, period.end, "day")) == 1
    assert bucket_dates(date(2026, 10, 21), date(2026, 10, 29), "week") == [
        date(2026, 10, 19),
        date(2026, 10, 26),
    ]


def test_rates_do_not_invent_conversion_when_denominator_is_empty():
    assert percent(0, 0) is None
    assert percent(1, 3) == 33.33
    with pytest.raises(ValueError):
        percent(4, 3)


@pytest.mark.parametrize(
    "start,end",
    [
        (date(2026, 10, 25), date(2026, 10, 24)),
        (date(2024, 1, 1), date(2026, 1, 1)),
        (date.max, date.max),
        (date.min, date.min),
    ],
)
def test_invalid_or_excessive_periods_are_rejected(start, end):
    with pytest.raises(ValueError):
        period_window("Asia/Kolkata", start, end)


def test_final_calendar_bucket_does_not_increment_beyond_its_period():
    assert bucket_dates(date.max, date.max, "day") == [date.max]
    assert len(bucket_dates(date.max, date.max, "week")) == 1
