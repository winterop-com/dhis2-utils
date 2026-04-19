"""Generated SMSCommand model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import CompletenessMethod, ParserType


class SMSCommand(BaseModel):
    """Generated model for DHIS2 `SMSCommand`.

    DHIS2 S M S Command - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/smsCommands.

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
    codeValueSeparator: str | None = None
    completenessMethod: CompletenessMethod | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    currentPeriodUsedForReporting: bool | None = None
    dataset: Reference | None = Field(default=None, description="Reference to DataSet. Read-only (inverse side).")
    defaultMessage: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    moreThanOneOrgUnitMessage: str | None = None
    name: str | None = None
    noUserMessage: str | None = None
    parserType: ParserType | None = None
    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")
    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )
    receivedMessage: str | None = None
    separator: str | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    smsCodes: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    specialCharacters: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    successMessage: str | None = None
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userGroup: Reference | None = Field(default=None, description="Reference to UserGroup. Read-only (inverse side).")
    wrongFormatMessage: str | None = None
