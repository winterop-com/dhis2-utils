"""Generated Relationship model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from .attribute_value import AttributeValue


class Relationship(BaseModel):
    """Generated model for DHIS2 `Relationship`.

    DHIS2 Relationship - DHIS2 resource (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/relationships.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    deleted: bool | None = None
    description: str | None = Field(default=None, description="Length/value max=2147483647.")
    displayName: str | None = Field(default=None, description="Read-only.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    formName: str | None = Field(default=None, description="Length/value max=2147483647.")
    from_: Any | None = Field(
        default=None, alias="from", description="Reference to RelationshipItem. Unique. Length/value max=255."
    )
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    relationshipType: Reference | None = Field(default=None, description="Reference to RelationshipType.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")
    to: Any | None = Field(default=None, description="Reference to RelationshipItem. Unique. Length/value max=255.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
