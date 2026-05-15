"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AnalyticsPeriodBoundaryType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class AnalyticsPeriodBoundaryParamsCreatedBy(_BaseModel):
    """OpenAPI schema `AnalyticsPeriodBoundaryParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsPeriodBoundaryParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `AnalyticsPeriodBoundaryParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsPeriodBoundaryParams(_BaseModel):
    """OpenAPI schema `AnalyticsPeriodBoundaryParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    analyticsPeriodBoundaryType: AnalyticsPeriodBoundaryType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    boundaryTarget: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: AnalyticsPeriodBoundaryParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: AnalyticsPeriodBoundaryParamsLastUpdatedBy | None = None
    name: str | None = None
    offsetPeriodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialApril",
            "FinancialJuly",
            "FinancialNov",
            "FinancialSep",
            "FinancialOct",
            "Monthly",
            "Quarterly",
            "QuarterlyNov",
            "SixMonthlyApril",
            "SixMonthlyNov",
            "SixMonthly",
            "TwoYearly",
            "Weekly",
            "WeeklySaturday",
            "WeeklySunday",
            "WeeklyThursday",
            "WeeklyWednesday",
            "Yearly",
        ]
        | None
    ) = None
    offsetPeriods: int | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
