"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class AnalyticsPeriodBoundaryCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsPeriodBoundaryLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsPeriodBoundaryUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class AnalyticsPeriodBoundary(_BaseModel):
    """OpenAPI schema `AnalyticsPeriodBoundary`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    analyticsPeriodBoundaryType: (
        Literal[
            "BEFORE_START_OF_REPORTING_PERIOD",
            "BEFORE_END_OF_REPORTING_PERIOD",
            "AFTER_START_OF_REPORTING_PERIOD",
            "AFTER_END_OF_REPORTING_PERIOD",
        ]
        | None
    ) = None
    attributeValues: list[AttributeValue] | None = None
    boundaryTarget: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: AnalyticsPeriodBoundaryCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: AnalyticsPeriodBoundaryLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    offsetPeriodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialApril",
            "FinancialJuly",
            "FinancialNov",
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
    user: AnalyticsPeriodBoundaryUser | None = _Field(default=None, description="A UID reference to a User  ")
