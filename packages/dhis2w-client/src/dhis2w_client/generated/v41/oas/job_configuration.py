"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .aggregate_data_exchange_job_parameters import AggregateDataExchangeJobParameters
    from .analytics_job_parameters import AnalyticsJobParameters
    from .attribute_value import AttributeValue
    from .continuous_analytics_job_parameters import ContinuousAnalyticsJobParameters
    from .data_integrity_details_job_parameters import DataIntegrityDetailsJobParameters
    from .data_integrity_job_parameters import DataIntegrityJobParameters
    from .data_synchronization_job_parameters import DataSynchronizationJobParameters
    from .disable_inactive_users_job_parameters import DisableInactiveUsersJobParameters
    from .event_programs_data_synchronization_job_parameters import EventProgramsDataSynchronizationJobParameters
    from .geo_json_import_job_params import GeoJsonImportJobParams
    from .html_push_analytics_job_parameters import HtmlPushAnalyticsJobParameters
    from .import_options import ImportOptions
    from .lock_exception_cleanup_job_parameters import LockExceptionCleanupJobParameters
    from .metadata_import_params import MetadataImportParams
    from .metadata_sync_job_parameters import MetadataSyncJobParameters
    from .monitoring_job_parameters import MonitoringJobParameters
    from .predictor_job_parameters import PredictorJobParameters
    from .push_analysis_job_parameters import PushAnalysisJobParameters
    from .sharing import Sharing
    from .sms_job_parameters import SmsJobParameters
    from .sql_view_update_parameters import SqlViewUpdateParameters
    from .test_job_parameters import TestJobParameters
    from .tracker_programs_data_synchronization_job_parameters import TrackerProgramsDataSynchronizationJobParameters
    from .tracker_trigram_index_job_parameters import TrackerTrigramIndexJobParameters
    from .translation import Translation


class JobConfigurationCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class JobConfigurationLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class JobConfigurationUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class JobConfiguration(_BaseModel):
    """OpenAPI schema `JobConfiguration`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    configurable: bool | None = None
    created: datetime | None = None
    createdBy: JobConfigurationCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    cronExpression: str | None = None
    delay: int | None = None
    displayName: str | None = None
    enabled: bool | None = None
    errorCodes: str | None = None
    executedBy: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    jobParameters: (
        MetadataImportParams
        | ImportOptions
        | AnalyticsJobParameters
        | ContinuousAnalyticsJobParameters
        | MonitoringJobParameters
        | PredictorJobParameters
        | PushAnalysisJobParameters
        | HtmlPushAnalyticsJobParameters
        | SmsJobParameters
        | MetadataSyncJobParameters
        | EventProgramsDataSynchronizationJobParameters
        | TrackerProgramsDataSynchronizationJobParameters
        | DataSynchronizationJobParameters
        | DisableInactiveUsersJobParameters
        | TrackerTrigramIndexJobParameters
        | DataIntegrityJobParameters
        | DataIntegrityDetailsJobParameters
        | AggregateDataExchangeJobParameters
        | SqlViewUpdateParameters
        | LockExceptionCleanupJobParameters
        | TestJobParameters
        | GeoJsonImportJobParams
        | None
    ) = None
    jobStatus: Literal["RUNNING", "SCHEDULED", "DISABLED", "COMPLETED", "STOPPED", "FAILED", "NOT_STARTED"] | None = (
        None
    )
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
    lastAlive: datetime | None = None
    lastExecuted: datetime | None = None
    lastExecutedStatus: (
        Literal["RUNNING", "SCHEDULED", "DISABLED", "COMPLETED", "STOPPED", "FAILED", "NOT_STARTED"] | None
    ) = None
    lastFinished: datetime | None = None
    lastRuntimeExecution: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: JobConfigurationLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    leaderOnlyJob: bool | None = None
    maxDelayedExecutionTime: datetime | None = None
    name: str | None = None
    nextExecutionTime: datetime | None = None
    queueName: str | None = None
    queuePosition: int | None = None
    schedulingType: Literal["CRON", "FIXED_DELAY", "ONCE_ASAP"] | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: JobConfigurationUser | None = _Field(default=None, description="A UID reference to a User  ")
    userUid: str | None = None
