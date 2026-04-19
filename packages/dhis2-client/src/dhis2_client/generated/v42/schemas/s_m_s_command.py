"""Generated SMSCommand model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import CompletenessMethod, ParserType


class SMSCommand(BaseModel):
    """Generated model for DHIS2 `SMSCommand`.

    DHIS2 S M S Command - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/smsCommands.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
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
    userGroup: Reference | None = Field(default=None, description="Reference to UserGroup.")
    wrongFormatMessage: str | None = Field(default=None, description="Length/value max=2147483647.")
