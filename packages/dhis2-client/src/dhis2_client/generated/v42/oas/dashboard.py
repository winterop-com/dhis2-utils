"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .embedded_dashboard import EmbeddedDashboard
    from .item_config import ItemConfig
    from .layout import Layout
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Dashboard(_BaseModel):
    """OpenAPI schema `Dashboard`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    allowedFilters: list[str] | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dashboardItems: list[BaseIdentifiableObject] | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    embedded: EmbeddedDashboard | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    itemConfig: ItemConfig | None = None
    itemCount: int | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    layout: Layout | None = None
    name: str | None = None
    restrictFilters: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
