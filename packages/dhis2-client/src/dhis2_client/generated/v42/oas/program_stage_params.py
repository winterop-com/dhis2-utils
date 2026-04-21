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
    from .attribute_value_params import AttributeValueParams
    from .object_style import ObjectStyle
    from .program_params import ProgramParams
    from .program_stage_data_element_params import ProgramStageDataElementParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParamsDataEntryForm(_BaseModel):
    """OpenAPI schema `ProgramStageParamsDataEntryForm`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParamsNextScheduleDate(_BaseModel):
    """OpenAPI schema `ProgramStageParamsNextScheduleDate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParamsNotificationTemplates(_BaseModel):
    """OpenAPI schema `ProgramStageParamsNotificationTemplates`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParamsProgramStageSections(_BaseModel):
    """OpenAPI schema `ProgramStageParamsProgramStageSections`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageParams(_BaseModel):
    """OpenAPI schema `ProgramStageParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowGenerateNextVisit: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    autoGenerateEvent: bool | None = None
    blockEntryForm: bool | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramStageParamsCreatedBy | None = None
    dataEntryForm: ProgramStageParamsDataEntryForm | None = None
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
    featureType: FeatureType | None = None
    formName: str | None = None
    formType: FormType | None = None
    generatedByEnrollmentDate: bool | None = None
    hideDueDate: bool | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageParamsLastUpdatedBy | None = None
    minDaysFromStart: int | None = None
    name: str | None = None
    nextScheduleDate: ProgramStageParamsNextScheduleDate | None = None
    notificationTemplates: list[ProgramStageParamsNotificationTemplates] | None = None
    openAfterEnrollment: bool | None = None
    periodType: str | None = None
    preGenerateUID: bool | None = None
    program: ProgramParams | None = None
    programStageDataElements: list[ProgramStageDataElementParams] | None = None
    programStageLabel: str | None = None
    programStageSections: list[ProgramStageParamsProgramStageSections] | None = None
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
