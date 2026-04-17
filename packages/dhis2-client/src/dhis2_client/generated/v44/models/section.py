"""Generated Section model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Section(BaseModel):
    """DHIS2 Section resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    categoryCombos: list[Any] | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataElements: list[Any] | None = None

    dataSet: Reference | None = None

    description: str | None = None

    disableDataElementAutoGroup: bool | None = None

    displayName: str | None = None

    displayOptions: str | None = None

    greyedFields: list[Any] | None = None

    href: str | None = None

    indicators: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    sharing: Any | None = None

    showColumnTotals: bool | None = None

    showRowTotals: bool | None = None

    sortOrder: int | None = None

    translations: list[Any] | None = None

    uid: str | None = None
