"""Generated TrackedEntityType model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class TrackedEntityType(BaseModel):
    """DHIS2 TrackedEntityType resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    allowAuditLog: bool | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    displayTrackedEntityTypesLabel: str | None = None

    enableChangeLog: bool | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    featureType: str | None = None

    formName: str | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    maxTeiCountToReturn: int | None = None

    minAttributesRequiredToSearch: int | None = None

    name: str | None = None

    sharing: Any | None = None

    shortName: str | None = None

    style: Any | None = None

    trackedEntityTypeAttributes: list[Any] | None = None

    trackedEntityTypesLabel: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
