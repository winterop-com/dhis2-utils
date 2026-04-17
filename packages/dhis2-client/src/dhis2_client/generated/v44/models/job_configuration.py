"""Generated JobConfiguration model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class JobConfiguration(BaseModel):
    """DHIS2 JobConfiguration resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    configurable: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    cronExpression: str | None = None

    delay: int | None = None

    displayName: str | None = None

    enabled: bool | None = None

    errorCodes: str | None = None

    executedBy: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    jobParameters: Any | None = None

    jobStatus: str | None = None

    jobType: str | None = None

    lastAlive: datetime | None = None

    lastExecuted: datetime | None = None

    lastExecutedStatus: str | None = None

    lastFinished: datetime | None = None

    lastRuntimeExecution: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    leaderOnlyJob: bool | None = None

    maxDelayedExecutionTime: datetime | None = None

    name: str | None = None

    nextExecutionTime: datetime | None = None

    queueName: str | None = None

    queuePosition: int | None = None

    schedulingType: str | None = None

    sharing: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    userUid: str | None = None
