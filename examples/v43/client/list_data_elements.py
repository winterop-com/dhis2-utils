"""List data elements via the generated typed resources.

Demonstrates `Dhis2Client.resources` — the version-aware auto-generated
surface. After `connect()` binds the v42 module, `client.resources.dataElements`
is a typed accessor with pagination, field selection, and a pydantic model
return type.

Usage:
    uv run python examples/02_list_data_elements.py [limit]

Env: same as 01_whoami.py
"""

from __future__ import annotations

import sys

from _runner import run_example
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env


async def main() -> None:
    """Fetch up to `limit` data elements and print their uid + name."""
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    async with open_client(profile_from_env()) as client:
        # After connect(), client.resources.<name> is a typed accessor with pydantic
        # models as return types — no string-keyed dict access.
        elements = await client.resources.data_elements.list(
            fields="id,name,valueType,domainType",
            page_size=limit,
        )
        print(f"{len(elements)} data element(s) (DHIS2 {client.raw_version}):")
        for element in elements:
            print(
                f"  {element.id or '?':<12} "
                f"{element.name or '?':<40} "
                f"{str(element.valueType or '?'):<20} "
                f"{element.domainType or '?'}"
            )


if __name__ == "__main__":
    run_example(main)
