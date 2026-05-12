"""v43-only — set an alternative `enrollmentCategoryCombo` on a Program.

DHIS2 2.43 added `Program.enrollmentCategoryCombo` — an alternative
CategoryCombo applied specifically at enrollment time, distinct from
the program's regular `categoryCombo`. Lets programs carry one
disaggregation for the Program-level metadata and a different one for
enrollment-time data capture.

Unrelated to the v43 UI label overrides demoed in `program_set_labels.py`
or the `enableChangeLog` audit toggle in `program_set_change_log.py` —
they just happen to ship in the same v43 Program schema delta.

This example picks the first WITH_REGISTRATION program and an arbitrary
CategoryCombo (other than the program's existing `categoryCombo`), then
calls `set_enrollment_category_combo(uid, cc_uid)` and prints the result.

Usage:
    uv run python examples/v43/client/program_set_enrollment_category_combo.py

Requires: a DHIS2 v43 profile + at least one WITH_REGISTRATION program +
at least two CategoryCombos.
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_client.v43 import Dhis2Client
from dhis2w_core.client_context import build_auth_for_name
from dhis2w_core.profile import resolve


async def main() -> None:
    """Set `enrollmentCategoryCombo` to the first non-default combo on the first tracker program."""
    resolved = resolve()
    _, auth = build_auth_for_name(resolved.name)
    async with Dhis2Client(resolved.profile.base_url, auth=auth) as client:
        if client.version_key != "v43":
            print(f"skipping: this example targets v43; profile is on {client.version_key}")
            return

        programs = await client.programs.list_all(program_type="WITH_REGISTRATION", page_size=1)
        if not programs:
            print("skipping: no WITH_REGISTRATION programs found")
            return
        target = programs[0]
        if not target.id:
            print("skipping: first program has no id")
            return

        # Pick a CategoryCombo other than the program's current one.
        combos_raw = await client.get_raw("/api/categoryCombos", params={"fields": "id,name", "pageSize": 5})
        combos = [c for c in (combos_raw.get("categoryCombos") or []) if isinstance(c, dict) and c.get("id")]
        current_combo_id = target.categoryCombo.id if target.categoryCombo else None
        alt_combo = next(
            (c for c in combos if c["id"] != current_combo_id),
            None,
        )
        if alt_combo is None:
            print("skipping: instance has fewer than 2 CategoryCombos; can't pick an alt")
            return

        print(
            f"before: {target.id} name={target.name!r} "
            f"enrollmentCategoryCombo="
            f"{target.enrollmentCategoryCombo.id if target.enrollmentCategoryCombo else None}"
        )
        print(f"  using alt CC: {alt_combo['id']} name={alt_combo.get('name')!r}")

        updated = await client.programs.set_enrollment_category_combo(target.id, alt_combo["id"])

        print(
            f"after:  {updated.id} "
            f"enrollmentCategoryCombo="
            f"{updated.enrollmentCategoryCombo.id if updated.enrollmentCategoryCombo else None}"
        )


if __name__ == "__main__":
    run_example(main)
