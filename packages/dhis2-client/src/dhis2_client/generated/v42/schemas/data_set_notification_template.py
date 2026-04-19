"""Generated DataSetNotificationTemplate model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import DataSetNotificationRecipient, DataSetNotificationTrigger, SendStrategy


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataSetNotificationTemplate(BaseModel):
    """DHIS2 Data Set Notification Template - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/dataSetNotificationTemplates.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataSetNotificationTrigger: DataSetNotificationTrigger | None = None

    dataSets: list[Any] | None = Field(default=None, description="Collection of DataSet.")

    deliveryChannels: list[Any] | None = Field(default=None, description="Collection of DeliveryChannel.")

    displayMessageTemplate: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displaySubjectTemplate: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    messageTemplate: str | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    notificationRecipient: DataSetNotificationRecipient | None = None

    notifyParentOrganisationUnitOnly: bool | None = None

    notifyUsersInHierarchyOnly: bool | None = None

    recipientUserGroup: Reference | None = Field(default=None, description="Reference to UserGroup.")

    relativeScheduledDays: int | None = Field(default=None, description="Length/value max=2147483647.")

    sendStrategy: SendStrategy | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    subjectTemplate: str | None = Field(default=None, description="Length/value max=100.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
