"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class FollowupValue(_BaseModel):
    """OpenAPI schema `FollowupValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aoc: str | None = None
    aocName: str | None = None
    coc: str | None = None
    cocName: str | None = None
    comment: str | None = None
    created: datetime | None = None
    de: str | None = None
    deName: str | None = None
    lastUpdated: datetime | None = None
    max: int | None = None
    min: int | None = None
    ou: str | None = None
    ouName: str | None = None
    ouPath: str | None = None
    pe: str | None = None
    peEndDate: datetime | None = None
    peName: str | None = None
    peStartDate: datetime | None = None
    peType: str | None = None
    storedBy: str | None = None
    value: str | None = None
