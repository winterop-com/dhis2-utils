"""Generated Icon model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Icon(BaseModel):
    """Generated model for DHIS2 `Icon`.

    DHIS2 Icon - DHIS2 resource (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/icons.
    Transient — not stored in the DHIS2 database (computed / projection).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    custom: bool | None = None
    description: str | None = Field(default=None, description="Length/value max=2147483647.")
    fileResource: Reference | None = Field(
        default=None, description="Reference to FileResource. Read-only (inverse side)."
    )
    href: str | None = Field(default=None, description="Length/value max=2147483647.")
    key: str | None = Field(default=None, description="Length/value max=2147483647.")
    keywords: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    lastUpdated: datetime | None = None
