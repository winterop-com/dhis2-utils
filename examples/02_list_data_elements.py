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

from dhis2_client import AuthProvider, BasicAuth, Dhis2Client, PatAuth


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
    async with Dhis2Client(base_url, auth=_auth_from_env()) as client:
        # After connect(), client.resources is the generated v{NN} accessor.
        # Fall back to a raw call if your DHIS2 version doesn't have a
        # generated module yet.
        response = await client.get_raw(
            "/api/dataElements",
            params={"fields": "id,name,valueType,domainType", "pageSize": limit},
        )
        elements = response.get("dataElements", [])
        print(f"{len(elements)} data element(s) (DHIS2 {client.raw_version}):")
        for element in elements:
            print(
                f"  {element.get('id', '?'):<12} "
                f"{element.get('name', '?'):<40} "
                f"{element.get('valueType', '?'):<20} "
                f"{element.get('domainType', '?')}"
            )


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
