"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AppStatus, AppStorageSource, AppType

if TYPE_CHECKING:
    from .app_activities import AppActivities
    from .app_developer import AppDeveloper
    from .app_icons import AppIcons
    from .app_settings import AppSettings
    from .app_shortcut import AppShortcut


class App(_BaseModel):
    """OpenAPI schema `App`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    activities: AppActivities
    appState: AppStatus
    appStorageSource: AppStorageSource
    appType: AppType
    app_hub_id: str | None = None
    authorities: list[str] | None = None
    basePath: str | None = None
    baseUrl: str | None = None
    bundled: bool | None = None
    core_app: bool | None = None
    default_locale: str | None = None
    description: str | None = None
    developer: AppDeveloper | None = None
    displayDescription: str | None = None
    displayName: str | None = None
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
    shortcuts: list[AppShortcut] | None = None
    version: str | None = None
