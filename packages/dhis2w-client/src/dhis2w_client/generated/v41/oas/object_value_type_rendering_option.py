"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ObjectValueTypeRenderingOption(_BaseModel):
    """OpenAPI schema `ObjectValueTypeRenderingOption`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    clazz: str | None = None
    hasOptionSet: bool | None = None
    renderingTypes: list[str] | None = None
    valueType: str | None = None
