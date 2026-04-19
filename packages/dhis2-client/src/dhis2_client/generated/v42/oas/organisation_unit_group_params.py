"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, FeatureType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class OrganisationUnitGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParamsGroupSets(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsGroupSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParamsLegendSet(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParamsLegendSets(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupParams(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    color: str | None = None
    created: datetime | None = None
    createdBy: OrganisationUnitGroupParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    featureType: FeatureType
    formName: str | None = None
    geometry: dict[str, Any] | None = None
    groupSets: list[OrganisationUnitGroupParamsGroupSets] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OrganisationUnitGroupParamsLastUpdatedBy | None = None
    legendSet: OrganisationUnitGroupParamsLegendSet | None = None
    legendSets: list[OrganisationUnitGroupParamsLegendSets] | None = None
    name: str | None = None
    organisationUnits: list[OrganisationUnitGroupParamsOrganisationUnits] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    symbol: str | None = None
    translations: list[Translation] | None = None
