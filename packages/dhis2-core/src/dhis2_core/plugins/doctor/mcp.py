"""FastMCP tool registration for the `doctor` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.doctor import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `doctor_run` MCP tool."""

    @mcp.tool()
    async def doctor_run(profile: str | None = None) -> service.DoctorReport:
        """Probe a DHIS2 instance for known BUGS.md gotchas + workspace requirements.

        Runs a read-only battery of probes (~8 currently):
        - DHIS2 version >= 2.42
        - Authentication working (via /api/me)
        - /api/loginConfig summary (title, OIDC providers, logo flag)
        - /.well-known/openid-configuration present when OAuth2 is enabled
        - BUGS.md #1 — `/api/analytics/rawData` requires `.json` suffix
        - BUGS.md #8 — UserRole schema mis-pluralizes `authorities`
        - BUGS.md #11 — `keyUseCustomLogoFront` ↔ `useCustomLogoFront` consistency
        - BUGS.md #13 — `MOD_Z_SCORE` OAS enum rejected by server

        Each probe returns `pass` / `warn` / `fail` / `skip` with a BUGS.md
        cross-ref where relevant. `pass` means "bug workaround still works" OR
        "requirement satisfied" — the report message disambiguates.
        """
        return await service.run_doctor(resolve_profile(profile))
