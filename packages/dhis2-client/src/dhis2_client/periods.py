"""Hand-written `PeriodType` StrEnum — DHIS2's canonical period-type names.

DHIS2's `/api/schemas` reports `DataSet.periodType` as `TEXT` (not CONSTANT)
because upstream `PeriodType` is a Java class hierarchy — `MonthlyPeriodType`,
`DailyPeriodType`, etc. are subclasses, not enum constants. The 24 canonical
type-name strings live in `PeriodTypeEnum` (a separate helper enum DHIS2 uses
for mapping to/from the hierarchy). We list them here as a StrEnum so callers
get type-safe access to the same values. Version-independent — the set hasn't
changed across 2.40+.
"""

from __future__ import annotations

from enum import StrEnum


class PeriodType(StrEnum):
    """DHIS2 period types — the valid values for `DataSet.periodType`."""

    DAILY = "Daily"
    WEEKLY = "Weekly"
    WEEKLY_WEDNESDAY = "WeeklyWednesday"
    WEEKLY_THURSDAY = "WeeklyThursday"
    WEEKLY_FRIDAY = "WeeklyFriday"
    WEEKLY_SATURDAY = "WeeklySaturday"
    WEEKLY_SUNDAY = "WeeklySunday"
    BI_WEEKLY = "BiWeekly"
    MONTHLY = "Monthly"
    BI_MONTHLY = "BiMonthly"
    QUARTERLY = "Quarterly"
    QUARTERLY_NOV = "QuarterlyNov"
    SIX_MONTHLY = "SixMonthly"
    SIX_MONTHLY_APRIL = "SixMonthlyApril"
    SIX_MONTHLY_NOV = "SixMonthlyNov"
    YEARLY = "Yearly"
    TWO_YEARLY = "TwoYearly"
    FINANCIAL_FEB = "FinancialFeb"
    FINANCIAL_APRIL = "FinancialApril"
    FINANCIAL_JULY = "FinancialJuly"
    FINANCIAL_AUG = "FinancialAug"
    FINANCIAL_SEP = "FinancialSep"
    FINANCIAL_OCT = "FinancialOct"
    FINANCIAL_NOV = "FinancialNov"


__all__ = ["PeriodType"]
