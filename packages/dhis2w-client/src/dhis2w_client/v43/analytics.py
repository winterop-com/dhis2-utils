"""Typed models for DHIS2 `/api/analytics*` query responses.

Re-exports the OAS-emitted `Grid` / `GridHeader` models as the canonical
types for every `/api/analytics*` response (standard / raw / events /
enrollments / outlier / tracked-entity — they all share the Grid
envelope). `AnalyticsMetaData` is a typed parser helper: DHIS2's
`Grid.metaData` is `dict[str, Any]` on the wire (dimension lookups + item
descriptors keyed by UID), and callers that want the structured
`{items, dimensions}` view use `AnalyticsMetaData.model_validate(grid.metaData)`
to lift the raw dict into a typed model.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v42.oas import Grid, GridHeader


class AnalyticsMetaData(BaseModel):
    """Typed view over `Grid.metaData` — dimension lookups + item descriptors.

    DHIS2 returns `metaData` as a bare JSON object with two stable sub-keys
    (`items` and `dimensions`) plus freeform extras that vary by request.
    This helper parses the raw dict into those typed fields; callers lift
    a `Grid.metaData` dict via `AnalyticsMetaData.model_validate(grid.metaData)`
    when they want to walk `dimensions["dx"]` / look up `items[<uid>].name`
    / etc. without writing their own dict-walking.
    """

    model_config = ConfigDict(extra="allow")

    items: dict[str, Any] = Field(default_factory=dict)
    dimensions: dict[str, list[str]] = Field(default_factory=dict)


__all__ = ["AnalyticsMetaData", "Grid", "GridHeader"]
