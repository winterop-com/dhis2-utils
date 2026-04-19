"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .data_element_params import DataElementParams
    from .program_stage_params import ProgramStageParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageDataElementParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageDataElementParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramStageDataElementParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementParams(_BaseModel):
    """OpenAPI schema `ProgramStageDataElementParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowFutureDate: bool | None = None
    allowProvidedElsewhere: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: ProgramStageDataElementParamsCreatedBy | None = None
    dataElement: DataElementParams | None = None
    displayInReports: bool | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageDataElementParamsLastUpdatedBy | None = None
    name: str | None = None
    programStage: ProgramStageParams | None = None
    renderOptionsAsRadio: bool | None = None
    renderType: Any | None = None
    sharing: Sharing | None = None
    skipAnalytics: bool | None = None
    skipSynchronization: bool | None = None
    sortOrder: int | None = None
    translations: list[Translation] | None = None
