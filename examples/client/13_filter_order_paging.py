"""Metadata query DSL — filters, rootJunction, order, server-side paging.

Shows the full DHIS2 `/api/<resource>` query surface through the generated
typed accessor: multiple `filter=` params combined via `rootJunction`,
multi-clause `order=`, explicit `page` + `pageSize`, and the "dump it all"
variant (`paging=False`).

Usage:
    uv run python examples/client/13_filter_order_paging.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os

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


async def main() -> None:
    """Walk through the filter / order / paging surface on dataElements + orgUnits."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        # 1. Single filter.
        only_anc = await client.resources.data_elements.list(
            filters=["name:like:ANC"],
            fields="id,name",
        )
        print(f"name:like:ANC -> {len(only_anc)} elements")

        # 2. Multi-filter with OR junction (default is AND).
        anc_or_delivery = await client.resources.data_elements.list(
            filters=["name:like:ANC", "code:eq:DEdelFacilt"],
            root_junction="OR",
            fields="id,name,code",
        )
        print(f"name:like:ANC OR code:eq:DEdelFacilt -> {len(anc_or_delivery)} elements")

        # 3. Ordered + paged (server-side).
        sorted_ous = await client.resources.organisation_units.list(
            order=["level:asc", "name:asc"],
            page_size=5,
            page=2,
            fields="id,name,level",
        )
        print("\npage 2, 5/page, order=level:asc,name:asc:")
        for ou in sorted_ous:
            print(f"  level={ou.level}  id={ou.id}  name={ou.name}")

        # 4. paging=False — every row in one response. Use `list_raw` when you
        # want the `pager` metadata alongside the rows.
        all_des = await client.resources.data_elements.list(
            paging=False,
            fields=":identifiable",
        )
        print(f"\npaging=False, fields=:identifiable -> {len(all_des)} data elements (single request)")

        # 5. list_raw gives the envelope too.
        envelope = await client.resources.organisation_units.list_raw(
            page_size=3,
            page=1,
            fields="id,name",
        )
        pager = envelope.get("pager") or {}
        print(f"\npager: page={pager.get('page')}/{pager.get('pageCount')}  total={pager.get('total')}")


if __name__ == "__main__":
    asyncio.run(main())
