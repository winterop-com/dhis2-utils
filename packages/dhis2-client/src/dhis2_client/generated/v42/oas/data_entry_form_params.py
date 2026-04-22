"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import DisplayDensity

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class DataEntryFormParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataEntryFormParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataEntryFormParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataEntryFormParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataEntryFormParams(_BaseModel):
    """OpenAPI schema `DataEntryFormParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataEntryFormParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    format: int | None = None
    htmlCode: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataEntryFormParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    style: DisplayDensity | None = None
    translations: list[Translation] | None = None
