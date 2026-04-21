"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class DataValue(_BaseModel):
    """OpenAPI schema `DataValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: str | None = None
    categoryOptionCombo: str | None = None
    comment: str | None = None
    created: str | None = None
    dataElement: str | None = None
    deleted: bool | None = None
    followup: bool | None = None
    lastUpdated: str | None = None
    orgUnit: str | None = None
    period: str | None = None
    storedBy: str | None = None
    value: str | None = None
