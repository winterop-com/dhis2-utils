"""Generated DataApprovalWorkflow model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataApprovalWorkflow(BaseModel):
    """DHIS2 DataApprovalWorkflow resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    categoryCombo: Reference | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataSets: list[Any] | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    levels: list[Any] | None = None

    name: str | None = None

    periodType: str | None = None

    sharing: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
