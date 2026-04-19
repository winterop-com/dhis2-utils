"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .category_params import CategoryParams


class CategoryDimensionParamsCategoryOptions(_BaseModel):
    """OpenAPI schema `CategoryDimensionParamsCategoryOptions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class CategoryDimensionParams(_BaseModel):
    """OpenAPI schema `CategoryDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    category: CategoryParams | None = None
    categoryOptions: list[CategoryDimensionParamsCategoryOptions] | None = None
