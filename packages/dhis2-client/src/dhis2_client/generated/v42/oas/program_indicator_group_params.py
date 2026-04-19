"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramIndicatorGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramIndicatorGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramIndicatorGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorGroupParamsProgramIndicators(_BaseModel):
    """OpenAPI schema `ProgramIndicatorGroupParamsProgramIndicators`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorGroupParams(_BaseModel):
    """OpenAPI schema `ProgramIndicatorGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramIndicatorGroupParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramIndicatorGroupParamsLastUpdatedBy | None = None
    name: str | None = None
    programIndicators: list[ProgramIndicatorGroupParamsProgramIndicators] | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
