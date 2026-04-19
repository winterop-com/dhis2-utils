"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .map_view import MapView
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Map(_BaseModel):
    """OpenAPI schema `Map`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    basemap: str | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[BaseIdentifiableObject] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    latitude: float | None = None
    longitude: float | None = None
    mapViews: list[MapView] | None = None
    name: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    title: str | None = None
    translations: list[Translation] | None = None
    zoom: int | None = None
