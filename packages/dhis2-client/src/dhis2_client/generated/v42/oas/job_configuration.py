"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import JobStatus, JobType, SchedulingType

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
    from .single_event_data_synchronization_job_parameters import SingleEventDataSynchronizationJobParameters
    from .sms_job_parameters import SmsJobParameters
    from .sql_view_update_parameters import SqlViewUpdateParameters
    from .test_job_parameters import TestJobParameters
    from .tracker_data_synchronization_job_parameters import TrackerDataSynchronizationJobParameters
    from .tracker_trigram_index_job_parameters import TrackerTrigramIndexJobParameters
    from .translation import Translation
    from .user_dto import UserDto


class JobConfiguration(_BaseModel):
    """OpenAPI schema `JobConfiguration`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    configurable: bool | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
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
        | DataSynchronizationJobParameters
        | SingleEventDataSynchronizationJobParameters
        | TrackerDataSynchronizationJobParameters
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
    jobStatus: JobStatus | None = None
    jobType: JobType | None = None
    lastAlive: datetime | None = None
    lastExecuted: datetime | None = None
    lastExecutedStatus: JobStatus | None = None
    lastFinished: datetime | None = None
    lastRuntimeExecution: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    leaderOnlyJob: bool | None = None
    maxDelayedExecutionTime: datetime | None = None
    name: str | None = None
    nextExecutionTime: datetime | None = None
    queueName: str | None = None
    queuePosition: int | None = None
    schedulingType: SchedulingType | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    userUid: str | None = None
