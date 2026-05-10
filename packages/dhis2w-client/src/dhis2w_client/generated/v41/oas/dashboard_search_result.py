"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .app import App


class DashboardSearchResultEventCharts(_BaseModel):
    """A UID reference to a EventVisualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultEventReports(_BaseModel):
    """A UID reference to a EventVisualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultEventVisualizations(_BaseModel):
    """A UID reference to a SimpleEventVisualizationView  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultMaps(_BaseModel):
    """A UID reference to a Map  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultReports(_BaseModel):
    """A UID reference to a Report  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultResources(_BaseModel):
    """A UID reference to a Document  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultUsers(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResultVisualizations(_BaseModel):
    """A UID reference to a SimpleVisualizationView  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DashboardSearchResult(_BaseModel):
    """OpenAPI schema `DashboardSearchResult`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    appCount: int | None = None
    apps: list[App] | None = None
    eventChartCount: int | None = None
    eventCharts: list[DashboardSearchResultEventCharts] | None = None
    eventReportCount: int | None = None
    eventReports: list[DashboardSearchResultEventReports] | None = None
    eventVisualizationCount: int | None = None
    eventVisualizations: list[DashboardSearchResultEventVisualizations] | None = None
    mapCount: int | None = None
    maps: list[DashboardSearchResultMaps] | None = None
    reportCount: int | None = None
    reports: list[DashboardSearchResultReports] | None = None
    resourceCount: int | None = None
    resources: list[DashboardSearchResultResources] | None = None
    searchCount: int | None = None
    userCount: int | None = None
    users: list[DashboardSearchResultUsers] | None = None
    visualizationCount: int | None = None
    visualizations: list[DashboardSearchResultVisualizations] | None = None
