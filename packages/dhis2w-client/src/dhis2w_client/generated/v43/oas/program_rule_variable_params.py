"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ProgramRuleVariableSourceType, ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_element_params import DataElementParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .translation import Translation


class ProgramRuleVariableParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleVariableParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleVariableParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableParams(_BaseModel):
    """OpenAPI schema `ProgramRuleVariableParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleVariableParamsCreatedBy | None = None
    dataElement: DataElementParams | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleVariableParamsLastUpdatedBy | None = None
    name: str | None = None
    program: ProgramParams | None = None
    programRuleVariableSourceType: ProgramRuleVariableSourceType | None = None
    programStage: ProgramStageParams | None = None
    sharing: Sharing | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
    translations: list[Translation] | None = None
    useCodeForOptionSet: bool | None = None
    valueType: ValueType | None = None
