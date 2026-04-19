"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class DocumentParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DocumentParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DocumentParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DocumentParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DocumentParams(_BaseModel):
    """OpenAPI schema `DocumentParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attachment: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    contentType: str | None = None
    created: datetime | None = None
    createdBy: DocumentParamsCreatedBy | None = None
    displayName: str | None = None
    external: bool | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DocumentParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    url: str | None = None
