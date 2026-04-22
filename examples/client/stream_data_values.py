"""Stream a dataValueSets upload — `client.data_values.stream`.

DHIS2's `POST /api/dataValueSets` accepts JSON, XML, CSV, and ADX. For
large payloads (100k+ rows), buffering the whole body in memory before
sending is the slow path — `client.data_values.stream` feeds httpx's
chunked transfer encoding directly.

Covered here:

1. **Bytes** — in-memory payload; typed envelope back.
2. **Sync generator** — build chunks on the fly; bytes never fully
   resident in Python.
3. **Path (CSV)** — stream a file straight to the socket; DHIS2's CSV
   loader requires the full column set (`dataelement,period,orgunit,
   categoryoptioncombo,attributeoptioncombo,value,storedby,lastupdated,
   comment,followup,deleted`) — partial-header CSVs get a 409.
4. **Large file timing** — how long a 1 000-row CSV takes end-to-end.

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
from dhis2_client import WebMessageResponse
from dhis2_core.client_context import open_client
from dhis2_core.profile import profile_from_env

# Known-good combo on the seeded v42 stack (same triplet the
# `push_data_value.py` example uses).
_DE = "fClA2Erf6IO"
_OU = "PMa2VCrupOd"
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
        # DHIS2's CSV loader demands the full 11-column header.
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "values.csv"
            csv_path.write_text(
                '"dataelement","period","orgunit","categoryoptioncombo",'
                '"attributeoptioncombo","value","storedby","lastupdated","comment","followup","deleted"\n'
                f'"{_DE}","{_PERIOD}","{_OU}","","","29","","","","",""\n'
            )
            print(f"\n--- Path / CSV ({csv_path.stat().st_size} B) ---")
            envelope = await client.data_values.stream(csv_path, content_type="application/csv")
            _print_counts(envelope)

            # 4. 1 000-row CSV — shows streaming scales cleanly to large batches.
            big = Path(tmp) / "big.csv"
            with big.open("w") as handle:
                handle.write(
                    '"dataelement","period","orgunit","categoryoptioncombo",'
                    '"attributeoptioncombo","value","storedby","lastupdated","comment","followup","deleted"\n'
                )
                for idx in range(1000):
                    handle.write(f'"{_DE}","{_PERIOD}","{_OU}","","","{idx}","","","","",""\n')
            print(f"\n--- 1000-row CSV stream ({big.stat().st_size} B) ---")
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
