"""Generated SMSCommand model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import CompletenessMethod, ParserType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class SMSCommand(BaseModel):
    """DHIS2 S M S Command - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/smsCommands.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    code: str | None = None

    codeValueSeparator: str | None = Field(default=None, description="Length/value max=2147483647.")

    completenessMethod: CompletenessMethod | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    currentPeriodUsedForReporting: bool | None = None

    dataset: Reference | None = Field(default=None, description="Reference to DataSet.")

    defaultMessage: str | None = Field(default=None, description="Length/value max=2147483647.")

    displayName: str | None = Field(default=None, description="Read-only.")

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    moreThanOneOrgUnitMessage: str | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    noUserMessage: str | None = Field(default=None, description="Length/value max=2147483647.")

    parserType: ParserType | None = None

    program: Reference | None = Field(default=None, description="Reference to Program.")

    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    receivedMessage: str | None = Field(default=None, description="Length/value max=2147483647.")

    separator: str | None = Field(default=None, description="Length/value max=2147483647.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    smsCodes: list[Any] | None = Field(default=None, description="Collection of SMSCode.")

    specialCharacters: list[Any] | None = Field(default=None, description="Collection of SMSSpecialCharacter.")

    successMessage: str | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroup: Reference | None = Field(default=None, description="Reference to UserGroup.")

    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )

    wrongFormatMessage: str | None = Field(default=None, description="Length/value max=2147483647.")
