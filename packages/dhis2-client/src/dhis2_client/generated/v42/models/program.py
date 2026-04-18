"""Generated Program model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Program(BaseModel):
    """DHIS2 Program - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/programs.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accessLevel: str | None = None

    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")

    categoryCombo: Reference | None = Field(default=None, description="Reference to CategoryCombo.")

    categoryMappings: list[Any] | None = Field(
        default=None, description="Collection of ProgramCategoryMapping. Length/value max=255."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    completeEventsExpiryDays: int | None = Field(default=None, description="Length/value max=2147483647.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    dataEntryForm: Reference | None = Field(default=None, description="Reference to DataEntryForm.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayEnrollmentDateLabel: str | None = Field(default=None, description="Read-only.")

    displayEnrollmentLabel: str | None = Field(default=None, description="Read-only.")

    displayEventLabel: str | None = Field(default=None, description="Read-only.")

    displayFollowUpLabel: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayFrontPageList: bool | None = None

    displayIncidentDate: bool | None = None

    displayIncidentDateLabel: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayNoteLabel: str | None = Field(default=None, description="Read-only.")

    displayOrgUnitLabel: str | None = Field(default=None, description="Read-only.")

    displayProgramStageLabel: str | None = Field(default=None, description="Read-only.")

    displayRelationshipLabel: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    displayTrackedEntityAttributeLabel: str | None = Field(default=None, description="Read-only.")

    enrollmentDateLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    enrollmentLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    eventLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    expiryDays: int | None = Field(default=None, description="Length/value max=2147483647.")

    expiryPeriodType: Any | None = Field(default=None, description="Reference to PeriodType. Length/value max=255.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    featureType: str | None = None

    followUpLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    ignoreOverdueEvents: bool | None = None

    incidentDateLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    maxTeiCountToReturn: int | None = Field(default=None, description="Length/value max=2147483647.")

    minAttributesRequiredToSearch: int | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    noteLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    notificationTemplates: list[Any] | None = Field(
        default=None, description="Collection of ProgramNotificationTemplate."
    )

    onlyEnrollOnce: bool | None = None

    openDaysAfterCoEndDate: int | None = Field(default=None, description="Length/value max=2147483647.")

    orgUnitLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    programAttributes: list[Any] | None = Field(
        default=None, description="Collection of ProgramTrackedEntityAttribute."
    )

    programIndicators: list[Any] | None = Field(
        default=None, description="Collection of ProgramIndicator. Read-only (inverse side)."
    )

    programRuleVariables: list[Any] | None = Field(
        default=None, description="Collection of ProgramRuleVariable. Read-only (inverse side)."
    )

    programSections: list[Any] | None = Field(default=None, description="Collection of ProgramSection.")

    programStageLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    programStages: list[Any] | None = Field(default=None, description="Collection of ProgramStage.")

    programType: str | None = None

    registration: bool | None = Field(default=None, description="Read-only.")

    relatedProgram: Reference | None = Field(default=None, description="Reference to Program.")

    relationshipLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    selectEnrollmentDatesInFuture: bool | None = None

    selectIncidentDatesInFuture: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")

    skipOffline: bool | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    trackedEntityAttributeLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    trackedEntityType: Reference | None = Field(default=None, description="Reference to TrackedEntityType.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    useFirstStageDuringRegistration: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userRoles: list[Any] | None = Field(default=None, description="Collection of UserRole. Read-only (inverse side).")

    version: int | None = Field(default=None, description="Length/value max=2147483647.")

    withoutRegistration: bool | None = Field(default=None, description="Read-only.")
