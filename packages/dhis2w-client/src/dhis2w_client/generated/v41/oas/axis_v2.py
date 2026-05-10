"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .line import Line
    from .styled_object import StyledObject


class AxisV2(_BaseModel):
    """OpenAPI schema `AxisV2`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    baseLine: Line | None = None
    decimals: int | None = None
    index: int | None = None
    label: StyledObject | None = None
    maxValue: float | None = None
    minValue: float | None = None
    steps: int | None = None
    targetLine: Line | None = None
    title: StyledObject | None = None
    type: str | None = None
