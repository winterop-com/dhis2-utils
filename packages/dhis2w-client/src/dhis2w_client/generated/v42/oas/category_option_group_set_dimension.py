"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .category_option_group import CategoryOptionGroup


class CategoryOptionGroupSetDimension(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryOptionGroupSet: BaseIdentifiableObject | None = None
    categoryOptionGroups: list[CategoryOptionGroup] | None = None
