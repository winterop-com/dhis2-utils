"""Program v43 additions: enableChangeLog, enrollmentCategoryCombo, plus 4 label-pair fields.

v43 added eight new fields to `Program`:

- enableChangeLog (bool)
- enrollmentCategoryCombo (Reference)
- enrollmentsLabel + displayEnrollmentsLabel (str)
- eventsLabel + displayEventsLabel (str)
- programStagesLabel + displayProgramStagesLabel (str)

The hand-written `client.programs.get` returns the v42-typed model, so
these arrive on `model_extra` for v43 wire data. For typed access,
import the v43 model directly.

v43 also REMOVED `Program.favorite`. Reads against a v42-pinned model
return None on v43 because the field is missing on the wire.

Usage:
    uv run python examples/client/program_change_log_and_labels.py
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_client.generated.v43.schemas.program import Program as ProgramV43
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env


async def main() -> None:
    """Read one Program and surface every v43 addition (and the removed `favorite` field)."""
    async with open_client(profile_from_env()) as client:
        programs = await client.programs.list_all(page_size=1)
        if not programs:
            print("no programs on this instance")
            return
        program = programs[0]
        print(f"version={client.version_key} program={program.id} name={program.name!r}")

        if client.version_key == "v42":
            print(f"  v42 program.favorite={getattr(program, 'favorite', None)}  (removed in v43)")
            return

        # v43 path 1: read additions off model_extra on the v42-typed helper.
        extras = program.model_extra or {}
        print(
            f"  [extras] enableChangeLog={extras.get('enableChangeLog')} "
            f"enrollmentsLabel={extras.get('enrollmentsLabel')!r} "
            f"eventsLabel={extras.get('eventsLabel')!r} "
            f"programStagesLabel={extras.get('programStagesLabel')!r}"
        )

        # v43 path 2: typed access via direct v43 import.
        raw = await client.get_raw(f"/api/programs/{program.id}")
        program_v43 = ProgramV43.model_validate(raw)
        print(
            f"  [typed v43] enableChangeLog={program_v43.enableChangeLog} "
            f"enrollmentCategoryCombo="
            f"{program_v43.enrollmentCategoryCombo.id if program_v43.enrollmentCategoryCombo else None} "
            f"enrollmentsLabel={program_v43.enrollmentsLabel!r}"
        )
        print("  v43 program.favorite -> N/A (field removed)")


if __name__ == "__main__":
    run_example(main)
