"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .database_info import DatabaseInfo
    from .system_capability import SystemCapability


class SystemInfo(_BaseModel):
    """OpenAPI schema `SystemInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    buildTime: datetime | None = None
    calendar: str | None = None
    capability: SystemCapability | None = None
    clusterHostname: str | None = None
    contextPath: str | None = None
    cpuCores: int | None = None
    databaseInfo: DatabaseInfo | None = None
    dateFormat: str | None = None
    emailConfigured: bool | None = None
    encryption: bool | None = None
    environmentVariable: str | None = None
    externalDirectory: str | None = None
    fileStoreProvider: str | None = None
    instanceBaseUrl: str | None = None
    intervalSinceLastAnalyticsTablePartitionSuccess: str | None = None
    intervalSinceLastAnalyticsTableSuccess: str | None = None
    isMetadataSyncEnabled: bool | None = None
    isMetadataVersionEnabled: bool | None = None
    jasperReportsVersion: str | None = None
    javaOpts: str | None = None
    javaVendor: str | None = None
    javaVersion: str | None = None
    lastAnalyticsTablePartitionRuntime: str | None = None
    lastAnalyticsTablePartitionSuccess: datetime | None = None
    lastAnalyticsTableRuntime: str | None = None
    lastAnalyticsTableSuccess: datetime | None = None
    lastMetadataVersionSyncAttempt: datetime | None = None
    lastSystemMonitoringSuccess: datetime | None = None
    memoryInfo: str | None = None
    nodeId: str | None = None
    osArchitecture: str | None = None
    osName: str | None = None
    osVersion: str | None = None
    readOnlyMode: str | None = None
    readReplicaCount: int | None = None
    redisEnabled: bool | None = None
    redisHostname: str | None = None
    revision: str | None = None
    serverDate: datetime | None = None
    serverTimeZoneDisplayName: str | None = None
    serverTimeZoneId: str | None = None
    sessionTimeout: int | None = None
    systemId: str | None = None
    systemMetadataVersion: str | None = None
    systemMonitoringUrl: str | None = None
    systemName: str | None = None
    userAgent: str | None = None
    version: str | None = None
