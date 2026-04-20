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


class OrganisationUnitLevelParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitLevelParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitLevelParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitLevelParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitLevelParams(_BaseModel):
    """OpenAPI schema `OrganisationUnitLevelParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OrganisationUnitLevelParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OrganisationUnitLevelParamsLastUpdatedBy | None = None
    level: int | None = None
    name: str | None = None
    offlineLevels: int | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
