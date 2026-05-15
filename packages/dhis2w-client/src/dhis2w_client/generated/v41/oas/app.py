"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .app_activities import AppActivities
    from .app_developer import AppDeveloper
    from .app_icons import AppIcons
    from .app_settings import AppSettings


class App(_BaseModel):
    """OpenAPI schema `App`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    activities: AppActivities | None = None
    appState: (
        Literal[
            "OK",
            "INVALID_BUNDLED_APP_OVERRIDE",
            "INVALID_CORE_APP",
            "NAMESPACE_TAKEN",
            "INVALID_ZIP_FORMAT",
            "MISSING_MANIFEST",
            "INVALID_MANIFEST_JSON",
            "INSTALLATION_FAILED",
            "NOT_FOUND",
            "MISSING_SYSTEM_BASE_URL",
            "APPROVED",
            "PENDING",
            "NOT_APPROVED",
            "DELETION_IN_PROGRESS",
        ]
        | None
    ) = None
    appStorageSource: Literal["LOCAL", "JCLOUDS"] | None = None
    appType: Literal["APP", "RESOURCE", "DASHBOARD_WIDGET", "TRACKER_DASHBOARD_WIDGET"] | None = None
    app_hub_id: str | None = None
    authorities: list[str] | None = None
    baseUrl: str | None = None
    bundled: bool | None = None
    core_app: bool | None = None
    default_locale: str | None = None
    description: str | None = None
    developer: AppDeveloper | None = None
    folderName: str | None = None
    icons: AppIcons | None = None
    installs_allowed_from: list[str] | None = None
    key: str | None = None
    launchUrl: str | None = None
    launch_path: str | None = None
    name: str | None = None
    pluginLaunchUrl: str | None = None
    plugin_launch_path: str | None = None
    plugin_type: str | None = None
    settings: AppSettings | None = None
    short_name: str | None = None
    version: str | None = None
