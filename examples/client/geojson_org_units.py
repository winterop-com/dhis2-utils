"""Pull DHIS2 org units as GeoJSON, validate with geojson-pydantic.

Demonstrates `/api/organisationUnits.geojson`. Parses the response
through `geojson_pydantic.FeatureCollection` so coordinates, geometry
types, and properties are all typed — no manual `dict.get(...)` chains.

By default the seeded Norway fixture has no geometries, so this example
falls back to showing the feature-free FeatureCollection. Against a real
instance (or after PATCH /api/organisationUnits/{uid} with a geometry)
you'll see real coordinates.

Usage:
    uv run python examples/client/geojson_org_units.py [level]

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os
import sys

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth
from geojson_pydantic import FeatureCollection


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def main(level: int) -> None:
    """Fetch org-unit GeoJSON at `level` and print a typed summary."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        payload = await client.get_raw(
            "/api/organisationUnits.geojson",
            params={"level": level, "includeCoordinates": "true"},
        )
    # Validate through geojson-pydantic — gives us .features typed as
    # list[Feature[Geometry, Properties]] with real coordinate types.
    collection: FeatureCollection = FeatureCollection.model_validate(payload)
    print(f"level {level}: {len(collection.features)} feature(s)")
    for feature in collection.features[:5]:
        props = feature.properties or {}
        geom_type = feature.geometry.type if feature.geometry else "(none)"
        print(f"  {str(props.get('id', '?')):<12} {str(props.get('name', '?')):<28} geometry_type={geom_type}")
    if not collection.features:
        print("  (no geometries on the seeded fixture — PATCH a geometry onto an OU to see coordinates)")


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 2))
