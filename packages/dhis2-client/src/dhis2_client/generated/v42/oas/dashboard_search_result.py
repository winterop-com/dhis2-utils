"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .app import App
    from .base_identifiable_object import BaseIdentifiableObject
    from .simple_event_visualization_view import SimpleEventVisualizationView
    from .simple_visualization_view import SimpleVisualizationView


class DashboardSearchResult(_BaseModel):
    """OpenAPI schema `DashboardSearchResult`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    appCount: int
    apps: list[App] | None = None
    eventChartCount: int
    eventCharts: list[BaseIdentifiableObject] | None = None
    eventReportCount: int
    eventReports: list[BaseIdentifiableObject] | None = None
    eventVisualizationCount: int
    eventVisualizations: list[SimpleEventVisualizationView] | None = None
    mapCount: int
    maps: list[BaseIdentifiableObject] | None = None
    reportCount: int
    reports: list[BaseIdentifiableObject] | None = None
    resourceCount: int
    resources: list[BaseIdentifiableObject] | None = None
    searchCount: int
    userCount: int
    users: list[BaseIdentifiableObject] | None = None
    visualizationCount: int
    visualizations: list[SimpleVisualizationView] | None = None
