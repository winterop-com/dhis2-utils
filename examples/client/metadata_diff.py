"""Client-level example — use the `metadata` plugin service directly for diff workflows.

Mirrors the CLI's `dhis2 metadata diff` but calls `service.diff_bundles` /
`service.diff_bundle_against_instance` directly, so you can wire a diff into
a Python pipeline (CI drift detection, pre-import safety checks, etc.).
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from _runner import run_example
from dhis2_core.plugins.metadata import service
from dhis2_core.profile import profile_from_env


async def main() -> None:
    """Compare a fresh live export against a synthetic baseline + surface per-resource deltas."""
    profile = profile_from_env()

    # In real use the baseline would come from git / an artefact store. Here we
    # export the live catalog, save a copy as the "baseline," mutate it, and
    # diff to show how the machinery reports structural changes.
    live_bundle = await service.export_metadata(
        profile,
        resources=["dataElements"],
        fields=":owner",
    )
    baseline = json.loads(json.dumps(live_bundle))  # deep copy
    if baseline.get("dataElements"):
        baseline["dataElements"][0]["name"] = "BASELINE DRIFT"  # pretend the baseline has an older name

    diff = service.diff_bundles(
        baseline,
        live_bundle,
        left_label="baseline.json",
        right_label="instance",
    )
    print(f"diff {diff.left_label} -> {diff.right_label}")
    for resource in diff.resources:
        print(
            f"  {resource.resource}: "
            f"+{len(resource.created)} ~{len(resource.updated)} "
            f"-{len(resource.deleted)} ={resource.unchanged_count}"
        )
        for change in resource.updated[:3]:
            fields = ", ".join(change.changed_fields)
            print(f"    updated {change.id} ({change.name or '-'}): {fields}")

    # Convenience: compare a file-on-disk against the live instance in one call.
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(baseline, tmp)
        baseline_path = Path(tmp.name)
    live_diff = await service.diff_bundle_against_instance(
        profile,
        json.loads(baseline_path.read_text(encoding="utf-8")),
        bundle_label=baseline_path.name,
    )
    print(
        f"\nlive vs {baseline_path.name}: "
        f"+{live_diff.total_created} ~{live_diff.total_updated} -{live_diff.total_deleted}"
    )


if __name__ == "__main__":
    run_example(main)
