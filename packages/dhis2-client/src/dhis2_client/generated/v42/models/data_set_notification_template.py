"""Generated DataSetNotificationTemplate model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataSetNotificationTemplate(BaseModel):
    """DHIS2 DataSetNotificationTemplate resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataSetNotificationTrigger: str | None = None

    dataSets: list[Any] | None = None

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

    notifyParentOrganisationUnitOnly: bool | None = None

    notifyUsersInHierarchyOnly: bool | None = None

    recipientUserGroup: Reference | None = None

    relativeScheduledDays: int | None = None

    sendStrategy: str | None = None

    sharing: Any | None = None

    subjectTemplate: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
