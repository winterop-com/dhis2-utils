"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DataElementDomain, ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_combo_params import CategoryComboParams
    from .data_set_element_params import DataSetElementParams
    from .file_type_value_options import FileTypeValueOptions
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataElementParamsCommentOptionSet(_BaseModel):
    """OpenAPI schema `DataElementParamsCommentOptionSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataElementParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsDataElementGroups(_BaseModel):
    """OpenAPI schema `DataElementParamsDataElementGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataElementParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsLegendSet(_BaseModel):
    """OpenAPI schema `DataElementParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsLegendSets(_BaseModel):
    """OpenAPI schema `DataElementParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParamsOptionSet(_BaseModel):
    """OpenAPI schema `DataElementParamsOptionSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataElementParams(_BaseModel):
    """OpenAPI schema `DataElementParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationLevels: list[int] | None = None
    aggregationType: AggregationType
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombo: CategoryComboParams | None = None
    code: str | None = None
    commentOptionSet: DataElementParamsCommentOptionSet | None = None
    created: datetime | None = None
    createdBy: DataElementParamsCreatedBy | None = None
    dataElementGroups: list[DataElementParamsDataElementGroups] | None = None
    dataSetElements: list[DataSetElementParams] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    domainType: DataElementDomain
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementParamsLastUpdatedBy | None = None
    legendSet: DataElementParamsLegendSet | None = None
    legendSets: list[DataElementParamsLegendSets] | None = None
    name: str | None = None
    optionSet: DataElementParamsOptionSet | None = None
    optionSetValue: bool | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
    valueType: ValueType
    valueTypeOptions: FileTypeValueOptions | None = None
    zeroIsSignificant: bool | None = None
