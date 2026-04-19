"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .dashboard_item_params import DashboardItemParams
    from .embedded_dashboard import EmbeddedDashboard
    from .item_config import ItemConfig
    from .layout import Layout
    from .sharing import Sharing
    from .translation import Translation


class DashboardParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DashboardParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DashboardParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardParams(_BaseModel):
    """OpenAPI schema `DashboardParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowedFilters: list[str] | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DashboardParamsCreatedBy | None = None
    dashboardItems: list[DashboardItemParams] | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    embedded: EmbeddedDashboard | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    itemConfig: ItemConfig | None = None
    itemCount: int | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DashboardParamsLastUpdatedBy | None = None
    layout: Layout | None = None
    name: str | None = None
    restrictFilters: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
