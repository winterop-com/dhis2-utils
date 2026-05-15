"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .property import Property


class JobTypeInfo(_BaseModel):
    """OpenAPI schema `JobTypeInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    jobParameters: list[Property] | None = None
    jobType: (
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
    name: str | None = None
    schedulingType: Literal["CRON", "FIXED_DELAY", "ONCE_ASAP"] | None = None
