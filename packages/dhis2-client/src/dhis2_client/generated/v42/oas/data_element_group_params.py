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
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataElementGroupParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParamsDataElements(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsDataElements`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParamsGroupSets(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsGroupSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParamsLegendSet(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParamsLegendSets(_BaseModel):
    """OpenAPI schema `DataElementGroupParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupParams(_BaseModel):
    """OpenAPI schema `DataElementGroupParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataElementGroupParamsCreatedBy | None = None
    dataElements: list[DataElementGroupParamsDataElements] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    groupSets: list[DataElementGroupParamsGroupSets] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementGroupParamsLastUpdatedBy | None = None
    legendSet: DataElementGroupParamsLegendSet | None = None
    legendSets: list[DataElementGroupParamsLegendSets] | None = None
    name: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
