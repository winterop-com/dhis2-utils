"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataValueChangelogType


class DataValueChangelogEntryPeriod(_BaseModel):
    """OpenAPI schema `DataValueChangelogEntryPeriod`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataValueChangelogEntry(_BaseModel):
    """OpenAPI schema `DataValueChangelogEntry`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeOptionCombo: str | None = None
    auditType: DataValueChangelogType | None = None
    categoryOptionCombo: str | None = None
    created: datetime | None = None
    dataElement: str | None = None
    modifiedBy: str | None = None
    orgUnit: str | None = None
    period: DataValueChangelogEntryPeriod | None = None
    value: str | None = None
