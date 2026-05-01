"""Unit tests for the hand-written PeriodType StrEnum."""

from __future__ import annotations

from dhis2_client import PeriodType


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
    from dhis2_client.generated.v42.enums import PeriodType as Reexported

    assert Reexported is PeriodType


def test_dataset_schema_declares_period_type() -> None:
    """DataSet.periodType is typed PeriodType | None after codegen, not str."""
    from typing import get_args

    from dhis2_client.generated.v42.schemas.data_set import DataSet

    field = DataSet.model_fields["periodType"]
    # the annotation is `PeriodType | None` — verify PeriodType is in the union
    assert PeriodType in get_args(field.annotation)
