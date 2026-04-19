"""Typed models for DHIS2 aggregate data values.

Covers the `/api/dataValueSets` GET response (a `DataValueSet` envelope
containing a list of `DataValue`s). The corresponding POST/import path
returns a `WebMessageResponse` (see `dhis2_client/envelopes.py`).

Distinct from the *generated* `DataElement` / `DataSet` / `CategoryOptionCombo`
metadata models (those come out of `/api/schemas` codegen) — these describe
the **runtime values** captured against that metadata.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DataValue(BaseModel):
    """One aggregate data value — the payload captured for (DE, period, OU, COC, AOC)."""

    model_config = ConfigDict(extra="allow")

    dataElement: str | None = None
    period: str | None = None
    orgUnit: str | None = None
    categoryOptionCombo: str | None = None
    attributeOptionCombo: str | None = None
    value: str | None = None
    storedBy: str | None = None
    created: datetime | None = None
    lastUpdated: datetime | None = None
    comment: str | None = None
    followup: bool | None = None
    deleted: bool | None = None


class DataValueSet(BaseModel):
    """`/api/dataValueSets` GET envelope.

    DHIS2 returns a domain envelope (not a WebMessageResponse) for this read —
    optional `dataSet` / `completeDate` / `period` / `orgUnit` scope fields
    plus the `dataValues` list.
    """

    model_config = ConfigDict(extra="allow")

    dataSet: str | None = None
    completeDate: datetime | None = None
    period: str | None = None
    orgUnit: str | None = None
    dataValues: list[DataValue] = Field(default_factory=list)


__all__ = ["DataValue", "DataValueSet"]
