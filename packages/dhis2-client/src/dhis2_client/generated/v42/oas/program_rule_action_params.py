"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ProgramRuleActionEvaluationEnvironment, ProgramRuleActionEvaluationTime, ProgramRuleActionType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_element_params import DataElementParams
    from .program_indicator_params import ProgramIndicatorParams
    from .program_rule_params import ProgramRuleParams
    from .program_stage_params import ProgramStageParams
    from .program_stage_section_params import ProgramStageSectionParams
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .translation import Translation


class ProgramRuleActionParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleActionParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleActionParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionParamsOption(_BaseModel):
    """OpenAPI schema `ProgramRuleActionParamsOption`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionParamsOptionGroup(_BaseModel):
    """OpenAPI schema `ProgramRuleActionParamsOptionGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionParams(_BaseModel):
    """OpenAPI schema `ProgramRuleActionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    content: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleActionParamsCreatedBy | None = None
    data: str | None = None
    dataElement: DataElementParams | None = None
    displayContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleActionParamsLastUpdatedBy | None = None
    location: str | None = None
    name: str | None = None
    option: ProgramRuleActionParamsOption | None = None
    optionGroup: ProgramRuleActionParamsOptionGroup | None = None
    programIndicator: ProgramIndicatorParams | None = None
    programRule: ProgramRuleParams | None = None
    programRuleActionEvaluationEnvironments: list[ProgramRuleActionEvaluationEnvironment] | None = None
    programRuleActionEvaluationTime: ProgramRuleActionEvaluationTime | None = None
    programRuleActionType: ProgramRuleActionType | None = None
    programStage: ProgramStageParams | None = None
    programStageSection: ProgramStageSectionParams | None = None
    sharing: Sharing | None = None
    templateUid: str | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
    translations: list[Translation] | None = None
