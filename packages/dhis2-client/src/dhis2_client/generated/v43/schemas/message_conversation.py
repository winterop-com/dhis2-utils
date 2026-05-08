"""Generated MessageConversation model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import MessageConversationPriority, MessageConversationStatus, MessageType


class MessageConversation(BaseModel):
    """Generated model for DHIS2 `MessageConversation`.

    DHIS2 Message Conversation - DHIS2 resource (generated from /api/schemas at DHIS2 v43).

    API endpoint: /api/messageConversations.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    assignee: Reference | None = Field(default=None, description="Reference to User.")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    displayName: str | None = Field(default=None, description="Read-only.")
    extMessageId: str | None = Field(default=None, description="Length/value max=255.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    followUp: bool | None = None
    href: str | None = None
    id: str | None = Field(default=None, description="Length/value min=11, max=11.")
    lastMessage: datetime | None = None
    lastSender: Reference | None = Field(default=None, description="Reference to User.")
    lastSenderFirstname: str | None = Field(default=None, description="Length/value max=2147483647.")
    lastSenderSurname: str | None = Field(default=None, description="Length/value max=2147483647.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    messageCount: int | None = Field(default=None, description="Length/value max=2147483647.")
    messageType: MessageType | None = None
    messages: list[Any] | None = Field(default=None, description="Collection of Message.")
    name: str | None = Field(default=None, description="Length/value max=2147483647.")
    priority: MessageConversationPriority | None = None
    read: bool | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    status: MessageConversationStatus | None = None
    subject: str | None = Field(default=None, description="Length/value min=2, max=255.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userFirstname: str | None = Field(default=None, description="Length/value max=2147483647.")
    userMessages: list[Any] | None = Field(default=None, description="Collection of UserMessage.")
    userSurname: str | None = Field(default=None, description="Length/value max=2147483647.")
