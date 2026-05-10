"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class CategoryOptionGroupSetDimensionCategoryOptionGroupSet(_BaseModel):
    """A UID reference to a CategoryOptionGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupSetDimensionCategoryOptionGroups(_BaseModel):
    """A UID reference to a CategoryOptionGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class CategoryOptionGroupSetDimension(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionGroupSet: CategoryOptionGroupSetDimensionCategoryOptionGroupSet | None = _Field(
        default=None, description="A UID reference to a CategoryOptionGroupSet  "
    )
    categoryOptionGroups: list[CategoryOptionGroupSetDimensionCategoryOptionGroups] | None = None
