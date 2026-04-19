"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import MessageConversationPriority, MessageConversationStatus, MessageType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .message import Message
    from .sharing import Sharing
    from .translation import Translation
    from .user import User
    from .user_dto import UserDto
    from .user_message import UserMessage


class MessageConversation(_BaseModel):
    """OpenAPI schema `MessageConversation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    assignee: User | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    extMessageId: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followUp: bool | None = None
    href: str | None = None
    id: str | None = None
    lastMessage: datetime | None = None
    lastSender: BaseIdentifiableObject | None = None
    lastSenderFirstname: str | None = None
    lastSenderSurname: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    messageCount: int | None = None
    messageType: MessageType | None = None
    messages: list[Message] | None = None
    priority: MessageConversationPriority | None = None
    read: bool | None = None
    sharing: Sharing | None = None
    status: MessageConversationStatus | None = None
    subject: str | None = None
    translations: list[Translation] | None = None
    userFirstname: str | None = None
    userMessages: list[UserMessage] | None = None
    userSurname: str | None = None
