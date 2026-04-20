"""`dhis2 doctor` from Python — programmatic probe results for CI / monitoring.

The service returns a typed `DoctorReport`; consumers can iterate probes,
filter by status, log to whatever observability system they use. No raw
dicts, every field is a pydantic attribute.
"""

from __future__ import annotations

from _runner import run_example
from dhis2_core.plugins.doctor import service
from dhis2_core.profile import profile_from_env


async def main() -> None:
    """Run every probe + print a compact summary."""
    report = await service.run_doctor(profile_from_env())
    print(f"DHIS2 {report.dhis2_version or '?'} at {report.base_url}")
    print(f"{report.pass_count} pass / {report.warn_count} warn / {report.fail_count} fail / {report.skip_count} skip")
    for probe in report.probes:
        marker = {"pass": "+", "warn": "~", "fail": "-", "skip": " "}[probe.status]
        bugs = f" ({probe.bugs_ref})" if probe.bugs_ref else ""
        print(f"  {marker} {probe.name}: {probe.message}{bugs}")

    if report.fail_count:
        print("\nfailing probes indicate a requirement is not met — fix before relying on this instance")


if __name__ == "__main__":
    run_example(main)
