"""Async DHIS2 API client with pluggable auth and pydantic models."""

from dhis2_client.aggregate import DataValue, DataValueSet
from dhis2_client.analytics import AnalyticsMetaData, Grid, GridHeader
from dhis2_client.analytics_stream import AnalyticsAccessor
from dhis2_client.apps import App, AppHubApp, AppHubVersion, AppsAccessor, AppStatus, AppType
from dhis2_client.attribute_values import AttributeValuesAccessor
from dhis2_client.auth.base import AuthProvider
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.auth.oauth2 import OAuth2Auth, OAuth2Token, TokenStore
from dhis2_client.auth.pat import PatAuth
from dhis2_client.auth_schemes import (
    ApiHeadersAuthScheme,
    ApiQueryParamsAuthScheme,
    ApiTokenAuthScheme,
    AuthScheme,
    AuthSchemeAdapter,
    HttpBasicAuthScheme,
    OAuth2ClientCredentialsAuthScheme,
    auth_scheme_from_route,
)
from dhis2_client.client import Dhis2Client
from dhis2_client.customize import CustomizationResult, CustomizeAccessor, LoginCustomization
from dhis2_client.dashboards import DashboardsAccessor, DashboardSlot
from dhis2_client.data_values import DataValuesAccessor
from dhis2_client.envelopes import (
    Conflict,
    ConflictRow,
    ErrorReport,
    ImportCount,
    ImportReport,
    ObjectReport,
    Stats,
    TypeReport,
    WebMessageResponse,
)
from dhis2_client.errors import (
    AuthenticationError,
    Dhis2ApiError,
    Dhis2ClientError,
    OAuth2FlowError,
    UnsupportedVersionError,
)
from dhis2_client.files import Document, FileResource, FileResourceDomain, FilesAccessor
from dhis2_client.generated import Dhis2
from dhis2_client.json_patch import (
    AddOp,
    CopyOp,
    JsonPatchOp,
    JsonPatchOpAdapter,
    MoveOp,
    RemoveOp,
    ReplaceOp,
    TestOp,
)
from dhis2_client.maintenance import (
    DataIntegrityCheck,
    DataIntegrityIssue,
    DataIntegrityReport,
    DataIntegrityResult,
    IntegrityIssueRow,
    JobType,
    MaintenanceAccessor,
    Notification,
    NotificationDataType,
    NotificationLevel,
)
from dhis2_client.maps import LayerKind, MapLayerSpec, MapsAccessor, MapSpec
from dhis2_client.messaging import MessageConversation, MessagingAccessor, Recipient
from dhis2_client.metadata import MetadataAccessor, SearchHit, SearchResults
from dhis2_client.option_sets import OptionSetsAccessor, OptionSpec, UpsertReport
from dhis2_client.periods import PeriodType, RelativePeriod
from dhis2_client.predictors import PredictorsAccessor
from dhis2_client.program_rules import ProgramRulesAccessor
from dhis2_client.retry import RetryPolicy
from dhis2_client.sharing import (
    ACCESS_NONE,
    ACCESS_READ_DATA,
    ACCESS_READ_METADATA,
    ACCESS_READ_WRITE_DATA,
    ACCESS_READ_WRITE_METADATA,
    Sharing,
    SharingBuilder,
    SharingObject,
    access_string,
    apply_sharing,
    get_sharing,
)
from dhis2_client.sql_views import (
    SqlViewColumn,
    SqlViewResult,
    SqlViewRunner,
    SqlViewsAccessor,
)
from dhis2_client.system import DisplayRef, Me, SystemInfo, SystemModule
from dhis2_client.system_cache import SystemCache
from dhis2_client.tasks import TaskCompletion, TaskModule, TaskTimeoutError, parse_task_ref
from dhis2_client.tracker import (
    EnrollResult,
    EventResult,
    OutstandingEnrollment,
    RegisterResult,
    TrackerAccessor,
)
from dhis2_client.uids import UID_ALPHABET, UID_LENGTH, UID_LETTERS, UID_RE, generate_uid, generate_uids, is_valid_uid
from dhis2_client.validation import (
    ExpressionContext,
    ExpressionDescription,
    ValidationAccessor,
    ValidationAnalysisResult,
)
from dhis2_client.visualizations import DimensionAxis, VisualizationsAccessor, VisualizationSpec

