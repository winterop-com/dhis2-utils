"""Typed models for DHIS2 analytics query responses.

Covers the three response shapes the `/api/analytics` endpoint and its
`rawData.json` / `dataValueSet.json` siblings return. They share the same
top-level envelope (`headers`, `metaData`, `rows`, dimensions) — only the
inner row shape varies.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AnalyticsHeader(BaseModel):
    """One column header in `/api/analytics` responses."""

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    column: str | None = None
    valueType: str | None = None
    type: str | None = None
    hidden: bool | None = None
    meta: bool | None = None


class AnalyticsMetaData(BaseModel):
    """`metaData` sub-object — dimension lookups + item metadata.

    `items` maps dimension-value UIDs to `{name, code, uid, ...}` descriptors
    so callers can render human names for the UIDs in `rows`. `dimensions`
    maps each dimension key (`dx`, `pe`, `ou`, `co`, ...) to its list of
    requested UIDs in order.
    """

    model_config = ConfigDict(extra="allow")

    items: dict[str, Any] = Field(default_factory=dict)
    dimensions: dict[str, list[str]] = Field(default_factory=dict)


class AnalyticsResponse(BaseModel):
    """Top-level `/api/analytics` response.

    `rows` is a list of lists — each inner list has one entry per header,
    in the same order. Values are strings (DHIS2 encodes numbers as strings
    here to avoid JSON float-precision issues).
    """

    model_config = ConfigDict(extra="allow")

    headers: list[AnalyticsHeader] = Field(default_factory=list)
    metaData: AnalyticsMetaData | None = None
    rows: list[list[str]] = Field(default_factory=list)
    width: int | None = None
    height: int | None = None
    headerWidth: int | None = None
    rowContext: dict[str, Any] | None = None


__all__ = ["AnalyticsHeader", "AnalyticsMetaData", "AnalyticsResponse"]
