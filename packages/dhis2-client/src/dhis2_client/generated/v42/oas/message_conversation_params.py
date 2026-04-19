"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import MessageConversationPriority, MessageConversationStatus, MessageType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_message import UserMessage
    from .user_params import UserParams


class MessageConversationParamsAssignee(_BaseModel):
    """OpenAPI schema `MessageConversationParamsAssignee`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationParamsCreatedBy(_BaseModel):
    """OpenAPI schema `MessageConversationParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `MessageConversationParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationParamsMessages(_BaseModel):
    """OpenAPI schema `MessageConversationParamsMessages`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationParams(_BaseModel):
    """OpenAPI schema `MessageConversationParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    assignee: MessageConversationParamsAssignee | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: MessageConversationParamsCreatedBy | None = None
    displayName: str | None = None
    extMessageId: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    followUp: bool | None = None
    id: str | None = None
    lastMessage: datetime | None = None
    lastSender: UserParams | None = None
    lastSenderFirstname: str | None = None
    lastSenderSurname: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MessageConversationParamsLastUpdatedBy | None = None
    messageCount: int | None = None
    messageType: MessageType | None = None
    messages: list[MessageConversationParamsMessages] | None = None
    priority: MessageConversationPriority | None = None
    read: bool | None = None
    sharing: Sharing | None = None
    status: MessageConversationStatus | None = None
    subject: str | None = None
    translations: list[Translation] | None = None
    userFirstname: str | None = None
    userMessages: list[UserMessage] | None = None
    userSurname: str | None = None
