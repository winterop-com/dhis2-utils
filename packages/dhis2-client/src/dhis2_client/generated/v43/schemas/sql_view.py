"""Generated SqlView model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import CacheStrategy, SqlViewType


class SqlView(BaseModel):
    """Generated model for DHIS2 `SqlView`.

    DHIS2 Sql View - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /dev-2-43/api/sqlViews.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")
    cacheStrategy: CacheStrategy | None = None
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    description: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")
    displayName: str | None = Field(default=None, description="Read-only.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    sqlQuery: str | None = Field(default=None, description="Length/value max=2147483647.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    type: SqlViewType | None = None
    updateJobId: str | None = Field(default=None, description="Length/value max=2147483647.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
