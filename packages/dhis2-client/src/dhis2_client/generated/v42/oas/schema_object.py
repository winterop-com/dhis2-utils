"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class SchemaObject(_BaseModel):
    """OpenAPI schema `SchemaObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    ref: Any | None = _Field(default=None, alias="$ref")
    additionalProperties: SchemaObject | None = None
    allOf: list[Any] | None = None
    anyOf: list[Any] | None = None
    default: Any | None = None
    description: str | None = None
    enum: Any | None = None
    format: str | None = None
    items: SchemaObject | None = None
    maxLength: int | None = None
    minLength: int | None = None
    not_: SchemaObject | None = _Field(default=None, alias="not")
    oneOf: list[Any] | None = None
    pattern: str | None = None
    properties: dict[str, SchemaObject] | None = None
    readOnly: bool | None = None
    required: list[str] | None = None
    type: str | None = None
    x_kind: str | None = _Field(default=None, alias="x-kind")
    x_since: str | None = _Field(default=None, alias="x-since")
