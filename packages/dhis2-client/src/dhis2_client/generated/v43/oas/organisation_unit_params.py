"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class OrganisationUnitParamsAncestors(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsAncestors`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsChildren(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsChildren`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsDataSets(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsDataSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsImage(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsImage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsLegendSet(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsLegendSets(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParamsPrograms(_BaseModel):
    """OpenAPI schema `OrganisationUnitParamsPrograms`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParams(_BaseModel):
    """OpenAPI schema `OrganisationUnitParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    address: str | None = None
    aggregationType: AggregationType | None = None
    ancestors: list[OrganisationUnitParamsAncestors] | None = None
    attributeValues: list[AttributeValueParams] | None = None
    children: list[OrganisationUnitParamsChildren] | None = None
    closedDate: datetime | None = None
    code: str | None = None
    comment: str | None = None
    contactPerson: str | None = None
    created: datetime | None = None
    createdBy: OrganisationUnitParamsCreatedBy | None = None
    dataSets: list[OrganisationUnitParamsDataSets] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    email: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    geometry: dict[str, Any] | None = None
    id: str | None = None
    image: OrganisationUnitParamsImage | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OrganisationUnitParamsLastUpdatedBy | None = None
    leaf: bool | None = None
    legendSet: OrganisationUnitParamsLegendSet | None = None
    legendSets: list[OrganisationUnitParamsLegendSets] | None = None
    memberCount: int | None = None
    name: str | None = None
    openingDate: datetime | None = None
    organisationUnitGroups: list[OrganisationUnitParamsOrganisationUnitGroups] | None = None
    parent: OrganisationUnitParams | None = None
    path: str | None = None
    phoneNumber: str | None = None
    programs: list[OrganisationUnitParamsPrograms] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    type: str | None = None
    url: str | None = None
    users: list[UserDto] | None = None
