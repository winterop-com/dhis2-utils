"""Generated ApiToken model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ApiTokenType


class ApiToken(BaseModel):
    """Generated model for DHIS2 `ApiToken`.

    DHIS2 Api Token - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/apiToken.

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
    attributes: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    code: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    displayName: str | None = None
    expire: float | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    name: str | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    type: ApiTokenType | None = None
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    version: int | None = None
