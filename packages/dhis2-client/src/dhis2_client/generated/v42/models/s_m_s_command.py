"""Generated SMSCommand model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class SMSCommand(BaseModel):
    """DHIS2 SMSCommand resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    codeValueSeparator: str | None = None

    codes: list[Any] | None = None

    completenessMethod: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    currentPeriodUsedForReporting: bool | None = None

    dataset: Reference | None = None

    defaultMessage: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    moreThanOneOrgUnitMessage: str | None = None

    name: str | None = None

    noUserMessage: str | None = None

    parserType: str | None = None

    program: Reference | None = None

    programStage: Reference | None = None

    receivedMessage: str | None = None

    separator: str | None = None

    sharing: Any | None = None

    specialCharacters: list[Any] | None = None

    successMessage: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    userGroup: Reference | None = None

    wrongFormatMessage: str | None = None
