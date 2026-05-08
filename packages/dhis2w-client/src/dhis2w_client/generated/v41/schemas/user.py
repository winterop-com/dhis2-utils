"""Generated User model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from .attribute_value import AttributeValue


class User(BaseModel):
    """Generated model for DHIS2 `User`.

    DHIS2 User - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/users.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    accountExpiry: datetime | None = None
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )
    avatar: Reference | None = Field(default=None, description="Reference to FileResource.")
    birthday: datetime | None = None
    catDimensionConstraints: list[Any] | None = Field(default=None, description="Collection of Category.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    cogsDimensionConstraints: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroupSet."
    )
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataViewMaxOrganisationUnitLevel: int | None = Field(default=None, description="Length/value max=2147483647.")
    dataViewOrganisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")
    disabled: bool | None = None
    displayName: str | None = Field(default=None, description="Read-only.")
    education: str | None = Field(default=None, description="Length/value max=2147483647.")
    email: str | None = Field(default=None, description="Length/value max=160.")
    employer: str | None = Field(default=None, description="Length/value max=160.")
    externalAuth: bool | None = None
    facebookMessenger: str | None = Field(default=None, description="Length/value max=255.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    firstName: str | None = Field(default=None, description="Length/value min=1, max=160.")
    gender: str | None = Field(default=None, description="Length/value max=50.")
    href: str | None = None
    id: str | None = Field(default=None, description="Length/value min=11, max=11.")
    interests: str | None = Field(default=None, description="Length/value max=2147483647.")
    introduction: str | None = Field(default=None, description="Length/value max=2147483647.")
    invitation: bool | None = None
    jobTitle: str | None = Field(default=None, description="Length/value max=160.")
    languages: str | None = Field(default=None, description="Length/value max=2147483647.")
    lastCheckedInterpretations: datetime | None = None
    lastLogin: datetime | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    ldapId: str | None = Field(default=None, description="Unique. Length/value max=2147483647.")
    name: str | None = Field(default=None, description="Length/value max=2147483647.")
    nationality: str | None = Field(default=None, description="Length/value max=160.")
    openId: str | None = Field(default=None, description="Length/value max=2147483647.")
    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")
    password: str | None = Field(default=None, description="Length/value max=60.")
    passwordLastUpdated: datetime | None = None
    phoneNumber: str | None = Field(default=None, description="Length/value max=80.")
    selfRegistered: bool | None = None
    settings: Any | None = Field(default=None, description="Reference to UserSettings. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    skype: str | None = Field(default=None, description="Length/value max=255.")
    surname: str | None = Field(default=None, description="Length/value min=1, max=160.")
    teiSearchOrganisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")
    telegram: str | None = Field(default=None, description="Length/value max=255.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    twitter: str | None = Field(default=None, description="Length/value max=255.")
    twoFactorEnabled: bool | None = Field(default=None, description="Read-only.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userCredentials: Any | None = Field(
        default=None, description="Reference to UserCredentialsDto. Read-only (inverse side)."
    )
    userGroups: list[Any] | None = Field(default=None, description="Collection of UserGroup. Read-only (inverse side).")
    userRoles: list[Any] | None = Field(default=None, description="Collection of UserRole.")
    username: str | None = Field(default=None, description="Unique. Length/value max=255.")
    welcomeMessage: str | None = Field(default=None, description="Length/value max=2147483647.")
    whatsApp: str | None = Field(default=None, description="Length/value max=255.")
