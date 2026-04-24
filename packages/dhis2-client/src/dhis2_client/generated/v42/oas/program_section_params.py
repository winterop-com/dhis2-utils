"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .object_style import ObjectStyle
    from .program_params import ProgramParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramSectionParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramSectionParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramSectionParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramSectionParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramSectionParamsTrackedEntityAttributes(_BaseModel):
    """OpenAPI schema `ProgramSectionParamsTrackedEntityAttributes`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramSectionParams(_BaseModel):
    """OpenAPI schema `ProgramSectionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramSectionParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramSectionParamsLastUpdatedBy | None = None
    name: str | None = None
    program: ProgramParams | None = None
    renderType: Any | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    sortOrder: int | None = None
    style: ObjectStyle | None = None
    trackedEntityAttributes: list[ProgramSectionParamsTrackedEntityAttributes] | None = None
    translations: list[Translation] | None = None
