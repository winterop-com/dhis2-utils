"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .object_style import ObjectStyle
    from .program_stage_data_element import ProgramStageDataElement
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataEntryForm(_BaseModel):
    """A UID reference to a DataEntryForm  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageNextScheduleDate(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageNotificationTemplates(_BaseModel):
    """A UID reference to a ProgramNotificationTemplate  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageProgramStageSections(_BaseModel):
    """A UID reference to a ProgramStageSection  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


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
    createdBy: ProgramStageCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataEntryForm: ProgramStageDataEntryForm | None = _Field(
        default=None, description="A UID reference to a DataEntryForm  "
    )
    description: str | None = None
    displayDescription: str | None = None
    displayDueDateLabel: str | None = None
    displayEventLabel: str | None = None
    displayExecutionDateLabel: str | None = None
    displayFormName: str | None = None
    displayGenerateEventBox: bool | None = None
    displayName: str | None = None
    displayProgramStageLabel: str | None = None
    displayShortName: str | None = None
    dueDateLabel: str | None = None
    enableUserAssignment: bool | None = None
    eventLabel: str | None = None
    executionDateLabel: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    featureType: str | None = None
    formName: str | None = None
    formType: str | None = None
    generatedByEnrollmentDate: bool | None = None
    hideDueDate: bool | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    minDaysFromStart: int | None = None
    name: str | None = None
    nextScheduleDate: ProgramStageNextScheduleDate | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    notificationTemplates: list[ProgramStageNotificationTemplates] | None = None
    openAfterEnrollment: bool | None = None
    periodType: str | None = None
    preGenerateUID: bool | None = None
    program: ProgramStageProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStageDataElements: list[ProgramStageDataElement] | None = None
    programStageLabel: str | None = None
    programStageSections: list[ProgramStageProgramStageSections] | None = None
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
    user: ProgramStageUser | None = _Field(default=None, description="A UID reference to a User  ")
    validationStrategy: str | None = None