__all__ = [
    "ACCESS_NONE",
    "ACCESS_READ_DATA",
    "ACCESS_READ_METADATA",
    "ACCESS_READ_WRITE_DATA",
    "ACCESS_READ_WRITE_METADATA",
    "AddOp",
    "AnalyticsAccessor",
    "AnalyticsMetaData",
    "ApiHeadersAuthScheme",
    "ApiQueryParamsAuthScheme",
    "ApiTokenAuthScheme",
    "App",
    "AppHubApp",
    "AppHubVersion",
    "AppStatus",
    "AppType",
    "AppsAccessor",
    "AttributeValuesAccessor",
    "AuthProvider",
    "AuthScheme",
    "AuthSchemeAdapter",
    "AuthenticationError",
    "BasicAuth",
    "Conflict",
    "ConflictRow",
    "CopyOp",
    "CustomizationResult",
    "CustomizeAccessor",
    "DashboardSlot",
    "DashboardsAccessor",
    "DataIntegrityCheck",
    "DataIntegrityIssue",
    "DataIntegrityReport",
    "DataIntegrityResult",
    "DataValue",
    "DataValueSet",
    "DataValuesAccessor",
    "Dhis2",
    "Dhis2ApiError",
    "Dhis2Client",
    "Dhis2ClientError",
    "DimensionAxis",
    "DisplayRef",
    "Document",
    "EnrollResult",
    "ErrorReport",
    "EventResult",
    "ExpressionContext",
    "ExpressionDescription",
    "FileResource",
    "FileResourceDomain",
    "FilesAccessor",
    "Grid",
    "GridHeader",
    "HttpBasicAuthScheme",
    "ImportCount",
    "ImportReport",
    "IntegrityIssueRow",
    "JobType",
    "JsonPatchOp",
    "JsonPatchOpAdapter",
    "LayerKind",
    "LoginCustomization",
    "MaintenanceAccessor",
    "MapLayerSpec",
    "MapSpec",
    "MapsAccessor",
    "Me",
    "MessageConversation",
    "MessagingAccessor",
    "MetadataAccessor",
    "MoveOp",
    "Notification",
    "NotificationDataType",
    "NotificationLevel",
    "OAuth2Auth",
    "OAuth2ClientCredentialsAuthScheme",
    "OAuth2FlowError",
    "OAuth2Token",
    "ObjectReport",
    "OptionSetsAccessor",
    "OptionSpec",
    "OutstandingEnrollment",
    "PatAuth",
    "PeriodType",
    "PredictorsAccessor",
    "ProgramRulesAccessor",
    "Recipient",
    "RegisterResult",
    "RelativePeriod",
    "RemoveOp",
    "ReplaceOp",
    "RetryPolicy",
    "SearchHit",
    "SearchResults",
    "Sharing",
    "SharingBuilder",
    "SharingObject",
    "SqlViewColumn",
    "SqlViewResult",
    "SqlViewRunner",
    "SqlViewsAccessor",
    "Stats",
    "SystemCache",
    "SystemInfo",
    "SystemModule",
    "TaskCompletion",
    "TaskModule",
    "TaskTimeoutError",
    "TestOp",
    "TokenStore",
    "TrackerAccessor",
    "TypeReport",
    "UID_ALPHABET",
    "UID_LENGTH",
    "UID_LETTERS",
    "UID_RE",
    "UnsupportedVersionError",
    "UpsertReport",
    "ValidationAccessor",
    "ValidationAnalysisResult",
    "VisualizationSpec",
    "VisualizationsAccessor",
    "WebMessageResponse",
    "access_string",
    "apply_sharing",
    "auth_scheme_from_route",
    "generate_uid",
    "generate_uids",
    "get_sharing",
    "is_valid_uid",
    "parse_task_ref",
]
