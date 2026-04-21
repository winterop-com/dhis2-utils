"""Generated OutlierAnalysis model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import NormalizedOutlierMethod, OutlierMethod


class OutlierAnalysis(BaseModel):
    """Generated model for DHIS2 `OutlierAnalysis`.

    DHIS2 Outlier Analysis - DHIS2 resource (generated from /api/schemas at DHIS2 v43).

    Transient — not stored in the DHIS2 database (computed / projection).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    enabled: bool | None = None
    extremeLines: Any | None = Field(default=None, description="Reference to OutlierLine. Read-only (inverse side).")
    maxResults: int | None = Field(default=None, description="Length/value max=2147483647.")
    normalizationMethod: NormalizedOutlierMethod | None = None
    outlierMethod: OutlierMethod | None = None
    thresholdFactor: float | None = None
