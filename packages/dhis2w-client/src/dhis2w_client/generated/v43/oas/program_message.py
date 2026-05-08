"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DeliveryChannel, ProgramMessageStatus

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .identifiable_object import IdentifiableObject
    from .program_message_recipients import ProgramMessageRecipients


class ProgramMessage(_BaseModel):
    """OpenAPI schema `ProgramMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    enrollment: IdentifiableObject | None = None
    event: BaseIdentifiableObject | None = None
    messageStatus: ProgramMessageStatus | None = None
    notificationTemplate: str | None = None
    processedDate: datetime | None = None
    recipients: ProgramMessageRecipients | None = None
    subject: str | None = None
    text: str | None = None
