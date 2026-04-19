"""Generated Program model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AccessLevel, FeatureType, PeriodType, ProgramType
from .attribute_value import AttributeValue


class Program(BaseModel):
    """Generated model for DHIS2 `Program`.

    DHIS2 Program - persisted metadata (generated from /api/schemas at DHIS2 v41).


    API endpoint: /api/programs.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accessLevel: AccessLevel | None = None

    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    categoryCombo: Reference | None = Field(default=None, description="Reference to CategoryCombo.")

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

    expiryPeriodType: PeriodType | None = Field(
        default=None, description="Reference to PeriodType. Length/value max=255."
    )

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    featureType: FeatureType | None = None

    followUpLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

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

    programIndicators: list[Any] | None = Field(
        default=None, description="Collection of ProgramIndicator. Read-only (inverse side)."
    )

    programRuleVariables: list[Any] | None = Field(
        default=None, description="Collection of ProgramRuleVariable. Read-only (inverse side)."
    )

    programSections: list[Any] | None = Field(default=None, description="Collection of ProgramSection.")

    programStageLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    programStages: list[Any] | None = Field(default=None, description="Collection of ProgramStage.")

    programTrackedEntityAttributes: list[Any] | None = Field(
        default=None, description="Collection of ProgramTrackedEntityAttribute."
    )

    programType: ProgramType | None = None

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

    useFirstStageDuringRegistration: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userRoles: list[Any] | None = Field(default=None, description="Collection of UserRole. Read-only (inverse side).")

    version: int | None = Field(default=None, description="Length/value max=2147483647.")

    withoutRegistration: bool | None = Field(default=None, description="Read-only.")
