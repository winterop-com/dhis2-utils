"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import CacheStrategy, SqlViewType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class SqlViewParamsCreatedBy(_BaseModel):
    """OpenAPI schema `SqlViewParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SqlViewParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `SqlViewParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SqlViewParams(_BaseModel):
    """OpenAPI schema `SqlViewParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    cacheStrategy: CacheStrategy | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: SqlViewParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SqlViewParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    sqlQuery: str | None = None
    translations: list[Translation] | None = None
    type: SqlViewType | None = None
    updateJobId: str | None = None
