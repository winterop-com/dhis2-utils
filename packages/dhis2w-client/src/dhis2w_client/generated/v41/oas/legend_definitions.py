"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class LegendDefinitionsSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class LegendDefinitions(_BaseModel):
    """OpenAPI schema `LegendDefinitions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    set: LegendDefinitionsSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    showKey: bool | None = None
    strategy: Literal["FIXED", "BY_DATA_ITEM"] | None = None
    style: Literal["FILL", "TEXT"] | None = None
