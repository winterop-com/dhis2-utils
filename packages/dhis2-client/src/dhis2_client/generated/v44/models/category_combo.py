"""Generated CategoryCombo model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class CategoryCombo(BaseModel):
    """DHIS2 CategoryCombo resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    categories: list[Any] | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataDimensionType: str | None = None

    default: bool | None = None

    displayName: str | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    optionCombos: list[Any] | None = None

    sharing: Any | None = None

    skipTotal: bool | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
