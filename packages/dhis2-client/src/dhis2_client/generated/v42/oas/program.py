"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AccessLevel, FeatureType, ProgramType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_entry_form import DataEntryForm
    from .object_style import ObjectStyle
    from .program_category_mapping import ProgramCategoryMapping
    from .sharing import Sharing
    from .tracked_entity_type import TrackedEntityType
    from .translation import Translation
    from .user_dto import UserDto


class Program(_BaseModel):
    """OpenAPI schema `Program`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    accessLevel: AccessLevel
    attributeValues: list[AttributeValue] | None = None
    categoryCombo: BaseIdentifiableObject | None = None
    categoryMappings: list[ProgramCategoryMapping] | None = None
    code: str | None = None
    completeEventsExpiryDays: int
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataEntryForm: DataEntryForm | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayEnrollmentDateLabel: str | None = None
    displayEnrollmentLabel: str | None = None
    displayEventLabel: str | None = None
    displayFollowUpLabel: str | None = None
    displayFormName: str | None = None
    displayFrontPageList: bool | None = None
    displayIncidentDate: bool | None = None
    displayIncidentDateLabel: str | None = None
    displayName: str | None = None
    displayNoteLabel: str | None = None
    displayOrgUnitLabel: str | None = None
    displayProgramStageLabel: str | None = None
    displayRelationshipLabel: str | None = None
    displayShortName: str | None = None
    displayTrackedEntityAttributeLabel: str | None = None
    enrollmentDateLabel: str | None = None
    enrollmentLabel: str | None = None
    eventLabel: str | None = None
    expiryDays: int
    expiryPeriodType: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    featureType: FeatureType
    followUpLabel: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    ignoreOverdueEvents: bool | None = None
    incidentDateLabel: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    maxTeiCountToReturn: int
    minAttributesRequiredToSearch: int
    name: str | None = None
    noteLabel: str | None = None
    notificationTemplates: list[BaseIdentifiableObject] | None = None
    onlyEnrollOnce: bool | None = None
    openDaysAfterCoEndDate: int
    orgUnitLabel: str | None = None
    organisationUnits: list[BaseIdentifiableObject] | None = None
    programIndicators: list[BaseIdentifiableObject] | None = None
    programRuleVariables: list[BaseIdentifiableObject] | None = None
    programSections: list[BaseIdentifiableObject] | None = None
    programStageLabel: str | None = None
    programStages: list[BaseIdentifiableObject] | None = None
    programTrackedEntityAttributes: list[BaseIdentifiableObject] | None = None
    programType: ProgramType
    registration: bool | None = None
    relatedProgram: BaseIdentifiableObject | None = None
    relationshipLabel: str | None = None
    selectEnrollmentDatesInFuture: bool | None = None
    selectIncidentDatesInFuture: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipOffline: bool | None = None
    style: ObjectStyle | None = None
    trackedEntityAttributeLabel: str | None = None
    trackedEntityType: TrackedEntityType | None = None
    translations: list[Translation] | None = None
    useFirstStageDuringRegistration: bool | None = None
    userRoles: list[BaseIdentifiableObject] | None = None
    version: int
    withoutRegistration: bool | None = None
