"""Generated JobConfiguration model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import JobStatus, JobType, SchedulingType
from .attribute_value import AttributeValue


class JobConfiguration(BaseModel):
    """Generated model for DHIS2 `JobConfiguration`.

    DHIS2 Job Configuration - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/jobConfigurations.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: list[AttributeValue] | None = Field(
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
    errorCodes: str | None = Field(default=None, description="Length/value max=2147483647.")
    executedBy: str | None = Field(default=None, description="Length/value max=11.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    jobParameters: Any | None = Field(default=None, description="Reference to JobParameters. Length/value max=255.")
    jobStatus: JobStatus | None = None
    jobType: JobType | None = None
    lastAlive: datetime | None = None
    lastExecuted: datetime | None = None
    lastExecutedStatus: JobStatus | None = None
    lastFinished: datetime | None = None
    lastRuntimeExecution: str | None = Field(default=None, description="Read-only.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    leaderOnlyJob: bool | None = Field(default=None, description="Read-only.")
    maxDelayedExecutionTime: datetime | None = Field(default=None, description="Read-only.")
    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")
    nextExecutionTime: datetime | None = Field(default=None, description="Read-only.")
    queueName: str | None = Field(default=None, description="Length/value max=50.")
    queuePosition: int | None = Field(default=None, description="Length/value max=2147483647.")
    schedulingType: SchedulingType | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userUid: str | None = Field(default=None, description="Read-only.")
