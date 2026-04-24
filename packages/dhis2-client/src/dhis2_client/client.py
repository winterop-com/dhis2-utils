"""Async DHIS2 client with pluggable auth and version-aware generated dispatch."""

from __future__ import annotations

import logging
import re
import time
from types import ModuleType, TracebackType
from typing import Any, Self

import httpx
from pydantic import BaseModel

from dhis2_client.analytics_stream import AnalyticsAccessor
from dhis2_client.apps import AppsAccessor
from dhis2_client.attribute_values import AttributeValuesAccessor
from dhis2_client.auth.base import AuthProvider
from dhis2_client.category_option_group_sets import CategoryOptionGroupSetsAccessor
from dhis2_client.category_option_groups import CategoryOptionGroupsAccessor
from dhis2_client.category_options import CategoryOptionsAccessor
from dhis2_client.customize import CustomizeAccessor
from dhis2_client.dashboards import DashboardsAccessor
from dhis2_client.data_element_group_sets import DataElementGroupSetsAccessor
from dhis2_client.data_element_groups import DataElementGroupsAccessor
from dhis2_client.data_elements import DataElementsAccessor
from dhis2_client.data_sets import DataSetsAccessor
from dhis2_client.data_values import DataValuesAccessor
from dhis2_client.errors import AuthenticationError, Dhis2ApiError, UnsupportedVersionError
from dhis2_client.files import FilesAccessor
from dhis2_client.generated import Dhis2, available_versions, load
from dhis2_client.generated.v42.oas import SystemInfo as _SystemInfo
from dhis2_client.indicator_group_sets import IndicatorGroupSetsAccessor
from dhis2_client.indicator_groups import IndicatorGroupsAccessor
from dhis2_client.indicators import IndicatorsAccessor
from dhis2_client.legend_sets import LegendSetsAccessor
from dhis2_client.maintenance import MaintenanceAccessor
from dhis2_client.maps import MapsAccessor
from dhis2_client.messaging import MessagingAccessor
from dhis2_client.metadata import MetadataAccessor
from dhis2_client.option_sets import OptionSetsAccessor
from dhis2_client.organisation_unit_group_sets import OrganisationUnitGroupSetsAccessor
from dhis2_client.organisation_unit_groups import OrganisationUnitGroupsAccessor
from dhis2_client.organisation_unit_levels import OrganisationUnitLevelsAccessor
from dhis2_client.organisation_units import OrganisationUnitsAccessor
from dhis2_client.predictor_groups import PredictorGroupsAccessor
from dhis2_client.predictors import PredictorsAccessor
from dhis2_client.program_indicator_groups import ProgramIndicatorGroupsAccessor
from dhis2_client.program_indicators import ProgramIndicatorsAccessor
from dhis2_client.program_rules import ProgramRulesAccessor
from dhis2_client.programs import ProgramsAccessor
from dhis2_client.retry import RetryPolicy, build_retry_transport
from dhis2_client.sections import SectionsAccessor
from dhis2_client.sql_views import SqlViewsAccessor
from dhis2_client.system import SystemModule
from dhis2_client.system_cache import SystemCache
from dhis2_client.tasks import TaskModule
from dhis2_client.tracked_entity_attributes import TrackedEntityAttributesAccessor
from dhis2_client.tracked_entity_types import TrackedEntityTypesAccessor
from dhis2_client.tracker import TrackerAccessor
from dhis2_client.validation import ValidationAccessor
from dhis2_client.validation_rule_groups import ValidationRuleGroupsAccessor
from dhis2_client.validation_rules import ValidationRulesAccessor
from dhis2_client.visualizations import VisualizationsAccessor

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?")
_HTTP_LOG = logging.getLogger("dhis2_client.http")


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
        version: Dhis2 | None = Dhis2.V42,
        retry_policy: RetryPolicy | None = None,
        http_limits: httpx.Limits | None = None,
        system_cache_ttl: float | None = 300.0,
    ) -> None:
        """Build a client. Call connect() or use as an async context manager before API calls.

        `version` defaults to `Dhis2.V42` — the line we target across the
        workspace. Set explicitly (`Dhis2.V41`, `Dhis2.V44`, etc.) when
        targeting a different major, or pass `None` to let the client
        auto-detect via `/api/system/info` on `connect()`. Pinning skips
        that roundtrip and fails fast on a server version with no
        matching generated module.

        `retry_policy` (default: no retries) enables exponential-backoff
        retries on transient failures — connection errors plus the status
        codes listed on `RetryPolicy.retry_statuses` (default 429 / 502 /
        503 / 504). Non-idempotent methods (POST, PATCH) are exempt unless
        the policy sets `retry_non_idempotent=True`. See
        `dhis2_client.retry.RetryPolicy` for tuning knobs.

        `http_limits` overrides the httpx connection-pool defaults (100
        max connections, 20 keepalive). Raise them for high-concurrency
        batch workflows; lower them to protect a small DHIS2 instance
        from a large `asyncio.gather`. See
        `docs/architecture/client.md` for guidance.

        `system_cache_ttl` (default 300 s) caps how long cached system-level
        reads (`client.system.info()`, the default categoryCombo UID, and
        per-key system settings) stay fresh before the next call refetches.
        Pass `None` to disable the cache entirely. `connect()` primes the
        cache from the info fetch it already performs, so the first
        `client.system.info()` after connect costs zero round-trips.
        """
        self._base_url = base_url.rstrip("/")
        self._auth = auth
        self._timeout = httpx.Timeout(timeout, connect=connect_timeout)
        self._retry_policy = retry_policy
        self._http_limits = http_limits
        self._http: httpx.AsyncClient | None = None
        self._version_key: str | None = None
        self._raw_version: str | None = None
        self._generated: ModuleType | None = None
        self._allow_fallback = allow_version_fallback
        self._version = version
        self._resources: Any = None
        self._system_cache: SystemCache | None = (
            SystemCache(ttl=system_cache_ttl) if system_cache_ttl is not None else None
        )
        self.system: SystemModule = SystemModule(self)
        self.customize: CustomizeAccessor = CustomizeAccessor(self)
        self.tasks: TaskModule = TaskModule(self)
        self.maintenance: MaintenanceAccessor = MaintenanceAccessor(self)
        self.messaging: MessagingAccessor = MessagingAccessor(self)
        self.metadata: MetadataAccessor = MetadataAccessor(self)
        self.maps: MapsAccessor = MapsAccessor(self)
        self.files: FilesAccessor = FilesAccessor(self)
        self.legend_sets: LegendSetsAccessor = LegendSetsAccessor(self)
        self.validation: ValidationAccessor = ValidationAccessor(self)
        self.attribute_values: AttributeValuesAccessor = AttributeValuesAccessor(self)
        self.option_sets: OptionSetsAccessor = OptionSetsAccessor(self)
        self.organisation_units: OrganisationUnitsAccessor = OrganisationUnitsAccessor(self)
        self.organisation_unit_groups: OrganisationUnitGroupsAccessor = OrganisationUnitGroupsAccessor(self)
        self.organisation_unit_group_sets: OrganisationUnitGroupSetsAccessor = OrganisationUnitGroupSetsAccessor(self)
        self.organisation_unit_levels: OrganisationUnitLevelsAccessor = OrganisationUnitLevelsAccessor(self)
        self.predictors: PredictorsAccessor = PredictorsAccessor(self)
        self.program_rules: ProgramRulesAccessor = ProgramRulesAccessor(self)
        self.sql_views: SqlViewsAccessor = SqlViewsAccessor(self)
        self.visualizations: VisualizationsAccessor = VisualizationsAccessor(self)
        self.dashboards: DashboardsAccessor = DashboardsAccessor(self)
        self.data_values: DataValuesAccessor = DataValuesAccessor(self)
        self.analytics: AnalyticsAccessor = AnalyticsAccessor(self)
        self.tracker: TrackerAccessor = TrackerAccessor(self)
        self.apps: AppsAccessor = AppsAccessor(self)
        self.data_elements: DataElementsAccessor = DataElementsAccessor(self)
        self.data_element_groups: DataElementGroupsAccessor = DataElementGroupsAccessor(self)
        self.data_element_group_sets: DataElementGroupSetsAccessor = DataElementGroupSetsAccessor(self)
        self.indicators: IndicatorsAccessor = IndicatorsAccessor(self)
        self.indicator_groups: IndicatorGroupsAccessor = IndicatorGroupsAccessor(self)
        self.indicator_group_sets: IndicatorGroupSetsAccessor = IndicatorGroupSetsAccessor(self)
        self.program_indicators: ProgramIndicatorsAccessor = ProgramIndicatorsAccessor(self)
        self.program_indicator_groups: ProgramIndicatorGroupsAccessor = ProgramIndicatorGroupsAccessor(self)
        self.category_options: CategoryOptionsAccessor = CategoryOptionsAccessor(self)
        self.category_option_groups: CategoryOptionGroupsAccessor = CategoryOptionGroupsAccessor(self)
        self.category_option_group_sets: CategoryOptionGroupSetsAccessor = CategoryOptionGroupSetsAccessor(self)
        self.data_sets: DataSetsAccessor = DataSetsAccessor(self)
        self.sections: SectionsAccessor = SectionsAccessor(self)
        self.validation_rules: ValidationRulesAccessor = ValidationRulesAccessor(self)
        self.validation_rule_groups: ValidationRuleGroupsAccessor = ValidationRuleGroupsAccessor(self)
        self.predictor_groups: PredictorGroupsAccessor = PredictorGroupsAccessor(self)
        self.tracked_entity_attributes: TrackedEntityAttributesAccessor = TrackedEntityAttributesAccessor(self)
        self.tracked_entity_types: TrackedEntityTypesAccessor = TrackedEntityTypesAccessor(self)
        self.programs: ProgramsAccessor = ProgramsAccessor(self)

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

    @property
    def system_cache(self) -> SystemCache | None:
        """Per-client TTL cache for system-level reads; `None` when caching is disabled."""
        return self._system_cache

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
        resolved = await self._resolve_canonical_base_url(self._base_url)
        if resolved != self._base_url:
            self._base_url = resolved
        if self._http is None:
            kwargs: dict[str, Any] = {"base_url": self._base_url, "timeout": self._timeout}
            if self._retry_policy is not None:
                kwargs["transport"] = build_retry_transport(self._retry_policy)
            if self._http_limits is not None:
                kwargs["limits"] = self._http_limits
            self._http = httpx.AsyncClient(**kwargs)
        info = await self.get_raw("/api/system/info")
        self._raw_version = str(info.get("version", ""))
        if self._version is not None:
            # Caller asserted a version — skip auto-detection + fallback logic.
            self._version_key = self._version.value
        else:
            self._version_key = self._pick_version_key(self._raw_version)
        self._generated = load(self._version_key)
        # Prime the system cache with the info we already fetched so
        # `client.system.info()` right after connect is a free in-process read.
        if self._system_cache is not None:
            self._system_cache.set("info", _SystemInfo.model_validate(info))
        resources_cls = getattr(self._generated, "Resources", None)
        if resources_cls is not None:
            self._resources = resources_cls(self)

    @staticmethod
    async def _resolve_canonical_base_url(base_url: str) -> str:
        """Follow redirects (without auth) to find the canonical DHIS2 base URL.

        httpx strips Authorization headers on cross-host redirects as a security
        measure (it won't leak credentials to a host the user didn't target).
        DHIS2 `play.*` instances redirect `play.dhis2.org/dev` ->
        `play.im.dhis2.org/dev`, so every authenticated call would silently
        drop the Authorization header and get a 401.

        Resolve the chain once, unauthenticated, so subsequent requests go
        directly to the resolved host with credentials preserved.
        """
        candidate = base_url.rstrip("/")
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=10.0),
                follow_redirects=True,
            ) as probe:
                response = await probe.get(f"{candidate}/")
        except Exception:  # noqa: BLE001 — probe is best-effort; fall back to original URL
            return candidate
        final = str(response.url).rstrip("/")
        # Strip common DHIS2 login-page trailing paths so we land on the root.
        for suffix in ("/dhis-web-login", "/login", "/dhis-web-commons/security/login.action"):
            if final.endswith(suffix):
                return final[: -len(suffix)].rstrip("/")
        return final

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

    async def post_raw(self, path: str, body: Any = None, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Raw POST returning parsed JSON."""
        response = await self._request("POST", path, params=params, json=body)
        return self._parse_json(response)

    async def put_raw(self, path: str, body: Any = None, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Raw PUT returning parsed JSON."""
        response = await self._request("PUT", path, params=params, json=body)
        return self._parse_json(response)

    async def delete_raw(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Raw DELETE returning parsed JSON (or empty dict)."""
        response = await self._request("DELETE", path, params=params)
        return self._parse_json(response)

    async def patch_raw(
        self,
        path: str,
        body: Any,
        *,
        params: dict[str, Any] | None = None,
        content_type: str = "application/json-patch+json",
    ) -> dict[str, Any]:
        """Raw PATCH returning parsed JSON. Defaults to JSON Patch (RFC 6902) content type."""
        response = await self._request(
            "PATCH",
            path,
            params=params,
            json=body,
            extra_headers={"Content-Type": content_type},
        )
        return self._parse_json(response)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        content: httpx._types.RequestContent | None = None,
        files: dict[str, tuple[str, bytes, str]] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Dispatch a request through the shared pool with fresh auth headers."""
        if self._http is None:
            raise RuntimeError("Dhis2Client is not connected; call connect() first")
        headers = await self._auth.headers()
        if extra_headers:
            headers = {**headers, **extra_headers}
        t0 = time.monotonic()
        response = await self._http.request(
            method,
            path,
            params=params,
            json=json,
            content=content,
            files=files,
            headers=headers,
        )
        if _HTTP_LOG.isEnabledFor(logging.DEBUG):
            elapsed_ms = (time.monotonic() - t0) * 1000
            _HTTP_LOG.debug(
                "%s %s -> %d (%d bytes, %.0fms)",
                method,
                str(response.request.url),
                response.status_code,
                len(response.content),
                elapsed_ms,
            )
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
