"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class CategoryDimensionCategory(_BaseModel):
    """A UID reference to a Category  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryDimensionCategoryOptions(_BaseModel):
    """A UID reference to a CategoryOption  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryDimension(_BaseModel):
    """OpenAPI schema `CategoryDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    category: CategoryDimensionCategory | None = _Field(default=None, description="A UID reference to a Category  ")
    categoryOptions: list[CategoryDimensionCategoryOptions] | None = None
