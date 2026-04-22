"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_element_group import DataElementGroup


class DataElementGroupSetDimension(_BaseModel):
    """OpenAPI schema `DataElementGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElementGroupSet: BaseIdentifiableObject | None = None
    dataElementGroups: list[DataElementGroup] | None = None
