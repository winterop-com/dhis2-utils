"""Generated TrackedEntity model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from .attribute_value import AttributeValue
from .relationship_item import RelationshipItem
from .tracked_entity_attribute_value import TrackedEntityAttributeValue


class TrackedEntity(BaseModel):
    """Generated model for DHIS2 `TrackedEntity`.

    DHIS2 Tracked Entity - DHIS2 resource (generated from /api/schemas at DHIS2 v41).


    API endpoint: /api/trackedEntityInstances.



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

    createdByUserInfo: Any | None = Field(
        default=None, description="Reference to UserInfoSnapshot. Length/value max=255."
    )

    deleted: bool | None = None

    displayName: str | None = Field(default=None, description="Read-only.")

    enrollments: list[Any] | None = Field(
        default=None, description="Collection of Enrollment. Read-only (inverse side)."
    )

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    geometry: Any | None = Field(default=None, description="Reference to Geometry. Length/value max=255.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    inactive: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedAtClient: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    lastUpdatedByUserInfo: Any | None = Field(
        default=None, description="Reference to UserInfoSnapshot. Length/value max=255."
    )

    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    organisationUnit: Reference | None = Field(default=None, description="Reference to OrganisationUnit.")

    potentialDuplicate: bool | None = None

    programOwners: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityProgramOwner. Read-only (inverse side)."
    )

    relationshipItems: list[RelationshipItem] | None = Field(
        default=None, description="Collection of RelationshipItem. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    storedBy: str | None = Field(default=None, description="Length/value max=255.")

    trackedEntityAttributeValues: list[TrackedEntityAttributeValue] | None = Field(
        default=None, description="Collection of TrackedEntityAttributeValue. Read-only (inverse side)."
    )

    trackedEntityType: Reference | None = Field(default=None, description="Reference to TrackedEntityType.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
