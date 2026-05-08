"""Generated ProgramStageInstance model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import EventStatus
from .attribute_value import AttributeValue
from .relationship_item import RelationshipItem


class ProgramStageInstance(BaseModel):
    """Generated model for DHIS2 `ProgramStageInstance`.

    DHIS2 Program Stage Instance - DHIS2 resource (generated from /api/schemas at DHIS2 v40).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    assignedUser: Reference | None = Field(default=None, description="Reference to User.")
    attributeOptionCombo: Reference | None = Field(default=None, description="Reference to CategoryOptionCombo.")
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    comments: list[Any] | None = Field(default=None, description="Collection of TrackedEntityComment.")
    completed: bool | None = Field(default=None, description="Read-only.")
    completedBy: str | None = Field(default=None, description="Length/value max=255.")
    completedDate: datetime | None = None
    creatableInSearchScope: bool | None = Field(default=None, description="Read-only.")
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    createdByUserInfo: Any | None = Field(
        default=None, description="Reference to UserInfoSnapshot. Length/value max=255."
    )
    deleted: bool | None = None
    displayName: str | None = Field(default=None, description="Read-only.")
    dueDate: datetime | None = None
    eventDataValues: list[Any] | None = Field(
        default=None, description="Collection of EventDataValue. Length/value max=255."
    )
    executionDate: datetime | None = None
    externalAccess: bool | None = None
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    geometry: Any | None = Field(default=None, description="Reference to Geometry. Length/value max=255.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    lastUpdatedByUserInfo: Any | None = Field(
        default=None, description="Reference to UserInfoSnapshot. Length/value max=255."
    )
    messageConversations: list[Any] | None = Field(default=None, description="Collection of MessageConversation.")
    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    organisationUnit: Reference | None = Field(default=None, description="Reference to OrganisationUnit.")
    programInstance: Reference | None = Field(default=None, description="Reference to ProgramInstance.")
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")
    relationshipItems: list[RelationshipItem] | None = Field(
        default=None, description="Collection of RelationshipItem. Read-only (inverse side)."
    )
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    status: EventStatus | None = None
    storedBy: str | None = Field(default=None, description="Length/value max=255.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )
    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )
