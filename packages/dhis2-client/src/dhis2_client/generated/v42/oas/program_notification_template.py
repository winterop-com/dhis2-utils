"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import DeliveryChannel, NotificationTrigger, ProgramNotificationRecipient

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .data_element import DataElement
    from .sharing import Sharing
    from .tracked_entity_attribute import TrackedEntityAttribute
    from .translation import Translation
    from .user_dto import UserDto
    from .user_group import UserGroup


class ProgramNotificationTemplate(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    messageTemplate: str | None = None
    name: str | None = None
    notificationRecipient: ProgramNotificationRecipient | None = None
    notificationTrigger: NotificationTrigger | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientDataElement: DataElement | None = None
    recipientProgramAttribute: TrackedEntityAttribute | None = None
    recipientUserGroup: UserGroup | None = None
    relativeScheduledDays: int | None = None
    sendRepeatable: bool | None = None
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
