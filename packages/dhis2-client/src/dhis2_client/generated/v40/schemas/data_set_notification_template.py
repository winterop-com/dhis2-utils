"""Generated DataSetNotificationTemplate model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataSetNotificationTemplate(BaseModel):
    """DHIS2 Data Set Notification Template - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/dataSetNotificationTemplates.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataSetNotificationTrigger: str | None = None

    dataSets: list[Any] | None = Field(default=None, description="Collection of DataSet.")

    deliveryChannels: list[Any] | None = Field(default=None, description="Collection of DeliveryChannel.")

    displayMessageTemplate: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displaySubjectTemplate: str | None = Field(default=None, description="Read-only.")

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    messageTemplate: str | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    notificationRecipient: str | None = None

    notifyParentOrganisationUnitOnly: bool | None = None

    notifyUsersInHierarchyOnly: bool | None = None

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    recipientUserGroup: Reference | None = Field(default=None, description="Reference to UserGroup.")

    relativeScheduledDays: int | None = Field(default=None, description="Length/value max=2147483647.")

    sendStrategy: str | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    subjectTemplate: str | None = Field(default=None, description="Length/value max=100.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroupAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )
