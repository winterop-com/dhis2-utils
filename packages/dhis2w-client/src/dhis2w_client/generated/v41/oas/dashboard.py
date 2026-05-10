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
    from .dashboard_item import DashboardItem
    from .item_config import ItemConfig
    from .layout import Layout
    from .sharing import Sharing
    from .translation import Translation


class DashboardCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Dashboard(_BaseModel):
    """OpenAPI schema `Dashboard`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    allowedFilters: list[str] | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DashboardCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dashboardItems: list[DashboardItem] | None = None
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
    itemConfig: ItemConfig | None = None
    itemCount: int | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DashboardLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    layout: Layout | None = None
    name: str | None = None
    restrictFilters: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    user: DashboardUser | None = _Field(default=None, description="A UID reference to a User  ")
