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

import asyncio
import os
import sys

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def main(limit: int) -> None:
    """Fetch up to `limit` data elements and print their uid + name."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
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
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
