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
    from .attribute_value_params import AttributeValueParams
    from .enrollment_params import EnrollmentParams
    from .event_params import EventParams
    from .program_message_recipients_params import ProgramMessageRecipientsParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramMessageParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramMessageParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramMessageParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageParams(_BaseModel):
    """OpenAPI schema `ProgramMessageParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramMessageParamsCreatedBy | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    displayName: str | None = None
    enrollment: EnrollmentParams | None = None
    event: EventParams | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramMessageParamsLastUpdatedBy | None = None
    messageStatus: ProgramMessageStatus | None = None
    name: str | None = None
    notificationTemplate: str | None = None
    processedDate: datetime | None = None
    recipients: ProgramMessageRecipientsParams | None = None
    sharing: Sharing | None = None
    storeCopy: bool | None = None
    subject: str | None = None
    text: str | None = None
    translations: list[Translation] | None = None
