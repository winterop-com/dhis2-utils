"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .category_option_group_set_params import CategoryOptionGroupSetParams


class CategoryOptionGroupSetDimensionParamsCategoryOptionGroups(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupSetDimensionParamsCategoryOptionGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryOptionGroupSetDimensionParams(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupSetDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionGroupSet: CategoryOptionGroupSetParams | None = None
    categoryOptionGroups: list[CategoryOptionGroupSetDimensionParamsCategoryOptionGroups] | None = None
