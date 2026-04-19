"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ValueType


class GridHeader(_BaseModel):
    """OpenAPI schema `GridHeader`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    column: str | None = None
    hidden: bool | None = None
    legendSet: str | None = None
    meta: bool | None = None
    name: str | None = None
    optionSet: str | None = None
    programStage: str | None = None
    repeatableStageParams: str | None = None
    stageOffset: int | None = None
    type: str | None = None
    valueType: ValueType
