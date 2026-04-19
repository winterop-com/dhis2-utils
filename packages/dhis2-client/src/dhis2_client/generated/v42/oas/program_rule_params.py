"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramRuleParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramRuleParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleParamsProgramRuleActions(_BaseModel):
    """OpenAPI schema `ProgramRuleParamsProgramRuleActions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleParams(_BaseModel):
    """OpenAPI schema `ProgramRuleParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    condition: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleParamsLastUpdatedBy | None = None
    name: str | None = None
    priority: int | None = None
    program: ProgramParams | None = None
    programRuleActions: list[ProgramRuleParamsProgramRuleActions] | None = None
    programStage: ProgramStageParams | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
