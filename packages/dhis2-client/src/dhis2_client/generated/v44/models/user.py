"""Generated User model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class User(BaseModel):
    """DHIS2 User - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/users.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    accountExpiry: datetime | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    avatar: Reference | None = Field(default=None, description="Reference to FileResource. Read-only (inverse side).")

    birthday: datetime | None = None

    catDimensionConstraints: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    code: str | None = None

    cogsDimensionConstraints: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataViewMaxOrganisationUnitLevel: int | None = None

    dataViewOrganisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    disabled: bool | None = None

    displayName: str | None = None

    education: str | None = None

    email: str | None = None

    emailVerificationToken: str | None = None

    emailVerified: bool | None = None

    employer: str | None = None

    externalAuth: bool | None = None

    facebookMessenger: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    firstName: str | None = None

    gender: str | None = None

    groups: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    interests: str | None = None

    introduction: str | None = None

    invitation: bool | None = None

    jobTitle: str | None = None

    languages: str | None = None

    lastCheckedInterpretations: datetime | None = None

    lastLogin: datetime | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    ldapId: str | None = None

    name: str | None = None

    nationality: str | None = None

    openId: str | None = None

    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    password: str | None = None

    passwordLastUpdated: datetime | None = None

    phoneNumber: str | None = None

    selfRegistered: bool | None = None

    settings: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    skype: str | None = None

    surname: str | None = None

    teiSearchOrganisationUnits: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    telegram: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    twitter: str | None = None

    uid: str | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userRoles: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    username: str | None = None

    verifiedEmail: str | None = None

    welcomeMessage: str | None = None

    whatsApp: str | None = None
