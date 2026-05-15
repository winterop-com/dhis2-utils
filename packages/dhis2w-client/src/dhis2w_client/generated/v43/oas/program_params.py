"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AccessLevel, FeatureType, ProgramType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_combo_params import CategoryComboParams
    from .object_style import ObjectStyle
    from .program_category_mapping import ProgramCategoryMapping
    from .program_tracked_entity_attribute_params import ProgramTrackedEntityAttributeParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsDataEntryForm(_BaseModel):
    """OpenAPI schema `ProgramParamsDataEntryForm`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsNotificationTemplates(_BaseModel):
    """OpenAPI schema `ProgramParamsNotificationTemplates`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `ProgramParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsProgramIndicators(_BaseModel):
    """OpenAPI schema `ProgramParamsProgramIndicators`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsProgramRuleVariables(_BaseModel):
    """OpenAPI schema `ProgramParamsProgramRuleVariables`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsProgramSections(_BaseModel):
    """OpenAPI schema `ProgramParamsProgramSections`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsProgramStages(_BaseModel):
    """OpenAPI schema `ProgramParamsProgramStages`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsTrackedEntityType(_BaseModel):
    """OpenAPI schema `ProgramParamsTrackedEntityType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParamsUserRoles(_BaseModel):
    """OpenAPI schema `ProgramParamsUserRoles`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramParams(_BaseModel):
    """OpenAPI schema `ProgramParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    accessLevel: AccessLevel | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombo: CategoryComboParams | None = None
    categoryMappings: list[ProgramCategoryMapping] | None = None
    code: str | None = None
    completeEventsExpiryDays: int | None = None
    created: datetime | None = None
    createdBy: ProgramParamsCreatedBy | None = None
    dataEntryForm: ProgramParamsDataEntryForm | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayEnrollmentDateLabel: str | None = None
    displayEnrollmentLabel: str | None = None
    displayEnrollmentsLabel: str | None = None
    displayEventLabel: str | None = None
    displayEventsLabel: str | None = None
    displayFollowUpLabel: str | None = None
    displayFormName: str | None = None
    displayFrontPageList: bool | None = None
    displayIncidentDate: bool | None = None
    displayIncidentDateLabel: str | None = None
    displayName: str | None = None
    displayNoteLabel: str | None = None
    displayOrgUnitLabel: str | None = None
    displayProgramStageLabel: str | None = None
    displayProgramStagesLabel: str | None = None
    displayRelationshipLabel: str | None = None
    displayShortName: str | None = None
    displayTrackedEntityAttributeLabel: str | None = None
    enableChangeLog: bool | None = None
    enrollmentCategoryCombo: CategoryComboParams | None = None
    enrollmentDateLabel: str | None = None
    enrollmentLabel: str | None = None
    enrollmentsLabel: str | None = None
    eventLabel: str | None = None
    eventsLabel: str | None = None
    expiryDays: int | None = None
    expiryPeriodType: (
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
    featureType: FeatureType | None = None
    followUpLabel: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    ignoreOverdueEvents: bool | None = None
    incidentDateLabel: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramParamsLastUpdatedBy | None = None
    maxTeiCountToReturn: int | None = None
    minAttributesRequiredToSearch: int | None = None
    name: str | None = None
    noteLabel: str | None = None
    notificationTemplates: list[ProgramParamsNotificationTemplates] | None = None
    onlyEnrollOnce: bool | None = None
    openDaysAfterCoEndDate: int | None = None
    orgUnitLabel: str | None = None
    organisationUnits: list[ProgramParamsOrganisationUnits] | None = None
    programIndicators: list[ProgramParamsProgramIndicators] | None = None
    programRuleVariables: list[ProgramParamsProgramRuleVariables] | None = None
    programSections: list[ProgramParamsProgramSections] | None = None
    programStageLabel: str | None = None
    programStages: list[ProgramParamsProgramStages] | None = None
    programStagesLabel: str | None = None
    programTrackedEntityAttributes: list[ProgramTrackedEntityAttributeParams] | None = None
    programType: ProgramType | None = None
    registration: bool | None = None
    relatedProgram: ProgramParams | None = None
    relationshipLabel: str | None = None
    selectEnrollmentDatesInFuture: bool | None = None
    selectIncidentDatesInFuture: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipOffline: bool | None = None
    style: ObjectStyle | None = None
    trackedEntityAttributeLabel: str | None = None
    trackedEntityType: ProgramParamsTrackedEntityType | None = None
    translations: list[Translation] | None = None
    useFirstStageDuringRegistration: bool | None = None
    userRoles: list[ProgramParamsUserRoles] | None = None
    version: int | None = None
    withoutRegistration: bool | None = None
