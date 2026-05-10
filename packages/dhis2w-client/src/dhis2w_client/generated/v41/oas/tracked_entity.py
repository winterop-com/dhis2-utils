"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .relationship_item import RelationshipItem
    from .sharing import Sharing
    from .tracked_entity_attribute_value import TrackedEntityAttributeValue
    from .tracked_entity_program_owner import TrackedEntityProgramOwner
    from .translation import Translation
    from .user_info_snapshot import UserInfoSnapshot


class TrackedEntityCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityEnrollments(_BaseModel):
    """A UID reference to a Enrollment  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityTrackedEntityType(_BaseModel):
    """A UID reference to a TrackedEntityType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntity(_BaseModel):
    """OpenAPI schema `TrackedEntity`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: TrackedEntityCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    displayName: str | None = None
    enrollments: list[TrackedEntityEnrollments] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    geometry: dict[str, Any] | None = None
    href: str | None = None
    id: str | None = None
    inactive: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: TrackedEntityLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    name: str | None = None
    organisationUnit: TrackedEntityOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    potentialDuplicate: bool | None = None
    programOwners: list[TrackedEntityProgramOwner] | None = None
    relationshipItems: list[RelationshipItem] | None = None
    sharing: Sharing | None = None
    storedBy: str | None = None
    trackedEntityAttributeValues: list[TrackedEntityAttributeValue] | None = None
    trackedEntityType: TrackedEntityTrackedEntityType | None = _Field(
        default=None, description="A UID reference to a TrackedEntityType  "
    )
    translations: list[Translation] | None = None
    user: TrackedEntityUser | None = _Field(default=None, description="A UID reference to a User  ")
