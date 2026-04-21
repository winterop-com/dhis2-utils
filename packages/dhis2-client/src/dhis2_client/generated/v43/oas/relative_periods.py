"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class RelativePeriods(_BaseModel):
    """OpenAPI schema `RelativePeriods`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    biMonthsThisYear: bool | None = None
    last10FinancialYears: bool | None = None
    last10Years: bool | None = None
    last12Months: bool | None = None
    last12Weeks: bool | None = None
    last14Days: bool | None = None
    last180Days: bool | None = None
    last2SixMonths: bool | None = None
    last30Days: bool | None = None
    last3Days: bool | None = None
    last3Months: bool | None = None
    last4BiWeeks: bool | None = None
    last4Quarters: bool | None = None
    last4Weeks: bool | None = None
    last52Weeks: bool | None = None
    last5FinancialYears: bool | None = None
    last5Years: bool | None = None
    last60Days: bool | None = None
    last6BiMonths: bool | None = None
    last6Months: bool | None = None
    last7Days: bool | None = None
    last90Days: bool | None = None
    lastBiWeek: bool | None = None
    lastBimonth: bool | None = None
    lastFinancialYear: bool | None = None
    lastMonth: bool | None = None
    lastQuarter: bool | None = None
    lastSixMonth: bool | None = None
    lastWeek: bool | None = None
    lastYear: bool | None = None
    monthsLastYear: bool | None = None
    monthsThisYear: bool | None = None
    quartersLastYear: bool | None = None
    quartersThisYear: bool | None = None
    thisBiWeek: bool | None = None
    thisBimonth: bool | None = None
    thisDay: bool | None = None
    thisFinancialYear: bool | None = None
    thisMonth: bool | None = None
    thisQuarter: bool | None = None
    thisSixMonth: bool | None = None
    thisWeek: bool | None = None
    thisYear: bool | None = None
    weeksThisYear: bool | None = None
    yesterday: bool | None = None
