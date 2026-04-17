"""Generated ProgramNotificationTemplate model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramNotificationTemplate(BaseModel):
    """DHIS2 ProgramNotificationTemplate resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    deliveryChannels: list[Any] | None = None

    displayMessageTemplate: str | None = None

    displayName: str | None = None

    displaySubjectTemplate: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    messageTemplate: str | None = None

    name: str | None = None

    notificationRecipient: str | None = None

    notificationTrigger: str | None = None

    notifyParentOrganisationUnitOnly: bool | None = None

    notifyUsersInHierarchyOnly: bool | None = None

    recipientDataElement: Reference | None = None

    recipientProgramAttribute: Reference | None = None

    recipientUserGroup: Reference | None = None

    relativeScheduledDays: int | None = None

    sendRepeatable: bool | None = None

    sharing: Any | None = None

    subjectTemplate: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
