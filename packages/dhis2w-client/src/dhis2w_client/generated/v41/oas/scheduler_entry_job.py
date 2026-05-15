"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class SchedulerEntryJob(_BaseModel):
    """OpenAPI schema `SchedulerEntryJob`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    cronExpression: str | None = None
    delay: int | None = None
    id: str | None = _Field(default=None, description="A UID for an JobConfiguration object  ")
    name: str | None = None
    nextExecutionTime: datetime | None = None
    status: Literal["RUNNING", "SCHEDULED", "DISABLED", "COMPLETED", "STOPPED", "FAILED", "NOT_STARTED"] | None = None
    type: (
        Literal[
            "DATA_INTEGRITY",
            "DATA_INTEGRITY_DETAILS",
            "RESOURCE_TABLE",
            "ANALYTICS_TABLE",
            "CONTINUOUS_ANALYTICS_TABLE",
            "DATA_SYNC",
            "TRACKER_PROGRAMS_DATA_SYNC",
            "EVENT_PROGRAMS_DATA_SYNC",
            "META_DATA_SYNC",
            "AGGREGATE_DATA_EXCHANGE",
            "SEND_SCHEDULED_MESSAGE",
            "PROGRAM_NOTIFICATIONS",
            "MONITORING",
            "PUSH_ANALYSIS",
            "HTML_PUSH_ANALYTICS",
            "TRACKER_SEARCH_OPTIMIZATION",
            "PREDICTOR",
            "MATERIALIZED_SQL_VIEW_UPDATE",
            "DISABLE_INACTIVE_USERS",
            "TEST",
            "LOCK_EXCEPTION_CLEANUP",
            "MOCK",
            "SMS_SEND",
            "TRACKER_IMPORT_JOB",
            "TRACKER_IMPORT_NOTIFICATION_JOB",
            "TRACKER_IMPORT_RULE_ENGINE_JOB",
            "IMAGE_PROCESSING",
            "COMPLETE_DATA_SET_REGISTRATION_IMPORT",
            "DATAVALUE_IMPORT_INTERNAL",
            "METADATA_IMPORT",
            "DATAVALUE_IMPORT",
            "GEOJSON_IMPORT",
            "EVENT_IMPORT",
            "ENROLLMENT_IMPORT",
            "TEI_IMPORT",
            "GML_IMPORT",
            "HOUSEKEEPING",
            "DATA_VALUE_TRIM",
            "DATA_SET_NOTIFICATION",
            "CREDENTIALS_EXPIRY_ALERT",
            "DATA_STATISTICS",
            "FILE_RESOURCE_CLEANUP",
            "ACCOUNT_EXPIRY_ALERT",
            "VALIDATION_RESULTS_NOTIFICATION",
            "REMOVE_USED_OR_EXPIRED_RESERVED_VALUES",
            "SYSTEM_VERSION_UPDATE_CHECK",
        ]
        | None
    ) = None
