"""Generated ProgramRuleVariable model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramRuleVariable(BaseModel):
    """DHIS2 ProgramRuleVariable resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attribute: Reference | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataElement: Reference | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    program: Reference | None = None

    programStage: Reference | None = None

    sharing: Any | None = None

    sourceType: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    useCodeForOptionSet: bool | None = None

    user: Reference | None = None

    valueType: str | None = None
