"""Generated CategoryOption model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class CategoryOption(BaseModel):
    """Generated model for DHIS2 `CategoryOption`.

    DHIS2 Category Option - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/categoryOptions.

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
    categoryOptionCombos: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    categoryOptionGroups: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    categorys: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    code: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    default: bool | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    endDate: datetime | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    name: str | None = None
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    startDate: datetime | None = None
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
