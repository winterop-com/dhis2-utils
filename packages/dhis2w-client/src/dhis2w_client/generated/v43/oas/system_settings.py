"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import (
    AnalyticsCacheTtlMode,
    AnalyticsFinancialYearStartKey,
    AnalyticsWeeklyStartKey,
    Cacheability,
    CacheStrategy,
    DigitGroupSeparator,
    DisplayProperty,
    FileResourceRetentionStrategy,
    LoginPageLayout,
    NotificationLevel,
    RelativePeriodEnum,
)


class SystemSettings(_BaseModel):
    """OpenAPI schema `SystemSettings`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    KeyTrackedEntityMaxLimit: int | None = None
    accountExpiresInDays: int | None = None
    accountExpiryAlert: bool | None = None
    analyticsFinancialYearStart: AnalyticsFinancialYearStartKey | None = None
    analyticsWeeklyStart: AnalyticsWeeklyStartKey | None = None
    applicationTitle: str | None = None
    autoVerifyInvitedUserEmail: bool | None = None
    credentialsExpires: int | None = None
    credentialsExpiresReminderInDays: int | None = None
    credentialsExpiryAlert: bool | None = None
    dataEntryAutoGroup: bool | None = None
    deviceEnrollmentAllowedUserGroups: str | None = None
    deviceEnrollmentIATTtlSeconds: int | None = None
    deviceEnrollmentRedirectAllowlist: str | None = None
    emailConfigured: bool | None = None
    enforceVerifiedEmail: bool | None = None
    experimentalAnalyticsSqlEngineEnabled: bool | None = None
    factorDeviation: float | None = None
    globalShellAppName: str | None = None
    globalShellEnabled: bool | None = None
    googleAnalyticsUA: str | None = None
    helpPageLink: str | None = None
    hideUnapprovedDataInAnalytics: bool | None = None
    jobsCleanupAfterMinutes: int | None = None
    jobsLogDebugBelowSeconds: int | None = None
    jobsMaxCronDelayHours: int | None = None
    jobsRescheduleAfterMinutes: int | None = None
    keyAcceptanceRequiredForApproval: bool | None = None
    keyAccountRecovery: bool | None = None
    keyAllowObjectAssignment: bool | None = None
    keyAnalysisDigitGroupSeparator: DigitGroupSeparator | None = None
    keyAnalysisDisplayProperty: DisplayProperty | None = None
    keyAnalysisRelativePeriod: RelativePeriodEnum | None = None
    keyAnalyticsCacheProgressiveTtlFactor: int | None = None
    keyAnalyticsCacheTtlMode: AnalyticsCacheTtlMode | None = None
    keyAnalyticsDownloadCombinationLimit: int | None = None
    keyAnalyticsMaxLimit: int | None = None
    keyAnalyticsPeriodYearsOffset: int | None = None
    keyApplicationFooter: str | None = None
    keyApplicationIntro: str | None = None
    keyApplicationNotification: str | None = None
    keyApplicationRightFooter: str | None = None
    keyAzureMapsApiKey: str | None = None
    keyBingMapsApiKey: str | None = None
    keyCacheStrategy: CacheStrategy | None = None
    keyCacheability: Cacheability | None = None
    keyCalendar: str | None = None
    keyCanGrantOwnUserAuthorityGroups: bool | None = None
    keyCountPassiveDashboardViewsInUsageAnalytics: bool | None = None
    keyCurrentDomainType: str | None = None
    keyCustomColor: str | None = None
    keyCustomColorMobile: str | None = None
    keyCustomCss: str | None = None
    keyCustomJs: str | None = None
    keyCustomLoginPageLogo: bool | None = None
    keyCustomTopMenuLogo: bool | None = None
    keyCustomTranslationsEnabled: bool | None = None
    keyDashboardContextMenuItemOpenInRelevantApp: bool | None = None
    keyDashboardContextMenuItemShowInterpretationsAndDetails: bool | None = None
    keyDashboardContextMenuItemSwitchViewType: bool | None = None
    keyDashboardContextMenuItemViewFullscreen: bool | None = None
    keyDataImportRequireAttributeOptionCombo: bool | None = None
    keyDataImportStrictAttributeOptionCombos: bool | None = None
    keyDataImportStrictOrganisationUnits: bool | None = None
    keyDataImportStrictPeriods: bool | None = None
    keyDataQualityMaxLimit: int | None = None
    keyDatabaseServerCpus: int | None = None
    keyDateFormat: str | None = None
    keyDbLocale: str | None = None
    keyDefaultBaseMap: str | None = None
    keyEmailHostName: str | None = None
    keyEmailPassword: str | None = None
    keyEmailPort: int | None = None
    keyEmailSender: str | None = None
    keyEmailTls: bool | None = None
    keyEmailUsername: str | None = None
    keyEmbeddedDashboardsEnabled: bool | None = None
    keyFileResourceRetentionStrategy: FileResourceRetentionStrategy | None = None
    keyFlag: str | None = None
    keyFlagImage: str | None = None
    keyGatherAnalyticalObjectStatisticsInDashboardViews: bool | None = None
    keyGoogleMapsApiKey: str | None = None
    keyHideBiMonthlyPeriods: bool | None = None
    keyHideBiWeeklyPeriods: bool | None = None
    keyHideDailyPeriods: bool | None = None
    keyHideMonthlyPeriods: bool | None = None
    keyHideWeeklyPeriods: bool | None = None
    keyHtmlPushAnalyticsUrl: str | None = None
    keyIgnoreAnalyticsApprovalYearThreshold: int | None = None
    keyIncludeZeroValuesInAnalytics: bool | None = None
    keyLastCompleteDataSetRegistrationSyncSuccess: datetime | None = None
    keyLastMetaDataSyncSuccess: datetime | None = None
    keyLastMonitoringRun: datetime | None = None
    keyLastSuccessfulAnalyticsTablesRuntime: str | None = None
    keyLastSuccessfulAnalyticsTablesUpdate: datetime | None = None
    keyLastSuccessfulDataSynch: datetime | None = None
    keyLastSuccessfulEventsDataSynch: datetime | None = None
    keyLastSuccessfulLatestAnalyticsPartitionRuntime: str | None = None
    keyLastSuccessfulLatestAnalyticsPartitionUpdate: datetime | None = None
    keyLastSuccessfulMonitoring: datetime | None = None
    keyLastSuccessfulResourceTablesUpdate: datetime | None = None
    keyLastSuccessfulScheduledDataSetNotifications: datetime | None = None
    keyLastSuccessfulScheduledProgramNotifications: datetime | None = None
    keyLastSuccessfulSystemMonitoringPush: datetime | None = None
    keyLockMultipleFailedLogins: bool | None = None
    keyMetaDataRepoUrl: str | None = None
    keyMetadataFailedVersion: str | None = None
    keyMetadataLastFailedTime: datetime | None = None
    keyNextAnalyticsTableUpdate: datetime | None = None
    keyParallelJobsInAnalyticsTableExport: int | None = None
    keyRemoteInstancePassword: str | None = None
    keyRemoteInstanceUrl: str | None = None
    keyRemoteInstanceUsername: str | None = None
    keyRemoteMetadataVersion: str | None = None
    keyRequireAddToView: bool | None = None
    keyRespectMetaDataStartEndDatesInAnalyticsTableExport: bool | None = None
    keySelfRegistrationNoRecaptcha: bool | None = None
    keySkipDataTypeValidationInAnalyticsTableExport: bool | None = None
    keySmsMaxLength: int | None = None
    keySqlViewMaxLimit: int | None = None
    keyStopMetadataSync: bool | None = None
    keySystemMetadataVersion: str | None = None
    keySystemNotificationsEmail: str | None = None
    keyTrackerDashboardLayout: str | None = None
    keyUiLocale: str | None = None
    keyUseCustomLogoBanner: bool | None = None
    keyUseCustomLogoFront: bool | None = None
    keyVersionEnabled: bool | None = None
    lastSuccessfulDataStatistics: datetime | None = None
    loginPageLayout: LoginPageLayout | None = None
    loginPageTemplate: str | None = None
    loginPopup: str | None = None
    maxPasswordLength: int | None = None
    minPasswordLength: int | None = None
    notifierCleanAfterIdleTime: int | None = None
    notifierGistOverview: bool | None = None
    notifierLogLevel: NotificationLevel | None = None
    notifierMaxAgeDays: int | None = None
    notifierMaxJobsPerType: int | None = None
    notifierMaxMessagesPerJob: int | None = None
    orgUnitCentroidsInEventsAnalytics: bool | None = None
    phoneNumberAreaCode: str | None = None
    recaptchaSecret: str | None = None
    recaptchaSite: str | None = None
    ruleEngineAssignOverwrite: bool | None = None
    startModule: str | None = None
    startModuleEnableLightweight: bool | None = None
    syncDelayBetweenRemoteServerAvailabilityCheckAttempts: int | None = None
    syncMaxAttempts: int | None = None
    syncMaxRemoteServerAvailabilityCheckAttempts: int | None = None
    syncSkipSyncForDataChangedBefore: datetime | None = None
