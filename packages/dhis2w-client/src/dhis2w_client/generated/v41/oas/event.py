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
    from .event_data_value import EventDataValue
    from .relationship_item import RelationshipItem
    from .sharing import Sharing
    from .translation import Translation
    from .user_info_snapshot import UserInfoSnapshot


class EventAssignedUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventAttributeOptionCombo(_BaseModel):
    """A UID reference to a CategoryOptionCombo  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventEnrollment(_BaseModel):
    """A UID reference to a Enrollment  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventMessageConversations(_BaseModel):
    """A UID reference to a MessageConversation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventNotes(_BaseModel):
    """A UID reference to a Note  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Event(_BaseModel):
    """OpenAPI schema `Event`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    assignedUser: EventAssignedUser | None = _Field(default=None, description="A UID reference to a User  ")
    attributeOptionCombo: EventAttributeOptionCombo | None = _Field(
        default=None, description="A UID reference to a CategoryOptionCombo  "
    )
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    completed: bool | None = None
    completedBy: str | None = None
    completedDate: datetime | None = None
    creatableInSearchScope: bool | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: EventCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    createdByUserInfo: UserInfoSnapshot | None = None
    deleted: bool | None = None
    displayName: str | None = None
    enrollment: EventEnrollment | None = _Field(default=None, description="A UID reference to a Enrollment  ")
    eventDataValues: list[EventDataValue] | None = None
    eventDate: datetime | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    geometry: dict[str, Any] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedAtClient: datetime | None = None
    lastUpdatedBy: EventLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    lastUpdatedByUserInfo: UserInfoSnapshot | None = None
    messageConversations: list[EventMessageConversations] | None = None
    name: str | None = None
    notes: list[EventNotes] | None = None
    organisationUnit: EventOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    programStage: EventProgramStage | None = _Field(default=None, description="A UID reference to a ProgramStage  ")
    relationshipItems: list[RelationshipItem] | None = None
    scheduledDate: datetime | None = None
    sharing: Sharing | None = None
    status: Literal["ACTIVE", "COMPLETED", "VISITED", "SCHEDULE", "OVERDUE", "SKIPPED"] | None = None
    storedBy: str | None = None
    translations: list[Translation] | None = None
    user: EventUser | None = _Field(default=None, description="A UID reference to a User  ")
