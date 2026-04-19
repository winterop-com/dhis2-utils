"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .data_element_group_set_params import DataElementGroupSetParams


class DataElementGroupSetDimensionParamsDataElementGroups(_BaseModel):
    """OpenAPI schema `DataElementGroupSetDimensionParamsDataElementGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataElementGroupSetDimensionParams(_BaseModel):
    """OpenAPI schema `DataElementGroupSetDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElementGroupSet: DataElementGroupSetParams | None = None
    dataElementGroups: list[DataElementGroupSetDimensionParamsDataElementGroups] | None = None
