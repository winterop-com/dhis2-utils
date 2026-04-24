"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DeduplicationStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class PotentialDuplicateParamsCreatedBy(_BaseModel):
    """OpenAPI schema `PotentialDuplicateParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PotentialDuplicateParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `PotentialDuplicateParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PotentialDuplicateParams(_BaseModel):
    """OpenAPI schema `PotentialDuplicateParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PotentialDuplicateParamsCreatedBy | None = None
    createdByUserName: str | None = None
    displayName: str | None = None
    duplicate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PotentialDuplicateParamsLastUpdatedBy | None = None
    lastUpdatedByUserName: str | None = None
    name: str | None = None
    original: str | None = None
    sharing: Sharing | None = None
    status: DeduplicationStatus | None = None
    translations: list[Translation] | None = None
