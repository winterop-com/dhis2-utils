"""Indicator CRUD — create a typed Indicator with a formula, use it, clean up.

DHIS2 indicators are computed fields (`numerator / denominator * factor`)
where both numerator and denominator are expressions referencing data elements
or other indicators. This script creates an indicator that computes
`ANC coverage = #{DEancVisit1} / #{DEancVisit4}` and links it to a default
indicator type, then tears it down.

Shows: `IndicatorType` accessor for the type lookup, `Indicator` typed model
with a real formula payload, typed PUT-update via `update()`, `delete()`.

Usage:
    uv run python examples/client/15_indicator_crud.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os

from dhis2_client import AuthProvider, BasicAuth, Dhis2, Dhis2Client, PatAuth
from dhis2_client.generated.v42.common import Reference
from dhis2_client.generated.v42.schemas.indicator import Indicator

# IndicatorType is imported lazily inside _ensure_indicator_type so the example
# stays self-contained even when the seeded fixture doesn't ship one.


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def _mint_uid(client: Dhis2Client) -> str:
    """Ask DHIS2 for a fresh 11-char UID (utility, not a resource)."""
    response = await client.get_raw("/api/system/id", params={"limit": 1})
    return str(response["codes"][0])


async def _ensure_indicator_type(client: Dhis2Client) -> str:
    """Return an existing IndicatorType UID, or create a throwaway one if none exist."""
    types = await client.resources.indicator_types.list(fields="id,name", page_size=1)
    if types:
        return str(types[0].id)
    # Seed fixture didn't ship one; create a minimal IndicatorType so the rest
    # of the demo has something to reference. No cleanup — it's harmless leftover.
    from dhis2_client.generated.v42.schemas.indicator_type import IndicatorType

    type_uid = await _mint_uid(client)
    await client.resources.indicator_types.create(
        IndicatorType(id=type_uid, name=f"Example IT {type_uid[:4]}", factor=1, number=False),
    )
    return type_uid


async def main() -> None:
    """Create one indicator, update its shortName, delete it."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        uid = await _mint_uid(client)
        type_uid = await _ensure_indicator_type(client)
        print(f"minted indicator uid={uid}  indicatorType={type_uid}")

        indicator = Indicator(
            id=uid,
            code=f"EX_IND_{uid}",
            name=f"Example ANC coverage {uid}",
            shortName=f"ANC cov {uid[:4]}",
            # Formula: DHIS2 expression language — `#{DE_UID}` is a data-element placeholder.
            numerator="#{DEancVisit1}",
            numeratorDescription="ANC 1st visits",
            denominator="#{DEancVisit4}",
            denominatorDescription="ANC 4th visits",
            indicatorType=Reference(id=type_uid),
            annualized=False,
        )
        await client.resources.indicators.create(indicator)
        print(f"CREATE  uid={uid}")

        try:
            fetched = await client.resources.indicators.get(
                uid,
                fields="id,name,shortName,numerator,denominator,indicatorType[id,name]",
            )
            print(f"READ    name={fetched.name}  numerator={fetched.numerator}  denominator={fetched.denominator}")

            # PUT-replace through the typed accessor.
            fetched.shortName = f"Updated {uid[:4]}"
            await client.resources.indicators.update(fetched)
            refreshed = await client.resources.indicators.get(uid, fields="id,shortName,lastUpdated")
            print(f"UPDATE  shortName={refreshed.shortName}  lastUpdated={refreshed.lastUpdated}")
        finally:
            await client.resources.indicators.delete(uid)
            print(f"DELETE  {uid}")


if __name__ == "__main__":
    asyncio.run(main())
