"""Generated ProgramRule model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramRule(BaseModel):
    """DHIS2 ProgramRule resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    condition: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    priority: int | None = None

    program: Reference | None = None

    programRuleActions: list[Any] | None = None

    programStage: Reference | None = None

    sharing: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
