"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .identifiable_object import IdentifiableObject
    from .user_dto import UserDto


class DataApprovalWorkflow(_BaseModel):
    """OpenAPI schema `DataApprovalWorkflow`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    categoryCombo: IdentifiableObject | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataApprovalLevels: list[IdentifiableObject] | None = None
    dataSets: list[IdentifiableObject] | None = None
    displayName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    periodType: (
        Literal[
            "BiMonthly",
            "BiWeekly",
            "Daily",
            "FinancialFeb",
            "FinancialApril",
            "FinancialJuly",
            "FinancialAug",
            "FinancialSep",
            "FinancialOct",
            "FinancialNov",
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
            "WeeklyFriday",
            "WeeklyWednesday",
            "Yearly",
        ]
        | None
    ) = None
