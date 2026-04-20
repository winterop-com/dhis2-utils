"""Async DHIS2 API client with pluggable auth and pydantic models."""

from dhis2_client.aggregate import DataValue, DataValueSet
from dhis2_client.analytics import AnalyticsHeader, AnalyticsMetaData, AnalyticsResponse
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
from dhis2_client.envelopes import (
    Conflict,
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
    Notification,
)
from dhis2_client.periods import PeriodType
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
from dhis2_client.system import DisplayRef, Me, SystemInfo, SystemModule
from dhis2_client.uids import UID_ALPHABET, UID_LENGTH, UID_LETTERS, UID_RE, generate_uid, generate_uids, is_valid_uid

__all__ = [
    "ACCESS_NONE",
    "ACCESS_READ_DATA",
    "ACCESS_READ_METADATA",
    "ACCESS_READ_WRITE_DATA",
    "ACCESS_READ_WRITE_METADATA",
    "AddOp",
    "AnalyticsHeader",
    "AnalyticsMetaData",
    "AnalyticsResponse",
    "ApiHeadersAuthScheme",
    "ApiQueryParamsAuthScheme",
    "ApiTokenAuthScheme",
    "AuthProvider",
    "AuthScheme",
    "AuthSchemeAdapter",
    "AuthenticationError",
    "BasicAuth",
    "Conflict",
    "CopyOp",
    "CustomizationResult",
    "CustomizeAccessor",
    "DataIntegrityCheck",
    "DataIntegrityIssue",
    "DataIntegrityReport",
    "DataIntegrityResult",
    "DataValue",
    "DataValueSet",
    "Dhis2",
    "Dhis2ApiError",
    "Dhis2Client",
    "Dhis2ClientError",
    "DisplayRef",
    "ErrorReport",
    "HttpBasicAuthScheme",
    "ImportCount",
    "ImportReport",
    "JsonPatchOp",
    "JsonPatchOpAdapter",
    "LoginCustomization",
    "Me",
    "MoveOp",
    "Notification",
    "OAuth2Auth",
    "OAuth2ClientCredentialsAuthScheme",
    "OAuth2FlowError",
    "OAuth2Token",
    "ObjectReport",
    "PatAuth",
    "PeriodType",
    "RemoveOp",
    "ReplaceOp",
    "Sharing",
    "SharingBuilder",
    "SharingObject",
    "Stats",
    "SystemInfo",
    "SystemModule",
    "TestOp",
    "TokenStore",
    "TypeReport",
    "UID_ALPHABET",
    "UID_LENGTH",
    "UID_LETTERS",
    "UID_RE",
    "UnsupportedVersionError",
    "WebMessageResponse",
    "access_string",
    "apply_sharing",
    "auth_scheme_from_route",
    "generate_uid",
    "generate_uids",
    "get_sharing",
    "is_valid_uid",
]
