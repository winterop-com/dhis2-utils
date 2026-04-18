"""Generated JobConfiguration model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class JobConfiguration(BaseModel):
    """DHIS2 Job Configuration - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/jobConfigurations.



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

    configurable: bool | None = Field(default=None, description="Read-only.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    cronExpression: str | None = Field(default=None, description="Length/value max=255.")

    delay: int | None = Field(default=None, description="Length/value max=2147483647.")

    displayName: str | None = Field(default=None, description="Read-only.")

    enabled: bool | None = None

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    jobParameters: Any | None = Field(default=None, description="Reference to JobParameters. Length/value max=255.")

    jobStatus: str | None = None

    jobType: str | None = None

    lastExecuted: datetime | None = None

    lastExecutedStatus: str | None = None

    lastRuntimeExecution: str | None = Field(default=None, description="Length/value max=2147483647.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    leaderOnlyJob: bool | None = Field(default=None, description="Read-only.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    nextExecutionTime: datetime | None = Field(default=None, description="Read-only.")

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    schedulingType: str | None = Field(default=None, description="Read-only.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroupAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )

    userUid: str | None = Field(default=None, description="Length/value max=2147483647.")
