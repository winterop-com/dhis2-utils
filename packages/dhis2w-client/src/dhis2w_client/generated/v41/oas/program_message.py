"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .program_message_recipients import ProgramMessageRecipients
    from .sharing import Sharing
    from .translation import Translation


class ProgramMessageCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageEnrollment(_BaseModel):
    """A UID reference to a Enrollment  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageEvent(_BaseModel):
    """A UID reference to a Event  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessage(_BaseModel):
    """OpenAPI schema `ProgramMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramMessageCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    deliveryChannels: list[str] | None = None
    displayName: str | None = None
    enrollment: ProgramMessageEnrollment | None = _Field(default=None, description="A UID reference to a Enrollment  ")
    event: ProgramMessageEvent | None = _Field(default=None, description="A UID reference to a Event  ")
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramMessageLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    messageStatus: str | None = None
    name: str | None = None
    notificationTemplate: str | None = None
    processedDate: datetime | None = None
    recipients: ProgramMessageRecipients | None = None
    sharing: Sharing | None = None
    storeCopy: bool | None = None
    subject: str | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    user: ProgramMessageUser | None = _Field(default=None, description="A UID reference to a User  ")
