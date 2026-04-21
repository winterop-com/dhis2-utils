"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import FeatureType, FormType, ValidationStrategy

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_element import DataElement
    from .data_entry_form import DataEntryForm
    from .identifiable_object import IdentifiableObject
    from .object_style import ObjectStyle
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class ProgramStage(_BaseModel):
    """OpenAPI schema `ProgramStage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    allowGenerateNextVisit: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    autoGenerateEvent: bool | None = None
    blockEntryForm: bool | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataEntryForm: DataEntryForm | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayDueDateLabel: str | None = None
    displayEventLabel: str | None = None
    displayEventsLabel: str | None = None
    displayExecutionDateLabel: str | None = None
    displayFormName: str | None = None
    displayGenerateEventBox: bool | None = None
    displayName: str | None = None
    displayProgramStageLabel: str | None = None
    displayShortName: str | None = None
    dueDateLabel: str | None = None
    enableUserAssignment: bool | None = None
    eventLabel: str | None = None
    eventsLabel: str | None = None
    executionDateLabel: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    featureType: FeatureType | None = None
    formName: str | None = None
    formType: FormType | None = None
    generatedByEnrollmentDate: bool | None = None
    hideDueDate: bool | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    minDaysFromStart: int | None = None
    name: str | None = None
    nextScheduleDate: DataElement | None = None
    notificationTemplates: list[BaseIdentifiableObject] | None = None
    openAfterEnrollment: bool | None = None
    periodType: str | None = None
    preGenerateUID: bool | None = None
    program: IdentifiableObject | None = None
    programStageDataElements: list[BaseIdentifiableObject] | None = None
    programStageLabel: str | None = None
    programStageSections: list[BaseIdentifiableObject] | None = None
    referral: bool | None = None
    remindCompleted: bool | None = None
    repeatable: bool | None = None
    reportDateToUse: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    sortOrder: int | None = None
    standardInterval: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    validationStrategy: ValidationStrategy | None = None
