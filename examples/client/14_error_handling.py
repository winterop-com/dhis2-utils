"""Error handling — Dhis2ApiError, WebMessage conflicts, AuthenticationError.

Every DHIS2 non-2xx is raised as `Dhis2ApiError` with the full JSON body
attached. `error.web_message` lazily parses the body into a typed
`WebMessageResponse` so callers can inspect `conflicts[]`, `importCount`,
`rejectedIndexes[]`, and `errorReports[]` without re-parsing strings.

Usage:
    uv run python examples/client/14_error_handling.py

Env: same as 01_whoami.py.
"""

from __future__ import annotations

import asyncio
import os

from dhis2_client import (
    AuthenticationError,
    AuthProvider,
    BasicAuth,
    DataValue,
    DataValueSet,
    Dhis2,
    Dhis2ApiError,
    Dhis2Client,
    PatAuth,
)


def _auth_from_env() -> AuthProvider:
    """Pick PAT or Basic based on what's in the environment."""
    pat = os.environ.get("DHIS2_PAT")
    if pat:
        return PatAuth(token=pat)
    return BasicAuth(
        username=os.environ.get("DHIS2_USERNAME", "admin"),
        password=os.environ.get("DHIS2_PASSWORD", "district"),
    )


async def demo_409_with_conflicts(client: Dhis2Client) -> None:
    """Push a data value for a period outside the dataset's open-future window.

    DHIS2 returns 409 with a populated `conflicts[]` block describing the
    rejection — classic `E7641` (period past open-future-period window).
    """
    future = DataValueSet(
        dataValues=[
            DataValue(
                dataElement="DEancVisit1",
                period="202712",  # far-future period the seeded dataset won't accept
                orgUnit="NOROsloProv",
                value="99",
            ),
        ],
    )
    try:
        await client.post_raw("/api/dataValueSets", future.model_dump(exclude_none=True))
    except Dhis2ApiError as exc:
        print(f"\n[Dhis2ApiError] {exc.status_code}: {exc.message}")
        envelope = exc.web_message
        if envelope is None:
            print("  body was not a WebMessage dict")
            return
        counts = envelope.import_count()
        if counts is not None:
            print(
                f"  import_count: imported={counts.imported} updated={counts.updated}"
                f" ignored={counts.ignored} deleted={counts.deleted}"
            )
        for conflict in envelope.conflicts():
            print(f"  conflict: {conflict.property} = {conflict.value} [{conflict.errorCode}]")
        print(f"  rejected_indexes: {envelope.rejected_indexes()}")


async def demo_404(client: Dhis2Client) -> None:
    """GET a resource that doesn't exist — 404 -> Dhis2ApiError."""
    try:
        await client.resources.data_elements.get("nonexistent123")
    except Dhis2ApiError as exc:
        print(f"\n[Dhis2ApiError] {exc.status_code}: {exc.message}")
        if isinstance(exc.body, dict):
            print(f"  body message: {exc.body.get('message')}")


async def demo_auth_failure(base_url: str) -> None:
    """Wrong basic-auth password raises `AuthenticationError` (401)."""
    bad = Dhis2Client(base_url, auth=BasicAuth(username="admin", password="definitely-wrong"))
    try:
        async with bad as client:
            await client.system.me()
    except AuthenticationError as exc:
        print(f"\n[AuthenticationError] {exc}")
    except Dhis2ApiError as exc:
        # DHIS2 sometimes responds 400 (instead of 401) when the *credential
        # shape* is rejected (unknown PAT token, malformed header). Still a
        # typed `Dhis2ApiError` with a useful body.
        print(f"\n[Dhis2ApiError] {exc.status_code}: {exc.message}")


async def main() -> None:
    """Exercise the three error paths callers are most likely to hit."""
    base_url = os.environ.get("DHIS2_URL", "http://localhost:8080")
    async with Dhis2Client(base_url, auth=_auth_from_env(), version=Dhis2.V42) as client:
        await demo_409_with_conflicts(client)
        await demo_404(client)
    await demo_auth_failure(base_url)


if __name__ == "__main__":
    asyncio.run(main())
