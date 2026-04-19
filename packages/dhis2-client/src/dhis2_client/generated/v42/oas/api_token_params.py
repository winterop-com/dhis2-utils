"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ApiTokenType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .ip_allowed_list import IpAllowedList
    from .method_allowed_list import MethodAllowedList
    from .referer_allowed_list import RefererAllowedList
    from .sharing import Sharing
    from .translation import Translation


class ApiTokenParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ApiTokenParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApiTokenParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ApiTokenParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ApiTokenParams(_BaseModel):
    """OpenAPI schema `ApiTokenParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    attributes: list[IpAllowedList | RefererAllowedList | MethodAllowedList] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ApiTokenParamsCreatedBy | None = None
    displayName: str | None = None
    expire: int | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ApiTokenParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: ApiTokenType | None = None
    version: int | None = None
