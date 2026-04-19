"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .program_stage_query_criteria import ProgramStageQueryCriteria
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageWorkingListParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageWorkingListParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramStageWorkingListParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageWorkingListParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramStageWorkingListParams(_BaseModel):
    """OpenAPI schema `ProgramStageWorkingListParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramStageWorkingListParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageWorkingListParamsLastUpdatedBy | None = None
    name: str | None = None
    program: ProgramParams | None = None
    programStage: ProgramStageParams | None = None
    programStageQueryCriteria: ProgramStageQueryCriteria | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
