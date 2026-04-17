"""Generated User model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class User(BaseModel):
    """DHIS2 User resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    accountExpiry: datetime | None = None

    attributeValues: Any | None = None

    avatar: Reference | None = None

    birthday: datetime | None = None

    catDimensionConstraints: list[Any] | None = None

    code: str | None = None

    cogsDimensionConstraints: list[Any] | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataViewMaxOrganisationUnitLevel: int | None = None

    dataViewOrganisationUnits: list[Any] | None = None

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

    favorites: list[Any] | None = None

    firstName: str | None = None

    gender: str | None = None

    groups: list[Any] | None = None

    href: str | None = None

    interests: str | None = None

    introduction: str | None = None

    invitation: bool | None = None

    jobTitle: str | None = None

    languages: str | None = None

    lastCheckedInterpretations: datetime | None = None

    lastLogin: datetime | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    ldapId: str | None = None

    name: str | None = None

    nationality: str | None = None

    openId: str | None = None

    organisationUnits: list[Any] | None = None

    password: str | None = None

    passwordLastUpdated: datetime | None = None

    phoneNumber: str | None = None

    selfRegistered: bool | None = None

    settings: Any | None = None

    sharing: Any | None = None

    skype: str | None = None

    surname: str | None = None

    teiSearchOrganisationUnits: list[Any] | None = None

    telegram: str | None = None

    translations: list[Any] | None = None

    twitter: str | None = None

    uid: str | None = None

    user: Reference | None = None

    userRoles: list[Any] | None = None

    username: str | None = None

    verifiedEmail: str | None = None

    welcomeMessage: str | None = None

    whatsApp: str | None = None
