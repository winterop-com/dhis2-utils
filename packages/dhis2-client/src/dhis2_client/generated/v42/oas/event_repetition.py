"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DimensionAttribute


class EventRepetition(_BaseModel):
    """OpenAPI schema `EventRepetition`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dimension: str | None = None
    indexes: list[int] | None = None
    parent: DimensionAttribute | None = None
    program: str | None = None
    programStage: str | None = None
