"""Generated ProgramNotificationTemplate model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import NotificationTrigger, ProgramNotificationRecipient


class ProgramNotificationTemplate(BaseModel):
    """Generated model for DHIS2 `ProgramNotificationTemplate`.

    DHIS2 Program Notification Template - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /api/programNotificationTemplates.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
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
    messageTemplate: str | None = Field(default=None, description="Length/value min=1, max=10000.")
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    notificationRecipient: ProgramNotificationRecipient | None = None
    notificationTrigger: NotificationTrigger | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientDataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    recipientProgramAttribute: Reference | None = Field(
        default=None, description="Reference to TrackedEntityAttribute."
    )
    recipientUserGroup: Reference | None = Field(default=None, description="Reference to UserGroup.")
    relativeScheduledDays: int | None = Field(default=None, description="Length/value max=2147483647.")
    sendRepeatable: bool | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    subjectTemplate: str | None = Field(default=None, description="Length/value max=100.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
