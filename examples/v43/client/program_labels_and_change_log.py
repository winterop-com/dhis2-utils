"""v43-only — set the v43 Program configuration fields (change-log + custom UI labels).

DHIS2 2.43 added five fields to the `Program` schema:

- `enableChangeLog` (bool) — gates the per-program enrollment + event
  change-log endpoints (`/api/tracker/enrollments/{uid}/changeLogs`,
  `/api/tracker/events/{event}/changeLogs`, etc.). Default off.
- `enrollmentsLabel`, `eventsLabel`, `programStagesLabel` (2-255 chars) —
  override the default "Enrollments" / "Events" / "Program stages"
  terminology in the Capture + Tracker Capture apps. Lets implementations
  use domain-native vocabulary ("Visits", "Encounters", "Stages", etc.).
- `enrollmentCategoryCombo` (Reference) — an alternative CategoryCombo
  applied specifically at enrollment time (distinct from the program's
  regular `categoryCombo`).

`ProgramsAccessor.set_labels(uid, **kwargs)` is the v43-only helper that
PUTs only the fields you pass; everything else round-trips untouched.

This example reads the first WITH_REGISTRATION program in the active
profile, applies a sample label set + turns change-log on, then re-reads
to confirm the fields persisted.

Pairs with `docs/architecture/schema-diff-v41-v42-v43.md` (the
"Program.enableChangeLog + label fields" section) which documents the
underlying schema delta in detail.

Usage:
    uv run python examples/v43/client/program_labels_and_change_log.py

Requires: a profile pointing at a DHIS2 v43 instance with at least one
WITH_REGISTRATION program; the seeded Sierra Leone fixture qualifies
(IpHINAT79UW — Child Programme).
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_client.v43 import Dhis2Client
from dhis2w_core.client_context import build_auth_for_name
from dhis2w_core.profile import resolve


async def main() -> None:
    """Set v43-only Program label fields + enable_change_log on the first tracker program."""
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

        # The v43 `Program` schema declares these as typed fields, and the
        # accessor's `_PROGRAM_FIELDS` requests them — so they're available
        # as typed attributes on the parsed model (not via `model_extra`).
        print(f"before: {target.id} name={target.name!r}")
        print(
            f"  enableChangeLog={target.enableChangeLog}\n"
            f"  enrollmentsLabel={target.enrollmentsLabel!r}\n"
            f"  eventsLabel={target.eventsLabel!r}"
        )

        updated = await client.programs.set_labels(
            target.id,
            enable_change_log=True,
            enrollments_label="Visits",
            events_label="Encounters",
            program_stages_label="Care Stages",
        )

        print(f"after:  {updated.id} name={updated.name!r}")
        print(
            f"  enableChangeLog={updated.enableChangeLog}\n"
            f"  enrollmentsLabel={updated.enrollmentsLabel!r}\n"
            f"  eventsLabel={updated.eventsLabel!r}\n"
            f"  programStagesLabel={updated.programStagesLabel!r}"
        )


if __name__ == "__main__":
    run_example(main)
