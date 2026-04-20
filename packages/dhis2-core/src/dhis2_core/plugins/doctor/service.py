"""Service layer for the `doctor` plugin — probe a DHIS2 instance for known gotchas.

Every probe is a pure read: no mutations, safe to run against production. Each
returns a `ProbeResult` with a status (`pass` | `warn` | `fail`), a one-line
message, optional BUGS.md cross-reference, and optional detail for follow-up.

`run_doctor` dispatches every probe concurrently (they're independent HTTP
GETs) and assembles a `DoctorReport` with a summary count. The CLI + MCP
layers render it; the report itself is pure pydantic so callers can consume
it programmatically.
"""

from __future__ import annotations

import asyncio
from typing import Literal

from dhis2_client import Dhis2ApiError, Dhis2Client
from pydantic import BaseModel, ConfigDict, Field

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_MIN_DHIS2_VERSION: tuple[int, int] = (2, 42)

ProbeStatus = Literal["pass", "warn", "fail", "skip"]


class ProbeResult(BaseModel):
    """Outcome of one doctor probe."""

    model_config = ConfigDict(frozen=True)

    name: str
    status: ProbeStatus
    message: str
    bugs_ref: str | None = None
    detail: str | None = None


class DoctorReport(BaseModel):
    """Aggregate of every probe run against an instance."""

    profile_name: str | None = None
    base_url: str
    dhis2_version: str | None = None
    probes: list[ProbeResult] = Field(default_factory=list)

    @property
    def pass_count(self) -> int:
        """Number of `pass` probes."""
        return sum(1 for probe in self.probes if probe.status == "pass")

    @property
    def warn_count(self) -> int:
        """Number of `warn` probes."""
        return sum(1 for probe in self.probes if probe.status == "warn")

    @property
    def fail_count(self) -> int:
        """Number of `fail` probes."""
        return sum(1 for probe in self.probes if probe.status == "fail")

    @property
    def skip_count(self) -> int:
        """Number of `skip` probes."""
        return sum(1 for probe in self.probes if probe.status == "skip")


# ---------------------------------------------------------------------------
# Probes
# ---------------------------------------------------------------------------


async def _probe_version(client: Dhis2Client) -> ProbeResult:
    """Check `/api/system/info` → version >= 2.42."""
    try:
        info = await client.get_raw("/api/system/info")
    except Exception as exc:  # noqa: BLE001 — probe must report, not raise
        return ProbeResult(name="dhis2-version", status="fail", message=f"/api/system/info failed: {exc}")
    raw = str(info.get("version", ""))
    parts = raw.split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
    except (IndexError, ValueError):
        return ProbeResult(
            name="dhis2-version",
            status="fail",
            message=f"could not parse DHIS2 version {raw!r} from /api/system/info",
        )
    if (major, minor) < _MIN_DHIS2_VERSION:
        return ProbeResult(
            name="dhis2-version",
            status="fail",
            message=f"DHIS2 {raw} < 2.42 — workspace requires 2.42+",
        )
    return ProbeResult(name="dhis2-version", status="pass", message=f"{raw} (workspace requires 2.42+)")


async def _probe_auth(client: Dhis2Client) -> ProbeResult:
    """Check `/api/me` — authentication works, user has a username."""
    try:
        me = await client.get_raw("/api/me", params={"fields": "id,username,displayName"})
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(name="auth", status="fail", message=f"/api/me failed: {exc}")
    username = str(me.get("username", ""))
    if not username:
        return ProbeResult(name="auth", status="fail", message="/api/me returned no username")
    return ProbeResult(name="auth", status="pass", message=f"authenticated as {username}")


async def _probe_analytics_rawdata_json_suffix(client: Dhis2Client) -> ProbeResult:
    """Check BUGS.md #1 — `/api/analytics/rawData` requires `.json` suffix."""
    # Without suffix: expect 404 or HTML error (content negotiation ignored on this sub-resource).
    without_suffix_404 = False
    try:
        await client.get_raw(
            "/api/analytics/rawData",
            params={"dimension": ["dx:nonexistent", "pe:LAST_12_MONTHS"]},
        )
    except Dhis2ApiError as exc:
        without_suffix_404 = exc.status_code == 404
    except Exception:  # noqa: BLE001
        pass
    if not without_suffix_404:
        return ProbeResult(
            name="analytics-rawdata-json-suffix",
            status="warn",
            message="GET /api/analytics/rawData (no suffix) didn't 404 — upstream may have fixed content negotiation",
            bugs_ref="BUGS.md #1",
        )
    return ProbeResult(
        name="analytics-rawdata-json-suffix",
        status="pass",
        message="404 without .json as expected (workaround still needed)",
        bugs_ref="BUGS.md #1",
    )


