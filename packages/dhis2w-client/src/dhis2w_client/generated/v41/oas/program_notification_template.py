"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class ProgramNotificationTemplateCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateRecipientDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateRecipientProgramAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateRecipientUserGroup(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplateUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramNotificationTemplate(_BaseModel):
    """OpenAPI schema `ProgramNotificationTemplate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramNotificationTemplateCreatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    deliveryChannels: list[str] | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramNotificationTemplateLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    messageTemplate: str | None = None
    name: str | None = None
    notificationRecipient: str | None = None
    notificationTrigger: str | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientDataElement: ProgramNotificationTemplateRecipientDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    recipientProgramAttribute: ProgramNotificationTemplateRecipientProgramAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    recipientUserGroup: ProgramNotificationTemplateRecipientUserGroup | None = _Field(
        default=None, description="A UID reference to a UserGroup  "
    )
    relativeScheduledDays: int | None = None
    sendRepeatable: bool | None = None
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
    user: ProgramNotificationTemplateUser | None = _Field(default=None, description="A UID reference to a User  ")
