"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import In

if TYPE_CHECKING:
    from .schema_object import SchemaObject


class ParameterObject(_BaseModel):
    """OpenAPI schema `ParameterObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    ref: ParameterObject | None = _Field(default=None, alias="$ref")
    deprecated: bool | None = None
    description: str | None = None
    in_: In = _Field(alias="in")
    name: str | None = None
    required: bool | None = None
    schema_: SchemaObject | None = _Field(default=None, alias="schema")
    schema_default: Any | None = _Field(default=None, alias="schema.default")
    x_since: str | None = _Field(default=None, alias="x-since")
