"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class PeriodType(_BaseModel):
    """OpenAPI schema `PeriodType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayLabel: str | None = None
    displayName: str | None = None
    frequencyOrder: int | None = None
    isoDuration: str | None = None
    isoFormat: str | None = None
    label: str | None = None
    name: str | None = None
