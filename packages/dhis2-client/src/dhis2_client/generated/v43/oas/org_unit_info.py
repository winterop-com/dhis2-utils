"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import FeatureType


class OrgUnitInfo(_BaseModel):
    """OpenAPI schema `OrgUnitInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    address: str | None = None
    closedDate: datetime | None = None
    code: str | None = None
    comment: str | None = None
    contactPerson: str | None = None
    description: str | None = None
    email: str | None = None
    featureType: FeatureType | None = None
    id: str | None = None
    imageId: str | None = None
    latitude: float | None = None
    level: int | None = None
    levelName: str | None = None
    longitude: float | None = None
    name: str | None = None
    openingDate: datetime | None = None
    parentName: str | None = None
    phoneNumber: str | None = None
    shortName: str | None = None
    url: str | None = None
