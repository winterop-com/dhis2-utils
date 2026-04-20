"""DHIS2 data-integrity probes — wraps `/api/dataIntegrity/summary`.

DHIS2 ships ~40 built-in integrity checks (organisation-unit coverage,
indicator expression validity, duplicate category options, etc.) that are
authoritative for the instance's own definition of "healthy." This module
surfaces each check's summary as a doctor `ProbeResult` so one
`dhis2 doctor` run covers workspace metadata probes + DHIS2's own.

Reuses the `maintenance` plugin's typed `DataIntegrityReport` — no duplicate
parsing logic.
"""

from __future__ import annotations

from dhis2_client import Dhis2Client

from dhis2_core.plugins.doctor._models import ProbeResult


async def run_integrity_probes(client: Dhis2Client) -> list[ProbeResult]:
    """Fetch `/api/dataIntegrity/summary` and convert each check into a ProbeResult.

    Each check becomes one `ProbeResult` with `category="integrity"`. `pass`
    when the check reports zero issues, `warn` otherwise. Severity is carried
    in the message so operators can triage.
    """
    try:
        raw = await client.get_raw("/api/dataIntegrity/summary")
    except Exception as exc:  # noqa: BLE001
        return [
            ProbeResult(
                name="dataIntegrity-summary",
                category="integrity",
                status="fail",
                message=f"/api/dataIntegrity/summary failed: {exc}",
            )
        ]
    # DHIS2 returns an empty `{}` when checks haven't been run yet — tell the
    # operator to kick a run off.
    if not raw:
        return [
            ProbeResult(
                name="dataIntegrity-summary",
                category="integrity",
                status="skip",
                message=(
                    "no data-integrity results on this instance yet — "
                    "run `dhis2 maintenance dataintegrity run --watch` first"
                ),
            )
        ]
    probes: list[ProbeResult] = []
    for name, result in raw.items():
        if not isinstance(result, dict):
            continue
        count = int(result.get("count", 0) or 0)
        severity = result.get("severity")
        sev_suffix = f" [severity={severity}]" if severity else ""
        if count == 0:
            probes.append(
                ProbeResult(
                    name=f"integrity:{name}",
                    category="integrity",
                    status="pass",
                    message=f"0 issues{sev_suffix}",
                )
            )
        else:
            probes.append(
                ProbeResult(
                    name=f"integrity:{name}",
                    category="integrity",
                    status="warn",
                    message=(
                        f"{count} issue(s){sev_suffix} — "
                        f"run `dhis2 maintenance dataintegrity result {name} --details` for UIDs "
                        "(requires a prior `dataintegrity run --details`)"
                    ),
                )
            )
    return probes
