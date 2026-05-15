"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class EventRepetition(_BaseModel):
    """OpenAPI schema `EventRepetition`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dimension: str | None = None
    indexes: list[int] | None = None
    parent: Literal["COLUMN", "ROW", "FILTER"] | None = None
    program: str | None = None
    programStage: str | None = None
