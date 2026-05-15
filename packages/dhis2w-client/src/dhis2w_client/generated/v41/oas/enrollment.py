"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .relationship_item import RelationshipItem
    from .sharing import Sharing
    from .translation import Translation
    from .user_info_snapshot import UserInfoSnapshot


class EnrollmentCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentEvents(_BaseModel):
    """A UID reference to a Event  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentMessageConversations(_BaseModel):
    """A UID reference to a MessageConversation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentTrackedEntityComments(_BaseModel):
    """A UID reference to a Note  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentTrackedEntityInstance(_BaseModel):
    """A UID reference to a TrackedEntity  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EnrollmentUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Enrollment(_BaseModel):
    """OpenAPI schema `Enrollment`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: EnrollmentCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    displayName: str | None = None
    enrollmentDate: datetime | None = None
    events: list[EnrollmentEvents] | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followup: bool | None = None
    geometry: dict[str, Any] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: EnrollmentLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    messageConversations: list[EnrollmentMessageConversations] | None = None
    name: str | None = None
    occurredDate: datetime | None = None
    organisationUnit: EnrollmentOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    program: EnrollmentProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    relationshipItems: list[RelationshipItem] | None = None
    sharing: Sharing | None = None
    status: Literal["ACTIVE", "COMPLETED", "CANCELLED"] | None = None
    storedBy: str | None = None
    trackedEntityComments: list[EnrollmentTrackedEntityComments] | None = None
    trackedEntityInstance: EnrollmentTrackedEntityInstance | None = _Field(
        default=None, description="A UID reference to a TrackedEntity  "
    )
    translations: list[Translation] | None = None
    user: EnrollmentUser | None = _Field(default=None, description="A UID reference to a User  ")
