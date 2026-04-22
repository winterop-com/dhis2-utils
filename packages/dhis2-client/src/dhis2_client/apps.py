"""DHIS2 apps + App Hub — `/api/apps` and `/api/appHub`.

Covers the installed-apps surface (list / install from zip / install from App
Hub / uninstall / reload-from-disk) plus read-only App Hub queries used by
the `update` verbs in the `apps` plugin.

Terminology:

- An **installed app** is a row DHIS2 returns from `GET /api/apps`. Its
  identifier is the folder name (`key`); that's what the DELETE endpoint
  takes. `app_hub_id` on the installed record matches the App Hub's own
  `id` so an `update` verb can locate the latest version.
- An **App Hub app** is a catalog entry under `GET /api/appHub`. Each has
  a list of `versions`, each with a unique `id` (the `versionId` the
  install endpoint takes).
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

from dhis2_client.generated.v42.oas import App
from dhis2_client.generated.v42.oas._enums import AppStatus, AppType

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


class AppHubVersion(BaseModel):
    """One version of an App Hub app — the install target for `POST /api/appHub/{versionId}`."""

    model_config = ConfigDict(extra="allow", populate_by_name=True, frozen=False)

    id: str | None = None
    version: str | None = None
    min_dhis2_version: str | None = None
    max_dhis2_version: str | None = None
    # DHIS2's App Hub returns epoch-millis integers here (e.g. 1747820526374);
    # the type is lax to absorb both shapes without a custom validator.
    created: int | str | None = None
    last_updated: int | str | None = None
    download_url: str | None = None
    channel: str | None = None


class AppHubApp(BaseModel):
    """One catalog entry from `GET /api/appHub` — the App Hub's view of an app."""

    model_config = ConfigDict(extra="allow", populate_by_name=True, frozen=False)

    id: str | None = None
    name: str | None = None
    app_type: str | None = None
    description: str | None = None
    developer: dict[str, Any] | None = None
    icons: dict[str, Any] | None = None
    versions: list[AppHubVersion] = []


class AppsAccessor:
    """`Dhis2Client.apps` — list / install / uninstall / reload + App Hub queries."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_apps(self) -> list[App]:
        """Return every installed app — `GET /api/apps`.

        The response body is a bare JSON array (no envelope key), so
        `get_raw` wraps it under `"data"` — unwrapping is a one-liner.
        Every row becomes a typed `App`; extra fields DHIS2 tacks on in
        minor versions ride through via `model_config = extra="allow"`.
        """
        raw = await self._client.get_raw("/api/apps")
        rows = _unwrap_array(raw)
        return [App.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, key: str) -> App | None:
        """Find one installed app by `key` (folder name). Returns None if not installed."""
        for app in await self.list_apps():
            if app.key == key:
                return app
        return None

    async def install_from_file(self, path: Path | str, *, filename: str | None = None) -> None:
        """Upload an `.zip` to `POST /api/apps` — installs or updates in place.

        DHIS2 accepts multipart/form-data with a single `file` field. On
        success the endpoint returns 204 No Content (or a thin JSON body);
        the caller then calls `list()` again to see the new row.
        `filename` overrides the on-the-wire filename (defaults to the
        local path's basename).
        """
        file_path = Path(path)
        if not file_path.is_file():
            raise FileNotFoundError(f"no such app zip: {file_path}")
        data = file_path.read_bytes()
        resolved_filename = filename or file_path.name
        await self._client._request(  # noqa: SLF001 — accessor is tight with the client
            "POST",
            "/api/apps",
            files={"file": (resolved_filename, data, "application/zip")},
        )

    async def install_from_hub(self, version_id: str) -> None:
        """Install a specific App Hub version — `POST /api/appHub/{versionId}`.

        DHIS2 streams the app zip from the App Hub server-side, so the
        local caller only supplies the `versionId` (usually a UUID the
        App Hub hands out). On success the installed row is returned
        from the next `list()` call.
        """
        if not version_id:
            raise ValueError("install_from_hub requires a non-empty version_id")
        await self._client.post_raw(f"/api/appHub/{version_id}")

    async def uninstall(self, key: str) -> None:
        """Remove an installed app by `key` — `DELETE /api/apps/{key}`."""
        if not key:
            raise ValueError("uninstall requires a non-empty app key")
        await self._client.delete_raw(f"/api/apps/{key}")

    async def reload(self) -> None:
        """Re-read every app from disk — `PUT /api/apps`. No new versions are fetched."""
        await self._client.put_raw("/api/apps")

    async def hub_list(self, *, query: str | None = None) -> list[AppHubApp]:
        """List every app in the configured App Hub — `GET /api/appHub`.

        DHIS2 proxies this call to the App Hub server the instance is
        pointed at (typically `apps.dhis2.org`, configurable via the
        `keyAppHubUrl` system setting). The response is a JSON array of
        hub-app records; each has a `versions` list whose `id` fields
        are install targets for `install_from_hub(version_id)`.

        `query` applies a case-insensitive substring filter on `name` +
        `description` after the full catalog lands — the App Hub proxy
        doesn't expose a server-side query parameter in v42, so the
        filter is client-side.
        """
        raw = await self._client.get_raw("/api/appHub")
        rows = _unwrap_array(raw)
        catalog = [AppHubApp.model_validate(row) for row in rows if isinstance(row, dict)]
        if not query:
            return catalog
        needle = query.lower()
        return [
            app
            for app in catalog
            if (app.name and needle in app.name.lower()) or (app.description and needle in app.description.lower())
        ]

    async def get_hub_url(self) -> str | None:
        """Return the configured App Hub URL (`keyAppHubUrl` system setting) or None if unset.

        When None, DHIS2 falls back to its hard-coded default
        (`https://apps.dhis2.org/api` on v42). The App Hub is open
        source (https://github.com/dhis2/app-hub); self-hosters can
        point their instance at a private catalog by setting this.
        """
        return await self._client.system.setting("keyAppHubUrl", use_cache=False)

    async def set_hub_url(self, url: str | None) -> None:
        """Set the `keyAppHubUrl` system setting — points DHIS2 at a different App Hub.

        Passing `None` clears the setting (server reverts to its
        hard-coded default). Any HTTP call that hits `/api/appHub` on
        this instance after this write uses the new URL.
        """
        await self._client.system.set_setting("keyAppHubUrl", url)


def _unwrap_array(raw: Any) -> list[Any]:
    """Unwrap a bare-array JSON response that `get_raw` wrapped as `{"data": [...]}`."""
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        data = raw.get("data")
        if isinstance(data, list):
            return data
    return []


__all__ = [
    "App",
    "AppHubApp",
    "AppHubVersion",
    "AppStatus",
    "AppType",
    "AppsAccessor",
]
