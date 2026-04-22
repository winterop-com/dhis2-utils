"""FastMCP tool registration for the `apps` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import App, AppHubApp

from dhis2_core.plugins.apps import service
from dhis2_core.plugins.apps.models import UpdateOutcome, UpdateSummary
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `apps_*` tools on the MCP server."""

    @mcp.tool()
    async def apps_list(profile: str | None = None) -> list[App]:
        """List every installed DHIS2 app (`GET /api/apps`). Returns typed App records."""
        return await service.list_apps(resolve_profile(profile))

    @mcp.tool()
    async def apps_get(key: str, profile: str | None = None) -> App | None:
        """Return one installed app by `key`; None if not installed."""
        return await service.get_app(resolve_profile(profile), key)

    @mcp.tool()
    async def apps_install_from_file(path: str, profile: str | None = None) -> None:
        """Install / update an app from a local `.zip` at `path` (`POST /api/apps`)."""
        await service.install_from_file(resolve_profile(profile), path)

    @mcp.tool()
    async def apps_install_from_hub(version_id: str, profile: str | None = None) -> None:
        """Install an App Hub version (`POST /api/appHub/{versionId}`)."""
        await service.install_from_hub(resolve_profile(profile), version_id)

    @mcp.tool()
    async def apps_uninstall(key: str, profile: str | None = None) -> None:
        """Remove an installed app by `key` (`DELETE /api/apps/{key}`)."""
        await service.uninstall(resolve_profile(profile), key)

    @mcp.tool()
    async def apps_reload(profile: str | None = None) -> None:
        """Re-read every app from disk (`PUT /api/apps`). No new versions fetched."""
        await service.reload_apps(resolve_profile(profile))

    @mcp.tool()
    async def apps_hub_list(profile: str | None = None) -> list[AppHubApp]:
        """List apps available in the configured App Hub (`GET /api/appHub`)."""
        return await service.hub_list(resolve_profile(profile))

    @mcp.tool()
    async def apps_update(key: str, dry_run: bool = False, profile: str | None = None) -> UpdateOutcome:
        """Update a single installed app to its latest App Hub version.

        Pass `dry_run=True` to report whether a newer version exists without
        calling the install endpoint — outcome status is `AVAILABLE` when a
        newer hub version is present, `UP_TO_DATE` otherwise.
        """
        return await service.update_one(resolve_profile(profile), key, dry_run=dry_run)

    @mcp.tool()
    async def apps_update_all(dry_run: bool = False, profile: str | None = None) -> UpdateSummary:
        """Walk every installed app; install the latest App Hub version where available.

        Bundled core apps + side-loaded zips without an `app_hub_id` are
        reported as `SKIPPED` in the returned summary. `dry_run=True`
        tags available updates as `AVAILABLE` and skips every install POST.
        """
        return await service.update_all(resolve_profile(profile), dry_run=dry_run)
