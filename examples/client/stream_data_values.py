"""Stream a dataValueSets upload — `client.data_values.stream`.

DHIS2's `POST /api/dataValueSets` accepts JSON, XML, CSV, and ADX. For
large payloads (100k+ rows), buffering the whole body in memory before
sending is the slow path — `client.data_values.stream` feeds httpx's
chunked transfer encoding directly.

Covered here:

1. **Bytes** — in-memory payload; typed envelope back.
2. **Sync generator** — build chunks on the fly; bytes never fully
   resident in Python.
3. **Path (CSV)** — stream a file straight to the socket. The minimal
   4-column header (`dataelement,period,orgunit,value`) is the cleanest
   form; DHIS2 derives default category/attribute combos from the
   dataset.
4. **Multi-row file timing** — how long a 48-row CSV stream takes
   end-to-end (rotating across 4 facilities × 12 months of 2024).

Usage:
    uv run python examples/client/stream_data_values.py
"""

from __future__ import annotations

import json
import tempfile
import time
from collections.abc import Iterator
from pathlib import Path

from _runner import run_example
from dhis2w_client import WebMessageResponse
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

# Known-good combo on the seeded stack (same triplet the
# `push_data_value.py` example uses). Ngelehun CHC is a facility-level
# OU assigned to the Child Health dataset on every seed rebuild.
_DE = "fClA2Erf6IO"
_OU = "DiszpKrYNg8"  # Ngelehun CHC
_PERIOD = "202603"


async def main() -> None:
    """Run all four streaming shapes against the seeded dataValueSets endpoint."""
    async with open_client(profile_from_env()) as client:
        # 1. Bytes — single-shot. No intermediate storage beyond the body itself.
        body = json.dumps(
            {"dataValues": [{"dataElement": _DE, "period": _PERIOD, "orgUnit": _OU, "value": "21"}]}
        ).encode()
        print("--- bytes / JSON ---")
        envelope = await client.data_values.stream(body, content_type="application/json")
        _print_counts(envelope)

        # 2. Sync generator — each chunk yields at send time. Useful when
        # the body is constructed from a large source (DB rows, line-by-line
        # transform) you don't want fully materialised in memory.
        print("\n--- sync generator / JSON ---")

        def chunks() -> Iterator[bytes]:
            yield b'{"dataValues":['
            yield json.dumps({"dataElement": _DE, "period": _PERIOD, "orgUnit": _OU, "value": "23"}).encode()
            yield b"]}"

        envelope = await client.data_values.stream(chunks(), content_type="application/json")
        _print_counts(envelope)

        # 3. Path / CSV — the typical "scheduled month-end import" shape.
        # The minimal 4-column header (dataelement, period, orgunit, value) is
        # the cleanest form; DHIS2 derives default category/attribute combos
        # from the dataset. Older docs show the full 11-column header — v43
        # rejects empty trailing columns with E8101 ("data set is required to
        # decode category options") when categoryoptioncombo / attributeoptioncombo
        # are blank, so omit them when defaults are fine.
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "values.csv"
            csv_path.write_text(f'"dataelement","period","orgunit","value"\n"{_DE}","{_PERIOD}","{_OU}","29"\n')
            print(f"\n--- Path / CSV ({csv_path.stat().st_size} B) ---")
            envelope = await client.data_values.stream(csv_path, content_type="application/csv")
            _print_counts(envelope)

            # 4. Multi-row CSV — shows streaming with a real multi-write batch.
            # Every row needs a unique (dataElement, period, orgUnit) key — v43
            # rejects batches where rows collide on the same DataValueKey.
            # Cycle through a few facility OUs across the 12 months of 2024.
            big = Path(tmp) / "big.csv"
            months = [f"2024{m:02d}" for m in range(1, 13)]
            ou_pool = [_OU, "ueuQlqb8ccl", "Mi4dWRtfIOC", "vELbGdEphPd"]  # Ngelehun + 3 other facilities
            with big.open("w") as handle:
                handle.write('"dataelement","period","orgunit","value"\n')
                for idx, (ou, month) in enumerate((ou, m) for ou in ou_pool for m in months):
                    handle.write(f'"{_DE}","{month}","{ou}","{idx}"\n')
            row_count = len(ou_pool) * len(months)
            print(f"\n--- {row_count}-row CSV stream ({big.stat().st_size} B) ---")
            t0 = time.monotonic()
            envelope = await client.data_values.stream(big, content_type="application/csv")
            elapsed_ms = (time.monotonic() - t0) * 1000
            _print_counts(envelope, suffix=f" ({elapsed_ms:.0f} ms)")


def _print_counts(envelope: WebMessageResponse, *, suffix: str = "") -> None:
    """Pull the `ImportCount` off a `WebMessageResponse` and pretty-print the counts."""
    count = envelope.import_count()
    if count is None:
        print(f"  status={envelope.status}  (no importCount on the response){suffix}")
        return
    print(
        f"  status={envelope.status}  "
        f"imported={count.imported}  updated={count.updated}  "
        f"ignored={count.ignored}  deleted={count.deleted}{suffix}"
    )


if __name__ == "__main__":
    run_example(main)
