"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class OptionSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OptionSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OptionSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionSetParamsOptions(_BaseModel):
    """OpenAPI schema `OptionSetParamsOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OptionSetParams(_BaseModel):
    """OpenAPI schema `OptionSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OptionSetParamsCreatedBy | None = None
    description: str | None = None
    displayName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OptionSetParamsLastUpdatedBy | None = None
    name: str | None = None
    options: list[OptionSetParamsOptions] | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
    version: int | None = None
