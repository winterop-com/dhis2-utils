"""Write one aggregate data value against the seeded Norway e2e dataset.

Exercises the bulk-import path at `/api/dataValueSets` with a single value.
Uses the org units / data elements baked into `infra/dhis-v42.sql.gz` so the
write succeeds out of the box against `make dhis2-run`.

Usage:
    uv run python examples/03_push_data_value.py [value]

Defaults to value=100 for NOROsloProv / DEancVisit1 / period 202603.

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import sys

from _runner import run_example
from dhis2_client import DataValue, DataValueSet
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env

_DEFAULT_VALUE = "100"


async def main() -> None:
    """Push one data value and print the import summary."""
    value = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_VALUE
    # DataValue / DataValueSet are exported from dhis2_client — same typed
    # envelope used by `dhis2 data aggregate get` returns.
    payload = DataValueSet(
        dataValues=[
            DataValue(
                dataElement="DEancVisit1",  # ANC 1st visit — from the seeded dump
                period="202603",  # March 2026
                orgUnit="NOROsloProv",  # Oslo — from the seeded dump
                value=value,
            ),
        ],
    )
    async with open_client(profile_from_env()) as client:
        # /api/dataValueSets is a bulk endpoint with no typed resource accessor;
        # post_raw is the escape hatch. The response is a WebMessageResponse.
        raw = await client.post_raw("/api/dataValueSets", payload.model_dump(exclude_none=True))
        from dhis2_client import WebMessageResponse

        response = WebMessageResponse.model_validate(raw)
        counts = response.import_count()
        print(f"status: {response.status or response.httpStatus or '?'}")
        if counts is not None:
            print(
                f"  imported={counts.imported}  updated={counts.updated}  "
                f"ignored={counts.ignored}  deleted={counts.deleted}"
            )
        for conflict in response.conflicts()[:5]:
            print(f"  conflict: {conflict.property} = {conflict.value} [{conflict.errorCode}]")


if __name__ == "__main__":
    run_example(main)
