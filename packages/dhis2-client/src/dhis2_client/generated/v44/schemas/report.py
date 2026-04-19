"""Generated Report model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import CacheStrategy, ReportType


class Report(BaseModel):
    """Generated model for DHIS2 `Report`.

    DHIS2 Report - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/reports.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    cacheStrategy: CacheStrategy | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    designContent: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    name: str | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    reportParams: Any | None = Field(
        default=None, description="Reference to ReportingParams. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    type: ReportType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    visualization: Reference | None = Field(
        default=None, description="Reference to Visualization. Read-only (inverse side)."
    )
