"""Generated UserCredentialsDto model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class UserCredentialsDto(BaseModel):
    """Generated model for DHIS2 `UserCredentialsDto`.

    DHIS2 User Credentials Dto - DHIS2 resource (generated from /api/schemas at DHIS2 v40).

    Transient — not stored in the DHIS2 database (computed / projection).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    accountExpiry: datetime | None = None
    catDimensionConstraints: list[Any] | None = Field(
        default=None, description="Collection of Category. Read-only (inverse side)."
    )
    cogsDimensionConstraints: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroupSet. Read-only (inverse side)."
    )
    disabled: bool | None = None
    externalAuth: bool | None = None
    id: str | None = Field(default=None, description="Length/value max=2147483647.")
    idToken: str | None = Field(default=None, description="Length/value max=2147483647.")
    invitation: bool | None = None
    lastLogin: datetime | None = None
    ldapId: str | None = Field(default=None, description="Length/value max=2147483647.")
    openId: str | None = Field(default=None, description="Length/value max=2147483647.")
    password: str | None = Field(default=None, description="Length/value max=2147483647.")
    passwordLastUpdated: datetime | None = None
    previousPasswords: list[Any] | None = Field(
        default=None, description="Collection of String. Read-only (inverse side)."
    )
    restoreExpiry: datetime | None = None
    restoreToken: str | None = Field(default=None, description="Length/value max=2147483647.")
    selfRegistered: bool | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    twoFA: bool | None = None
    userRoles: list[Any] | None = Field(default=None, description="Collection of UserRole. Read-only (inverse side).")
    username: str | None = Field(default=None, description="Length/value max=2147483647.")
    uuid: str | None = Field(default=None, description="Length/value max=2147483647.")
