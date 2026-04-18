"""Async DHIS2 API client with pluggable auth and pydantic models."""

from dhis2_client.auth.base import AuthProvider
from dhis2_client.auth.basic import BasicAuth
from dhis2_client.auth.oauth2 import OAuth2Auth, OAuth2Token, TokenStore
from dhis2_client.auth.pat import PatAuth
from dhis2_client.client import Dhis2Client
from dhis2_client.envelopes import (
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
from dhis2_client.system import Me, SystemInfo, SystemModule

__all__ = [
    "AuthProvider",
    "AuthenticationError",
    "BasicAuth",
    "Dhis2",
    "Dhis2ApiError",
    "Dhis2Client",
    "Dhis2ClientError",
    "ErrorReport",
    "ImportCount",
    "ImportReport",
    "Me",
    "OAuth2Auth",
    "OAuth2FlowError",
    "OAuth2Token",
    "ObjectReport",
    "PatAuth",
    "Stats",
    "SystemInfo",
    "SystemModule",
    "TokenStore",
    "TypeReport",
    "UnsupportedVersionError",
    "WebMessageResponse",
]
