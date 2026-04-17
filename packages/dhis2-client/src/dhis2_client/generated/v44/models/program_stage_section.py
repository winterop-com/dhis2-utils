"""Generated ProgramStageSection model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramStageSection(BaseModel):
    """DHIS2 ProgramStageSection resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataElements: list[Any] | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    programIndicators: list[Any] | None = None

    programStage: Reference | None = None

    renderType: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    sortOrder: int | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
