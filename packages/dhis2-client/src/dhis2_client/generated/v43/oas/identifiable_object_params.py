"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_values import AttributeValues
    from .sharing import Sharing
    from .translation import Translation


class IdentifiableObjectParamsCreatedBy(_BaseModel):
    """OpenAPI schema `IdentifiableObjectParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IdentifiableObjectParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `IdentifiableObjectParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IdentifiableObjectParams(_BaseModel):
    """OpenAPI schema `IdentifiableObjectParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: AttributeValues | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IdentifiableObjectParamsCreatedBy | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IdentifiableObjectParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
