"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation
    from .user_message import UserMessage


class MessageConversationAssignee(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationLastSender(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationMessages(_BaseModel):
    """A UID reference to a Message  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversation(_BaseModel):
    """OpenAPI schema `MessageConversation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    assignee: MessageConversationAssignee | None = _Field(default=None, description="A UID reference to a User  ")
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: MessageConversationCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    extMessageId: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followUp: bool | None = None
    href: str | None = None
    id: str | None = None
    lastMessage: datetime | None = None
    lastSender: MessageConversationLastSender | None = _Field(default=None, description="A UID reference to a User  ")
    lastSenderFirstname: str | None = None
    lastSenderSurname: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MessageConversationLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    messageCount: int | None = None
    messageType: Literal["PRIVATE", "SYSTEM", "VALIDATION_RESULT", "TICKET", "SYSTEM_VERSION_UPDATE"] | None = None
    messages: list[MessageConversationMessages] | None = None
    priority: Literal["NONE", "LOW", "MEDIUM", "HIGH"] | None = None
    read: bool | None = None
    sharing: Sharing | None = None
    status: Literal["NONE", "OPEN", "PENDING", "INVALID", "SOLVED"] | None = None
    subject: str | None = None
    translations: list[Translation] | None = None
    user: MessageConversationUser | None = _Field(default=None, description="A UID reference to a User  ")
    userFirstname: str | None = None
    userMessages: list[UserMessage] | None = None
    userSurname: str | None = None
