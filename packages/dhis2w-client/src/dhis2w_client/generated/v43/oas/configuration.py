"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .identifiable_object import IdentifiableObject


class Configuration(_BaseModel):
    """OpenAPI schema `Configuration`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    corsAllowlist: list[str] | None = None
    corsWhitelist: list[str] | None = None
    dataOutputPeriodTypes: (
        list[
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
        ]
        | None
    ) = None
    facilityOrgUnitGroupSet: BaseIdentifiableObject | None = None
    facilityOrgUnitLevel: BaseIdentifiableObject | None = None
    feedbackRecipients: BaseIdentifiableObject | None = None
    infrastructuralDataElements: BaseIdentifiableObject | None = None
    infrastructuralIndicators: IdentifiableObject | None = None
    infrastructuralPeriodType: (
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
    offlineOrganisationUnitLevel: BaseIdentifiableObject | None = None
    selfRegistrationOrgUnit: BaseIdentifiableObject | None = None
    selfRegistrationRole: BaseIdentifiableObject | None = None
    systemId: str | None = None
    systemUpdateNotificationRecipients: BaseIdentifiableObject | None = None
