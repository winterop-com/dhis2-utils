"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class DateFilterPeriod(_BaseModel):
    """OpenAPI schema `DateFilterPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    endBuffer: int | None = None
    endDate: datetime | None = None
    period: (
        Literal[
            "TODAY",
            "YESTERDAY",
            "LAST_3_DAYS",
            "LAST_7_DAYS",
            "LAST_14_DAYS",
            "LAST_30_DAYS",
            "LAST_60_DAYS",
            "LAST_90_DAYS",
            "LAST_180_DAYS",
            "THIS_MONTH",
            "LAST_MONTH",
            "THIS_BIMONTH",
            "LAST_BIMONTH",
            "THIS_QUARTER",
            "LAST_QUARTER",
            "THIS_SIX_MONTH",
            "LAST_SIX_MONTH",
            "WEEKS_THIS_YEAR",
            "MONTHS_THIS_YEAR",
            "BIMONTHS_THIS_YEAR",
            "QUARTERS_THIS_YEAR",
            "THIS_YEAR",
            "MONTHS_LAST_YEAR",
            "QUARTERS_LAST_YEAR",
            "LAST_YEAR",
            "LAST_5_YEARS",
            "LAST_10_YEARS",
            "LAST_12_MONTHS",
            "LAST_6_MONTHS",
            "LAST_3_MONTHS",
            "LAST_6_BIMONTHS",
            "LAST_4_QUARTERS",
            "LAST_2_SIXMONTHS",
            "THIS_FINANCIAL_YEAR",
            "LAST_FINANCIAL_YEAR",
            "LAST_5_FINANCIAL_YEARS",
            "LAST_10_FINANCIAL_YEARS",
            "THIS_WEEK",
            "LAST_WEEK",
            "THIS_BIWEEK",
            "LAST_BIWEEK",
            "LAST_4_WEEKS",
            "LAST_4_BIWEEKS",
            "LAST_12_WEEKS",
            "LAST_52_WEEKS",
        ]
        | None
    ) = None
    startBuffer: int | None = None
    startDate: datetime | None = None
    type: Literal["RELATIVE", "ABSOLUTE"] | None = None
