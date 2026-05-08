"""Hand-written period enums — `PeriodType` (frequency) + `RelativePeriod` (rolling window).

`PeriodType` is the frequency a `DataSet` collects data at (Daily, Monthly,
Quarterly…). DHIS2's `/api/schemas` reports `DataSet.periodType` as `TEXT`
(not CONSTANT) because upstream it's a Java class hierarchy —
`MonthlyPeriodType`, `DailyPeriodType`, etc. are subclasses, not enum
constants. We list the canonical type-name strings here as a StrEnum.

`RelativePeriod` mirrors the 45 boolean flags on the generated
`RelativePeriods` model (`generated/v42/oas/relative_periods.py`) — the
rolling windows a `Visualization` / `EventVisualization` / `Map` can pin
itself to (`last12Months`, `thisYear`, `lastSixMonth`, …). Use the enum
on builder APIs so callers don't have to remember the exact flag casing,
and materialise the selected set into a `RelativePeriods` model by
toggling the matching fields to `True`.

Both enums are version-independent — the value sets haven't changed
across 2.40+.
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


class RelativePeriod(StrEnum):
    """Rolling-window flags on the `RelativePeriods` model."""

    BI_MONTHS_THIS_YEAR = "biMonthsThisYear"
    LAST_10_FINANCIAL_YEARS = "last10FinancialYears"
    LAST_10_YEARS = "last10Years"
    LAST_12_MONTHS = "last12Months"
    LAST_12_WEEKS = "last12Weeks"
    LAST_14_DAYS = "last14Days"
    LAST_180_DAYS = "last180Days"
    LAST_2_SIX_MONTHS = "last2SixMonths"
    LAST_30_DAYS = "last30Days"
    LAST_3_DAYS = "last3Days"
    LAST_3_MONTHS = "last3Months"
    LAST_4_BI_WEEKS = "last4BiWeeks"
    LAST_4_QUARTERS = "last4Quarters"
    LAST_4_WEEKS = "last4Weeks"
    LAST_52_WEEKS = "last52Weeks"
    LAST_5_FINANCIAL_YEARS = "last5FinancialYears"
    LAST_5_YEARS = "last5Years"
    LAST_60_DAYS = "last60Days"
    LAST_6_BI_MONTHS = "last6BiMonths"
    LAST_6_MONTHS = "last6Months"
    LAST_7_DAYS = "last7Days"
    LAST_90_DAYS = "last90Days"
    LAST_BI_WEEK = "lastBiWeek"
    LAST_BIMONTH = "lastBimonth"
    LAST_FINANCIAL_YEAR = "lastFinancialYear"
    LAST_MONTH = "lastMonth"
    LAST_QUARTER = "lastQuarter"
    LAST_SIX_MONTH = "lastSixMonth"
    LAST_WEEK = "lastWeek"
    LAST_YEAR = "lastYear"
    MONTHS_LAST_YEAR = "monthsLastYear"
    MONTHS_THIS_YEAR = "monthsThisYear"
    QUARTERS_LAST_YEAR = "quartersLastYear"
    QUARTERS_THIS_YEAR = "quartersThisYear"
    THIS_BI_WEEK = "thisBiWeek"
    THIS_BIMONTH = "thisBimonth"
    THIS_DAY = "thisDay"
    THIS_FINANCIAL_YEAR = "thisFinancialYear"
    THIS_MONTH = "thisMonth"
    THIS_QUARTER = "thisQuarter"
    THIS_SIX_MONTH = "thisSixMonth"
    THIS_WEEK = "thisWeek"
    THIS_YEAR = "thisYear"
    WEEKS_THIS_YEAR = "weeksThisYear"
    YESTERDAY = "yesterday"


__all__ = ["PeriodType", "RelativePeriod"]
