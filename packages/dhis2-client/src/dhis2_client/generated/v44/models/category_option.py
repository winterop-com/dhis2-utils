"""Generated CategoryOption model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class CategoryOption(BaseModel):
    """DHIS2 CategoryOption resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    categories: list[Any] | None = None

    categoryOptionCombos: list[Any] | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    default: bool | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    endDate: datetime | None = None

    formName: str | None = None

    groups: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    organisationUnits: list[Any] | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    startDate: datetime | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
