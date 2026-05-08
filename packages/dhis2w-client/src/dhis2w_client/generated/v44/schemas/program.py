"""Generated Program model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AccessLevel, FeatureType, PeriodType, ProgramType


class Program(BaseModel):
    """Generated model for DHIS2 `Program`.

    DHIS2 Program - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/programs.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    accessLevel: AccessLevel | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    categoryCombo: Reference | None = Field(
        default=None, description="Reference to CategoryCombo. Read-only (inverse side)."
    )
    categoryMappings: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    code: str | None = None
    completeEventsExpiryDays: int | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataEntryForm: Reference | None = Field(
        default=None, description="Reference to DataEntryForm. Read-only (inverse side)."
    )
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
    enrollmentCategoryCombo: Reference | None = Field(
        default=None, description="Reference to CategoryCombo. Read-only (inverse side)."
    )
    enrollmentDateLabel: str | None = None
    enrollmentLabel: str | None = None
    enrollmentsLabel: str | None = None
    eventLabel: str | None = None
    eventsLabel: str | None = None
    expiryDays: int | None = None
    expiryPeriodType: PeriodType | None = Field(
        default=None, description="Reference to PeriodType. Read-only (inverse side)."
    )
    featureType: FeatureType | None = None
    followUpLabel: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    ignoreOverdueEvents: bool | None = None
    incidentDateLabel: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    maxTeiCountToReturn: int | None = None
    minAttributesRequiredToSearch: int | None = None
    name: str | None = None
    noteLabel: str | None = None
    notificationTemplates: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    onlyEnrollOnce: bool | None = None
    openDaysAfterCoEndDate: int | None = None
    orgUnitLabel: str | None = None
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    programIndicators: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    programRuleVariables: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    programSections: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    programStageLabel: str | None = None
    programStages: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    programStagesLabel: str | None = None
    programTrackedEntityAttributes: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    programType: ProgramType | None = None
    registration: bool | None = None
    relatedProgram: Reference | None = Field(
        default=None, description="Reference to Program. Read-only (inverse side)."
    )
    relationshipLabel: str | None = None
    selectEnrollmentDatesInFuture: bool | None = None
    selectIncidentDatesInFuture: bool | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    skipOffline: bool | None = None
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")
    trackedEntityAttributeLabel: str | None = None
    trackedEntityType: Reference | None = Field(
        default=None, description="Reference to TrackedEntityType. Read-only (inverse side)."
    )
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    useFirstStageDuringRegistration: bool | None = None
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userRoles: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    version: int | None = None
    withoutRegistration: bool | None = None
