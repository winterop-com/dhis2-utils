"""Generated DataSetNotificationTemplate model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataSetNotificationTemplate(BaseModel):
    """DHIS2 Data Set Notification Template - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/dataSetNotificationTemplates.



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

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataSetNotificationTrigger: str | None = None

    dataSets: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    deliveryChannels: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    displayMessageTemplate: str | None = None

    displayName: str | None = None

    displaySubjectTemplate: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    messageTemplate: str | None = None

    name: str | None = None

    notificationRecipient: str | None = None

    notifyParentOrganisationUnitOnly: bool | None = None

    notifyUsersInHierarchyOnly: bool | None = None

    recipientUserGroup: Reference | None = Field(
        default=None, description="Reference to UserGroup. Read-only (inverse side)."
    )

    relativeScheduledDays: int | None = None

    sendStrategy: str | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    subjectTemplate: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    uid: str | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
