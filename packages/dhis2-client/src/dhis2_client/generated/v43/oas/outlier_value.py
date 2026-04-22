"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class OutlierValue(_BaseModel):
    """OpenAPI schema `OutlierValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    absDev: float | None = None
    aoc: str | None = None
    aocName: str | None = None
    coc: str | None = None
    cocName: str | None = None
    de: str | None = None
    deName: str | None = None
    followup: bool | None = None
    lastUpdated: datetime | None = None
    lowerBound: float | None = None
    mean: float | None = None
    median: float | None = None
    ou: str | None = None
    ouName: str | None = None
    pe: str | None = None
    rawValue: str | None = None
    stdDev: float | None = None
    upperBound: float | None = None
    value: float | None = None
    zScore: float | None = None
