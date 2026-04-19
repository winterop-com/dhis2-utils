"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import DeliveryChannel, ProgramMessageStatus

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .program_message_recipients import ProgramMessageRecipients
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class ProgramMessage(_BaseModel):
    """OpenAPI schema `ProgramMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    displayName: str | None = None
    enrollment: BaseIdentifiableObject | None = None
    event: BaseIdentifiableObject | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    messageStatus: ProgramMessageStatus | None = None
    name: str | None = None
    notificationTemplate: str | None = None
    processedDate: datetime | None = None
    recipients: ProgramMessageRecipients | None = None
    sharing: Sharing | None = None
    storeCopy: bool | None = None
    subject: str | None = None
    text: str | None = None
    translations: list[Translation] | None = None
