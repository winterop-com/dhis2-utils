"""Generated Program model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Program(BaseModel):
    """DHIS2 Program resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    accessLevel: str | None = None

    attributeValues: Any | None = None

    categoryCombo: Reference | None = None

    categoryMappings: list[Any] | None = None

    code: str | None = None

    completeEventsExpiryDays: int | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataEntryForm: Reference | None = None

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

    enrollmentCategoryCombo: Reference | None = None

    enrollmentDateLabel: str | None = None

    enrollmentLabel: str | None = None

    enrollmentsLabel: str | None = None

    eventLabel: str | None = None

    eventsLabel: str | None = None

    expiryDays: int | None = None

    expiryPeriodType: Any | None = None

    featureType: str | None = None

    followUpLabel: str | None = None

    formName: str | None = None

    href: str | None = None

    ignoreOverdueEvents: bool | None = None

    incidentDateLabel: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    maxTeiCountToReturn: int | None = None

    minAttributesRequiredToSearch: int | None = None

    name: str | None = None

    noteLabel: str | None = None

    notificationTemplates: list[Any] | None = None

    onlyEnrollOnce: bool | None = None

    openDaysAfterCoEndDate: int | None = None

    orgUnitLabel: str | None = None

    organisationUnits: list[Any] | None = None

    programAttributes: list[Any] | None = None

    programIndicators: list[Any] | None = None

    programRuleVariables: list[Any] | None = None

    programSections: list[Any] | None = None

    programStageLabel: str | None = None

    programStages: list[Any] | None = None

    programStagesLabel: str | None = None

    programType: str | None = None

    registration: bool | None = None

    relatedProgram: Reference | None = None

    relationshipLabel: str | None = None

    selectEnrollmentDatesInFuture: bool | None = None

    selectIncidentDatesInFuture: bool | None = None

    sharing: Any | None = None

    shortName: str | None = None

    skipOffline: bool | None = None

    style: Any | None = None

    trackedEntityAttributeLabel: str | None = None

    trackedEntityType: Reference | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    useFirstStageDuringRegistration: bool | None = None

    user: Reference | None = None

    userRoles: list[Any] | None = None

    version: int | None = None

    withoutRegistration: bool | None = None
