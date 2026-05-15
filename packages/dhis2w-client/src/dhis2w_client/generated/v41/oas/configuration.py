"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class ConfigurationFacilityOrgUnitGroupSet(_BaseModel):
    """A UID reference to a OrganisationUnitGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationFacilityOrgUnitLevel(_BaseModel):
    """A UID reference to a OrganisationUnitLevel  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationFeedbackRecipients(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationInfrastructuralDataElements(_BaseModel):
    """A UID reference to a DataElementGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationInfrastructuralIndicators(_BaseModel):
    """A UID reference to a IndicatorGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationOfflineOrganisationUnitLevel(_BaseModel):
    """A UID reference to a OrganisationUnitLevel  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationSelfRegistrationOrgUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationSelfRegistrationRole(_BaseModel):
    """A UID reference to a UserRole  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ConfigurationSystemUpdateNotificationRecipients(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Configuration(_BaseModel):
    """OpenAPI schema `Configuration`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    corsAllowlist: list[str] | None = None
    corsWhitelist: list[str] | None = None
    facilityOrgUnitGroupSet: ConfigurationFacilityOrgUnitGroupSet | None = _Field(
        default=None, description="A UID reference to a OrganisationUnitGroupSet  "
    )
    facilityOrgUnitLevel: ConfigurationFacilityOrgUnitLevel | None = _Field(
        default=None, description="A UID reference to a OrganisationUnitLevel  "
    )
    feedbackRecipients: ConfigurationFeedbackRecipients | None = _Field(
        default=None, description="A UID reference to a UserGroup  "
    )
    infrastructuralDataElements: ConfigurationInfrastructuralDataElements | None = _Field(
        default=None, description="A UID reference to a DataElementGroup  "
    )
    infrastructuralIndicators: ConfigurationInfrastructuralIndicators | None = _Field(
        default=None, description="A UID reference to a IndicatorGroup  "
    )
    infrastructuralPeriodType: (
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
    offlineOrganisationUnitLevel: ConfigurationOfflineOrganisationUnitLevel | None = _Field(
        default=None, description="A UID reference to a OrganisationUnitLevel  "
    )
    selfRegistrationOrgUnit: ConfigurationSelfRegistrationOrgUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    selfRegistrationRole: ConfigurationSelfRegistrationRole | None = _Field(
        default=None, description="A UID reference to a UserRole  "
    )
    systemId: str | None = None
    systemUpdateNotificationRecipients: ConfigurationSystemUpdateNotificationRecipients | None = _Field(
        default=None, description="A UID reference to a UserGroup  "
    )
