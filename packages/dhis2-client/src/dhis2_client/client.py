"""Async DHIS2 client with pluggable auth and version-aware generated dispatch."""

from __future__ import annotations

import re
from types import ModuleType, TracebackType
from typing import Any, Self

import httpx
from pydantic import BaseModel

from dhis2_client.auth.base import AuthProvider
from dhis2_client.errors import AuthenticationError, Dhis2ApiError, UnsupportedVersionError
from dhis2_client.generated import available_versions, load
from dhis2_client.system import SystemModule

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")


class Dhis2Client:
    """Async DHIS2 client; version is discovered via /api/system/info on connect."""

    def __init__(
        self,
        base_url: str,
        auth: AuthProvider,
        *,
        timeout: float = 30.0,
        connect_timeout: float = 60.0,
        allow_version_fallback: bool = False,
    ) -> None:
        """Build a client. Call connect() or use as an async context manager before API calls."""
        self._base_url = base_url.rstrip("/")
        self._auth = auth
        self._timeout = httpx.Timeout(timeout, connect=connect_timeout)
        self._http: httpx.AsyncClient | None = None
        self._version_key: str | None = None
        self._raw_version: str | None = None
        self._generated: ModuleType | None = None
        self._allow_fallback = allow_version_fallback
        self._resources: Any = None
        self.system: SystemModule = SystemModule(self)

    @property
    def base_url(self) -> str:
        """Root URL of the connected DHIS2 instance."""
        return self._base_url

    @property
    def version_key(self) -> str:
        """Return the generated-client version key (e.g. "v42"); requires connect()."""
        if self._version_key is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")
        return self._version_key

    @property
    def raw_version(self) -> str:
        """Return the raw version string reported by the server (e.g. "2.42.0")."""
        if self._raw_version is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")
        return self._raw_version

    @property
    def resources(self) -> Any:
        """Return the version-bound generated `Resources` accessor; requires connect()."""
        if self._resources is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")
        return self._resources

    async def __aenter__(self) -> Self:
        """Open the HTTP pool and run version discovery."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Close the HTTP pool."""
        await self.close()

    async def connect(self) -> None:
        """Open the HTTP pool and bind the generated module matching the remote version."""
        if self._http is None:
            self._http = httpx.AsyncClient(base_url=self._base_url, timeout=self._timeout)
        info = await self.get_raw("/api/system/info")
        self._raw_version = str(info.get("version", ""))
        self._version_key = self._pick_version_key(self._raw_version)
        self._generated = load(self._version_key)
        resources_cls = getattr(self._generated, "Resources", None)
        if resources_cls is not None:
            self._resources = resources_cls(self)

    async def close(self) -> None:
        """Close the underlying HTTP pool."""
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    def _pick_version_key(self, version_str: str) -> str:
        """Select a generated module version key for the reported DHIS2 version."""
        match = _VERSION_RE.match(version_str)
        available = list(available_versions())
        if not match:
            raise UnsupportedVersionError(version=version_str or "unknown", available=available)
        minor = int(match.group(2))
        requested = f"v{minor}"
        if requested in available:
            return requested
        if not self._allow_fallback:
            raise UnsupportedVersionError(version=version_str, available=available)
        lower = [k for k in available if int(k[1:]) <= minor]
        if not lower:
            raise UnsupportedVersionError(version=version_str, available=available)
        return max(lower, key=lambda k: int(k[1:]))

    async def get_raw(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Raw GET returning parsed JSON; used internally and as an escape hatch."""
        response = await self._request("GET", path, params=params)
        return self._parse_json(response)

    async def get[T: BaseModel](
        self,
        path: str,
        model: type[T],
        params: dict[str, Any] | None = None,
    ) -> T:
        """Typed GET returning an instance of `model` parsed from JSON."""
        raw = await self.get_raw(path, params=params)
        return model.model_validate(raw)

    async def post_raw(self, path: str, body: Any = None) -> dict[str, Any]:
        """Raw POST returning parsed JSON."""
        response = await self._request("POST", path, json=body)
        return self._parse_json(response)

    async def put_raw(self, path: str, body: Any = None) -> dict[str, Any]:
        """Raw PUT returning parsed JSON."""
        response = await self._request("PUT", path, json=body)
        return self._parse_json(response)

    async def delete_raw(self, path: str) -> dict[str, Any]:
        """Raw DELETE returning parsed JSON (or empty dict)."""
        response = await self._request("DELETE", path)
        return self._parse_json(response)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> httpx.Response:
        """Dispatch a request through the shared pool with fresh auth headers."""
        if self._http is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")
        headers = await self._auth.headers()
        response = await self._http.request(method, path, params=params, json=json, headers=headers)
        if response.status_code == 401:
            raise AuthenticationError(f"401 Unauthorized at {method} {path}")
        if response.status_code >= 400:
            body: Any
            try:
                body = response.json()
            except ValueError:
                body = response.text
            raise Dhis2ApiError(status_code=response.status_code, message=response.reason_phrase, body=body)
        return response

    @staticmethod
    def _parse_json(response: httpx.Response) -> dict[str, Any]:
        """Parse a successful response body into a dict (wrapping non-dict JSON under "data")."""
        try:
            parsed = response.json()
        except ValueError:
            return {}
        if isinstance(parsed, dict):
            return parsed
        return {"data": parsed}
