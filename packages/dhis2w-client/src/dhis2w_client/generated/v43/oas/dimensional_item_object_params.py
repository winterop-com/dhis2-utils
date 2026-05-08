"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_values import AttributeValues
    from .sharing import Sharing
    from .translation import Translation


class DimensionalItemObjectParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DimensionalItemObjectParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DimensionalItemObjectParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DimensionalItemObjectParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DimensionalItemObjectParams(_BaseModel):
    """OpenAPI schema `DimensionalItemObjectParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: AttributeValues | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DimensionalItemObjectParamsCreatedBy | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DimensionalItemObjectParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
