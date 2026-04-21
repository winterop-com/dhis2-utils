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
    from .enrollment_params import EnrollmentParams
    from .program_message_recipients_params import ProgramMessageRecipientsParams
    from .tracker_event_params import TrackerEventParams


class ProgramMessageParams(_BaseModel):
    """OpenAPI schema `ProgramMessageParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    enrollment: EnrollmentParams | None = None
    event: TrackerEventParams | None = None
    messageStatus: ProgramMessageStatus | None = None
    notificationTemplate: str | None = None
    processedDate: datetime | None = None
    recipients: ProgramMessageRecipientsParams | None = None
    subject: str | None = None
    text: str | None = None
