"""Unit tests for the hand-written PeriodType StrEnum."""

from __future__ import annotations

from dhis2w_client import PeriodType


def test_canonical_names_complete() -> None:
    """PeriodType lists every string name DHIS2's PeriodTypeEnum ships."""
    values = {m.value for m in PeriodType}
    assert values == {
        "Daily",
        "Weekly",
        "WeeklyWednesday",
        "WeeklyThursday",
        "WeeklyFriday",
        "WeeklySaturday",
        "WeeklySunday",
        "BiWeekly",
        "Monthly",
        "BiMonthly",
        "Quarterly",
        "QuarterlyNov",
        "SixMonthly",
        "SixMonthlyApril",
        "SixMonthlyNov",
        "Yearly",
        "TwoYearly",
        "FinancialFeb",
        "FinancialApril",
        "FinancialJuly",
        "FinancialAug",
        "FinancialSep",
        "FinancialOct",
        "FinancialNov",
    }


def test_str_enum_interop_with_bare_strings() -> None:
    """StrEnum members compare equal to their wire strings (str subclass)."""
    assert PeriodType.MONTHLY.value == "Monthly"
    assert PeriodType("Daily") is PeriodType.DAILY
    assert str(PeriodType.YEARLY) == "Yearly"


def test_reexported_from_generated_enums() -> None:
    """The generated v42 enums module re-exports PeriodType so schema modules can import it."""
    from dhis2w_client.generated.v42.enums import PeriodType as Reexported

    assert Reexported is PeriodType


def test_dataset_schema_declares_period_type() -> None:
    """DataSet.periodType is typed PeriodType | None after codegen, not str."""
    from typing import get_args

    from dhis2w_client.generated.v42.schemas.data_set import DataSet

    field = DataSet.model_fields["periodType"]
    # the annotation is `PeriodType | None` — verify PeriodType is in the union
    assert PeriodType in get_args(field.annotation)


# --- period-id math (parse_period / next / previous / start-end) ---------


from datetime import date  # noqa: E402

import pytest  # noqa: E402
from dhis2w_client.v42.periods import (  # noqa: E402
    Period,
    PeriodKind,
    next_period_id,
    parse_period,
    period_start_end,
    previous_period_id,
)


def test_parse_daily() -> None:
    """Parse daily."""
    p = parse_period("20240315")
    assert p == Period(id="20240315", kind=PeriodKind.DAILY, start=date(2024, 3, 15), end=date(2024, 3, 15))


def test_parse_weekly_iso() -> None:
    """ISO week 1 of 2024 starts on 2024-01-01 (a Monday)."""
    p = parse_period("2024W1")
    assert p.kind is PeriodKind.WEEKLY
    assert p.start == date(2024, 1, 1)
    assert p.end == date(2024, 1, 7)


def test_parse_monthly_year_boundary() -> None:
    """December rollovers compute end-of-month correctly."""
    p = parse_period("202412")
    assert p.start == date(2024, 12, 1)
    assert p.end == date(2024, 12, 31)


def test_parse_quarterly() -> None:
    """Parse quarterly."""
    p = parse_period("2024Q1")
    assert p.kind is PeriodKind.QUARTERLY
    assert (p.start, p.end) == (date(2024, 1, 1), date(2024, 3, 31))


def test_parse_six_monthly() -> None:
    """Parse six monthly."""
    h1 = parse_period("2024S1")
    h2 = parse_period("2024S2")
    assert (h1.start, h1.end) == (date(2024, 1, 1), date(2024, 6, 30))
    assert (h2.start, h2.end) == (date(2024, 7, 1), date(2024, 12, 31))


def test_parse_yearly() -> None:
    """Parse yearly."""
    p = parse_period("2024")
    assert p.kind is PeriodKind.YEARLY
    assert (p.start, p.end) == (date(2024, 1, 1), date(2024, 12, 31))


@pytest.mark.parametrize("bad", ["LAST_12_MONTHS", "2024Q5", "20240230", "2024W54", "abc", ""])
def test_parse_rejects_unknown_or_out_of_range(bad: str) -> None:
    """Relative-period names and out-of-range values raise ValueError."""
    with pytest.raises(ValueError):
        parse_period(bad)


@pytest.mark.parametrize(
    ("pid", "expected"),
    [
        ("20240315", "20240316"),
        ("20241231", "20250101"),
        ("2024W1", "2024W02"),
        ("2024W52", "2025W01"),
        ("202403", "202404"),
        ("202412", "202501"),
        ("2024Q1", "2024Q2"),
        ("2024Q4", "2025Q1"),
        ("2024S1", "2024S2"),
        ("2024S2", "2025S1"),
        ("2024", "2025"),
    ],
)
def test_next_period_id(pid: str, expected: str) -> None:
    """`next_period_id` rolls forward correctly across all six kinds + boundaries."""
    assert next_period_id(pid) == expected


@pytest.mark.parametrize(
    ("pid", "expected"),
    [
        ("20240315", "20240314"),
        ("20240101", "20231231"),
        ("2024W2", "2024W01"),
        ("2024W1", "2023W52"),
        ("202403", "202402"),
        ("202401", "202312"),
        ("2024Q1", "2023Q4"),
        ("2024S1", "2023S2"),
        ("2024", "2023"),
    ],
)
def test_previous_period_id(pid: str, expected: str) -> None:
    """`previous_period_id` rolls backward correctly across all six kinds + boundaries."""
    assert previous_period_id(pid) == expected


def test_period_start_end_returns_inclusive_dates() -> None:
    """Both endpoints are inclusive — last day of the period, not the day after."""
    start, end = period_start_end("202402")
    assert start == date(2024, 2, 1)
    assert end == date(2024, 2, 29)  # 2024 is a leap year


def test_round_trip_next_then_previous_is_identity() -> None:
    """`previous(next(p))` returns the original id for every kind."""
    for pid in ["20240315", "2024W12", "202403", "2024Q1", "2024S1", "2024"]:
        assert previous_period_id(next_period_id(pid)) == pid