async def _probe_oauth2_discovery(client: Dhis2Client) -> ProbeResult:
    """Check `/.well-known/openid-configuration` — OAuth2 discovery endpoint."""
    try:
        discovery = await client.get_raw("/.well-known/openid-configuration")
    except Dhis2ApiError as exc:
        if exc.status_code == 404:
            return ProbeResult(
                name="oauth2-discovery",
                status="skip",
                message="OAuth2 not enabled (no /.well-known/openid-configuration)",
                bugs_ref="BUGS.md #4",
            )
        return ProbeResult(name="oauth2-discovery", status="fail", message=f"discovery returned {exc.status_code}")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(name="oauth2-discovery", status="fail", message=f"discovery failed: {exc}")
    required = {"authorization_endpoint", "token_endpoint", "jwks_uri"}
    missing = sorted(required - set(discovery))
    if missing:
        return ProbeResult(
            name="oauth2-discovery",
            status="fail",
            message=f"discovery missing fields: {missing}",
            bugs_ref="BUGS.md #4",
        )
    issuer = discovery.get("issuer", "?")
    return ProbeResult(name="oauth2-discovery", status="pass", message=f"issuer={issuer}, all required fields present")


async def _probe_login_config(client: Dhis2Client) -> ProbeResult:
    """Check `/api/loginConfig` — informational summary DHIS2's login app renders."""
    try:
        config = await client.get_raw("/api/loginConfig")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(name="login-config", status="fail", message=f"/api/loginConfig failed: {exc}")
    providers = config.get("oidcProviders") or []
    provider_ids = [p.get("id", "?") for p in providers]
    return ProbeResult(
        name="login-config",
        status="pass",
        message=(
            f"title={config.get('applicationTitle', '?')!r} "
            f"oidc-providers={provider_ids} "
            f"useCustomLogoFront={config.get('useCustomLogoFront')}"
        ),
    )


async def _probe_userrole_schema_naming(client: Dhis2Client) -> ProbeResult:
    """Check BUGS.md #8 — `/api/schemas/userRole` still mis-pluralizes `authorities` as `authoritys`."""
    try:
        schema = await client.get_raw("/api/schemas/userRole")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="userrole-authorities-naming",
            status="fail",
            message=f"/api/schemas/userRole failed: {exc}",
            bugs_ref="BUGS.md #8",
        )
    properties = schema.get("properties") or []
    # BUGS #8: /api/schemas reports the field as singular `authority` with fieldName `authorities`.
    # The wire key on /api/userRoles is `authorities` (the OpenAPI tells it correctly) — the /api/schemas
    # emitter is where the pluralisation is wrong.
    candidate = next(
        (p for p in properties if p.get("name") == "authority" or p.get("fieldName") == "authorities"),
        None,
    )
    if candidate is None:
        return ProbeResult(
            name="userrole-authorities-naming",
            status="warn",
            message="UserRole authorities/authority field not found in schema",
            bugs_ref="BUGS.md #8",
        )
    name = candidate.get("name")
    field_name = candidate.get("fieldName")
    if name == "authority" and field_name == "authorities":
        return ProbeResult(
            name="userrole-authorities-naming",
            status="pass",
            message=f"schema still reports name={name!r} fieldName={field_name!r} (workaround still needed)",
            bugs_ref="BUGS.md #8",
        )
    return ProbeResult(
        name="userrole-authorities-naming",
        status="warn",
        message=f"schema reports name={name!r} fieldName={field_name!r} — shape may have changed upstream",
        bugs_ref="BUGS.md #8",
    )


