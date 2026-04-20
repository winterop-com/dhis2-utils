"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DeliveryChannel, NotificationTrigger, ProgramNotificationRecipient


class ProgramNotificationTemplateSnapshot(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateSnapshot`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    deliveryChannels: list[DeliveryChannel] | None = None
    messageTemplate: str | None = None
    notificationRecipient: ProgramNotificationRecipient | None = None
    notificationTrigger: NotificationTrigger | None = None
    sendRepeatable: bool | None = None
    subjectTemplate: str | None = None
