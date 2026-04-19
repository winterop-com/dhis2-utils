"""Generated ApiToken model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ApiTokenType


class ApiToken(BaseModel):
    """Generated model for DHIS2 `ApiToken`.

    DHIS2 Api Token - persisted metadata (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/apiToken.



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

    attributes: list[Any] | None = Field(
        default=None, description="Collection of ApiTokenAttribute. Length/value max=255."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    displayName: str | None = Field(default=None, description="Read-only.")

    expire: float | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    type: ApiTokenType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    version: int | None = Field(default=None, description="Length/value max=2147483647.")
