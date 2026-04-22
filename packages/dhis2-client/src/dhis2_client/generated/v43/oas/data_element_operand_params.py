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
    from .category_option_combo_params import CategoryOptionComboParams
    from .data_element_params import DataElementParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataElementOperandParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataElementOperandParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataElementOperandParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandParamsLegendSet(_BaseModel):
    """OpenAPI schema `DataElementOperandParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandParamsLegendSets(_BaseModel):
    """OpenAPI schema `DataElementOperandParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementOperandParams(_BaseModel):
    """OpenAPI schema `DataElementOperandParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: CategoryOptionComboParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryOptionCombo: CategoryOptionComboParams | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataElementOperandParamsCreatedBy | None = None
    dataElement: DataElementParams | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataElementOperandParamsLastUpdatedBy | None = None
    legendSet: DataElementOperandParamsLegendSet | None = None
    legendSets: list[DataElementOperandParamsLegendSets] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
