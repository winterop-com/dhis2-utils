"""Generated JobConfiguration model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import JobStatus, JobType, SchedulingType


class JobConfiguration(BaseModel):
    """Generated model for DHIS2 `JobConfiguration`.

    DHIS2 Job Configuration - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/jobConfigurations.



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

    code: str | None = None

    configurable: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    cronExpression: str | None = None

    delay: int | None = None

    displayName: str | None = None

    enabled: bool | None = None

    errorCodes: str | None = None

    executedBy: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    jobParameters: Any | None = Field(default=None, description="Reference to JobParameters. Read-only (inverse side).")

    jobStatus: JobStatus | None = None

    jobType: JobType | None = None

    lastAlive: datetime | None = None

    lastExecuted: datetime | None = None

    lastExecutedStatus: JobStatus | None = None

    lastFinished: datetime | None = None

    lastRuntimeExecution: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    leaderOnlyJob: bool | None = None

    maxDelayedExecutionTime: datetime | None = None

    name: str | None = None

    nextExecutionTime: datetime | None = None

    queueName: str | None = None

    queuePosition: int | None = None

    schedulingType: SchedulingType | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userUid: str | None = None
