"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ValueTypeRenderingType


class ValueTypeRenderingObject(_BaseModel):
    """OpenAPI schema `ValueTypeRenderingObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    decimalPoints: int | None = None
    max: int | None = None
    min: int | None = None
    step: int | None = None
    type: ValueTypeRenderingType | None = None
