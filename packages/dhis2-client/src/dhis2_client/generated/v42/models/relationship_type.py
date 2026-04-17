"""Generated RelationshipType model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class RelationshipType(BaseModel):
    """DHIS2 RelationshipType resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attributeValues: Any | None = None

    bidirectional: bool | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    description: str | None = None

    displayFromToName: str | None = None

    displayName: str | None = None

    displayToFromName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    fromConstraint: Any | None = None

    fromToName: str | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    name: str | None = None

    referral: bool | None = None

    sharing: Any | None = None

    toConstraint: Any | None = None

    toFromName: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
