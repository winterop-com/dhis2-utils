"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DeliveryChannel, NotificationTrigger, ProgramNotificationRecipient

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class ProgramNotificationTemplateParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateParamsRecipientDataElement(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParamsRecipientDataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateParamsRecipientProgramAttribute(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParamsRecipientProgramAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateParamsRecipientUserGroup(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParamsRecipientUserGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateParams(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplateParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramNotificationTemplateParamsCreatedBy | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramNotificationTemplateParamsLastUpdatedBy | None = None
    messageTemplate: str | None = None
    name: str | None = None
    notificationRecipient: ProgramNotificationRecipient | None = None
    notificationTrigger: NotificationTrigger | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientDataElement: ProgramNotificationTemplateParamsRecipientDataElement | None = None
    recipientProgramAttribute: ProgramNotificationTemplateParamsRecipientProgramAttribute | None = None
    recipientUserGroup: ProgramNotificationTemplateParamsRecipientUserGroup | None = None
    relativeScheduledDays: int | None = None
    sendRepeatable: bool | None = None
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
