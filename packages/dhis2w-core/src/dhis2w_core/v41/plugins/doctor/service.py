"""Service layer for the `doctor` plugin — three probe categories, one report shape.

Three sub-commands, three probe modules:

- `metadata` (primary) — workspace-specific instance-health probes. "What's
  wrong with this instance's configuration?"
- `integrity` — wraps DHIS2's own `/api/dataIntegrity/summary` so one doctor
  run covers DHIS2's ~40 built-in checks alongside ours.
- `bugs` — drift detection against BUGS.md workarounds. Useful for workspace
  maintenance but not the operator-facing default.

`run_doctor()` with no category filter runs metadata + integrity (the two
that matter to operators). Pass `categories=("bugs",)` to run only the
workspace drift checks; `("metadata", "integrity", "bugs")` runs everything.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence

from dhis2w_client.v41 import Dhis2Client

from dhis2w_core.profile import Profile
from dhis2w_core.v41.client_context import open_client
from dhis2w_core.v41.plugins.doctor._models import DoctorReport, ProbeCategory, ProbeResult
from dhis2w_core.v41.plugins.doctor.probes_bugs import BUGS_PROBES
from dhis2w_core.v41.plugins.doctor.probes_integrity import run_integrity_probes
from dhis2w_core.v41.plugins.doctor.probes_metadata import METADATA_PROBES

# Default categories when the caller doesn't pick — operator-useful subset.
_DEFAULT_CATEGORIES: tuple[ProbeCategory, ...] = ("metadata", "integrity")
_ALL_CATEGORIES: tuple[ProbeCategory, ...] = ("metadata", "integrity", "bugs")


async def _probe_version(client: Dhis2Client) -> str | None:
    """Grab the version separately — the report surfaces it even when probes fail."""
    try:
        info = await client.get_raw("/api/system/info")
        return str(info.get("version", "")) or None
    except Exception:  # noqa: BLE001
        return None


async def _gather_metadata(client: Dhis2Client) -> list[ProbeResult]:
    return list(await asyncio.gather(*(probe(client) for probe in METADATA_PROBES)))


async def _gather_bugs(client: Dhis2Client) -> list[ProbeResult]:
    return list(await asyncio.gather(*(probe(client) for probe in BUGS_PROBES)))


async def _gather_integrity(client: Dhis2Client) -> list[ProbeResult]:
    return await run_integrity_probes(client)


async def run_doctor(
    profile: Profile,
    *,
    categories: Sequence[ProbeCategory] | None = None,
    profile_name: str | None = None,
) -> DoctorReport:
    """Run every probe in `categories` concurrently and assemble a report.

    Defaults to `("metadata", "integrity")` — the operator-facing checks.
    Pass `categories=("bugs",)` to run workspace drift detection only, or
    `("metadata", "integrity", "bugs")` for everything.
    """
    selected = tuple(categories) if categories else _DEFAULT_CATEGORIES
    async with open_client(profile) as client:
        version = await _probe_version(client)
        # Dispatch each category independently — within each category probes
        # already run concurrently. This keeps integrity failures from blocking
        # metadata results on slow instances.
        results: list[list[ProbeResult]] = []
        tasks: list = []
        if "metadata" in selected:
            tasks.append(_gather_metadata(client))
        if "integrity" in selected:
            tasks.append(_gather_integrity(client))
        if "bugs" in selected:
            tasks.append(_gather_bugs(client))
        if tasks:
            results = list(await asyncio.gather(*tasks))
    probes: list[ProbeResult] = [probe for group in results for probe in group]
    return DoctorReport(
        profile_name=profile_name,
        base_url=profile.base_url,
        dhis2_version=version,
        probes=probes,
    )


__all__ = ["DoctorReport", "ProbeCategory", "ProbeResult", "run_doctor"]
