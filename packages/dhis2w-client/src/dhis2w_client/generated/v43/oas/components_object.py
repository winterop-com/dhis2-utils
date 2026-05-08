"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .parameter_object import ParameterObject
    from .schema_object import SchemaObject


class ComponentsObject(_BaseModel):
    """OpenAPI schema `ComponentsObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    parameters: dict[str, ParameterObject] | None = None
    schemas: dict[str, SchemaObject] | None = None