async def _probe_outlier_algorithm_enum(client: Dhis2Client) -> ProbeResult:
    """Check BUGS.md #13 — DHIS2 server still rejects `MOD_Z_SCORE` even though OAS declares it."""
    try:
        await client.get_raw(
            "/api/analytics/outlierDetection",
            params={
                "ds": "nonexistent",  # deliberately bogus — we only care that validation runs
                "ou": "nonexistent",
                "pe": "LAST_12_MONTHS",
                "algorithm": "MOD_Z_SCORE",
            },
        )
    except Dhis2ApiError as exc:
        body = exc.body if isinstance(exc.body, dict) else {}
        message = str(body.get("message", ""))
        if exc.status_code == 400 and "MOD_Z_SCORE" in message and "MODIFIED_Z_SCORE" in message:
            return ProbeResult(
                name="outlier-algorithm-enum",
                status="pass",
                message="server still rejects MOD_Z_SCORE (use MODIFIED_Z_SCORE)",
                bugs_ref="BUGS.md #13",
            )
        if exc.status_code == 400:
            # Validation failed for a different reason (probably our bogus UIDs) — can't prove it either way.
            return ProbeResult(
                name="outlier-algorithm-enum",
                status="skip",
                message=f"unclear response: {exc.status_code} {message[:80]!r}",
                bugs_ref="BUGS.md #13",
            )
        return ProbeResult(
            name="outlier-algorithm-enum",
            status="warn",
            message=f"unexpected status {exc.status_code}",
            bugs_ref="BUGS.md #13",
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(name="outlier-algorithm-enum", status="fail", message=f"probe failed: {exc}")
    # 200? Then MOD_Z_SCORE is accepted — bug resolved upstream.
    return ProbeResult(
        name="outlier-algorithm-enum",
        status="warn",
        message="MOD_Z_SCORE accepted — upstream may have fixed the enum name",
        bugs_ref="BUGS.md #13",
    )


async def _probe_custom_logo_flag_consistency(client: Dhis2Client) -> ProbeResult:
    """Check BUGS.md #11 — `keyUseCustomLogoFront` system setting mirrors `/api/loginConfig.useCustomLogoFront`."""
    try:
        config = await client.get_raw("/api/loginConfig")
        setting = await client.get_raw("/api/systemSettings/keyUseCustomLogoFront")
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            name="custom-logo-flag",
            status="fail",
            message=f"probe failed: {exc}",
            bugs_ref="BUGS.md #11",
        )
    login_flag = config.get("useCustomLogoFront")
    raw_setting = setting.get("keyUseCustomLogoFront")

    # DHIS2 returns bool-ish strings; normalise for comparison.
    def _truthy(value: object) -> bool:
        return str(value).lower() == "true"

    if _truthy(login_flag) == _truthy(raw_setting):
        return ProbeResult(
            name="custom-logo-flag",
            status="pass",
            message=f"consistent: loginConfig={login_flag} keySetting={raw_setting}",
            bugs_ref="BUGS.md #11",
        )
    return ProbeResult(
        name="custom-logo-flag",
        status="warn",
        message=(
            f"mismatch — loginConfig.useCustomLogoFront={login_flag} "
            f"vs keyUseCustomLogoFront={raw_setting}. "
            "Upload won't be visible until both agree."
        ),
        bugs_ref="BUGS.md #11",
    )


_PROBES = (
    _probe_version,
    _probe_auth,
    _probe_login_config,
    _probe_oauth2_discovery,
    _probe_analytics_rawdata_json_suffix,
    _probe_userrole_schema_naming,
    _probe_outlier_algorithm_enum,
    _probe_custom_logo_flag_consistency,
)


async def run_doctor(profile: Profile, *, profile_name: str | None = None) -> DoctorReport:
    """Run every probe concurrently and assemble a report."""
    async with open_client(profile) as client:
        # Capture the version separately so it's on the report even when later probes fail.
        try:
            info = await client.get_raw("/api/system/info")
            version = str(info.get("version", "")) or None
        except Exception:  # noqa: BLE001
            version = None
        probes = await asyncio.gather(*(probe(client) for probe in _PROBES))
    return DoctorReport(
        profile_name=profile_name,
        base_url=profile.base_url,
        dhis2_version=version,
        probes=list(probes),
    )
