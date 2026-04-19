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
from dhis2_client.maintenance import (
    DataIntegrityCheck,
    DataIntegrityIssue,
    DataIntegrityReport,
    DataIntegrityResult,
    Notification,
)
from dhis2_client.periods import PeriodType
from dhis2_client.system import Me, SystemInfo, SystemModule
from dhis2_client.tracker import (
    EnrollmentStatus,
    EventStatus,
    TrackerAttributeValue,
    TrackerBundle,
    TrackerDataValue,
    TrackerEnrollment,
    TrackerEvent,
    TrackerNote,
    TrackerRelationship,
    TrackerRelationshipItem,
    TrackerTrackedEntity,
)
from dhis2_client.uids import UID_ALPHABET, UID_LENGTH, UID_LETTERS, UID_RE, generate_uid, generate_uids, is_valid_uid

__all__ = [
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
    "EnrollmentStatus",
    "ErrorReport",
    "EventStatus",
    "HttpBasicAuthScheme",
    "ImportCount",
    "ImportReport",
    "Me",
    "Notification",
    "OAuth2Auth",
    "OAuth2ClientCredentialsAuthScheme",
    "OAuth2FlowError",
    "OAuth2Token",
    "ObjectReport",
    "PatAuth",
    "PeriodType",
    "Stats",
    "SystemInfo",
    "SystemModule",
    "TokenStore",
    "TrackerAttributeValue",
    "TrackerBundle",
    "TrackerDataValue",
    "TrackerEnrollment",
    "TrackerEvent",
    "TrackerNote",
    "TrackerRelationship",
    "TrackerRelationshipItem",
    "TrackerTrackedEntity",
    "TypeReport",
    "UID_ALPHABET",
    "UID_LENGTH",
    "UID_LETTERS",
    "UID_RE",
    "UnsupportedVersionError",
    "WebMessageResponse",
    "auth_scheme_from_route",
    "generate_uid",
    "generate_uids",
    "is_valid_uid",
]
