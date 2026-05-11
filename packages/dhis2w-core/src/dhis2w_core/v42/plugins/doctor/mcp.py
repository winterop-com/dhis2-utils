"""FastMCP tool registration for the `doctor` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_core.profile import resolve_profile
from dhis2w_core.v42.plugins.doctor import service
from dhis2w_core.v42.plugins.doctor._models import DoctorReport, ProbeCategory


def register(mcp: Any) -> None:
    """Register `doctor_run` + category-specific MCP tools."""

    @mcp.tool()
    async def doctor_run(
        all_categories: bool = False,
        profile: str | None = None,
    ) -> DoctorReport:
        """Probe a DHIS2 instance — metadata health + DHIS2 data-integrity by default.

        Three probe categories:

        - `metadata` — workspace-specific instance-health checks (data sets with
          no data elements, programs without stages, user groups with no members,
          etc.). Each offending UID is listed in the probe's `offending_uids`.
        - `integrity` — wraps DHIS2's own `/api/dataIntegrity/summary` (~40
          built-in checks). `pass` when a DHIS2 check reports zero issues.
        - `bugs` — verifies BUGS.md workarounds still apply (workspace drift
          detection; not usually the right default for operators).

        Default: runs `metadata` + `integrity`. Pass `all_categories=True` to
        include `bugs` too.
        """
        categories: tuple[ProbeCategory, ...] = (
            ("metadata", "integrity", "bugs") if all_categories else ("metadata", "integrity")
        )
        return await service.run_doctor(resolve_profile(profile), categories=categories)

    @mcp.tool()
    async def doctor_metadata(profile: str | None = None) -> DoctorReport:
        """Run only the workspace metadata-health probes (no DHIS2 integrity, no bug drift)."""
        return await service.run_doctor(resolve_profile(profile), categories=("metadata",))

    @mcp.tool()
    async def doctor_integrity(profile: str | None = None) -> DoctorReport:
        """Run only DHIS2's `/api/dataIntegrity/summary` probes."""
        return await service.run_doctor(resolve_profile(profile), categories=("integrity",))

    @mcp.tool()
    async def doctor_bugs(profile: str | None = None) -> DoctorReport:
        """Run only BUGS.md workaround drift probes (workspace maintenance)."""
        return await service.run_doctor(resolve_profile(profile), categories=("bugs",))
