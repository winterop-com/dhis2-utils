"""Generated Program model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AccessLevel, FeatureType, ProgramType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Program(BaseModel):
    """DHIS2 Program - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/programs.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accessLevel: AccessLevel | None = None

    attributeValues: list[Any] | None = Field(
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

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayFrontPageList: bool | None = None

    displayIncidentDate: bool | None = None

    displayIncidentDateLabel: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    enrollmentDateLabel: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    expiryDays: int | None = Field(default=None, description="Length/value max=2147483647.")

    expiryPeriodType: Any | None = Field(default=None, description="Reference to PeriodType. Length/value max=255.")

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    featureType: FeatureType | None = None

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

    notificationTemplates: list[Any] | None = Field(
        default=None, description="Collection of ProgramNotificationTemplate."
    )

    onlyEnrollOnce: bool | None = None

    openDaysAfterCoEndDate: int | None = Field(default=None, description="Length/value max=2147483647.")

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    programIndicators: list[Any] | None = Field(
        default=None, description="Collection of ProgramIndicator. Read-only (inverse side)."
    )

    programRuleVariables: list[Any] | None = Field(
        default=None, description="Collection of ProgramRuleVariable. Read-only (inverse side)."
    )

    programSections: list[Any] | None = Field(default=None, description="Collection of ProgramSection.")

    programStages: list[Any] | None = Field(default=None, description="Collection of ProgramStage.")

    programTrackedEntityAttributes: list[Any] | None = Field(
        default=None, description="Collection of ProgramTrackedEntityAttribute."
    )

    programType: ProgramType | None = None

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    registration: bool | None = Field(default=None, description="Read-only.")

    relatedProgram: Reference | None = Field(default=None, description="Reference to Program.")

    selectEnrollmentDatesInFuture: bool | None = None

    selectIncidentDatesInFuture: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")

    skipOffline: bool | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    trackedEntityType: Reference | None = Field(default=None, description="Reference to TrackedEntityType.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    useFirstStageDuringRegistration: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )

    userRoles: list[Any] | None = Field(default=None, description="Collection of UserRole. Read-only (inverse side).")

    version: int | None = Field(default=None, description="Length/value max=2147483647.")

    withoutRegistration: bool | None = Field(default=None, description="Read-only.")
