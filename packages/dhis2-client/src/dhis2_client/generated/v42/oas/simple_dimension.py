"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DimensionAttribute


class SimpleDimension(_BaseModel):
    """OpenAPI schema `SimpleDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dimension: str
    parent: DimensionAttribute
    program: str | None = None
    programStage: str | None = None
    values: list[str]
