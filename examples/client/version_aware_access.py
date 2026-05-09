"""Version-aware access to v42 / v43 schemas — branch on `client.version_key`.

Hand-written client helpers (`client.system.info`, `client.dashboards.get`,
`client.tracked_entity_attributes.get`) parse responses against the v42
generated models. For most fields that's fine — the v42 and v43 shapes
are structurally compatible. For a handful of breaking-shape schemas,
or for v43-only fields, you have three options. This example demonstrates
all three:

1. Inspect `client.version_key` and branch.
2. Bypass the helper and import from `dhis2w_client.generated.v43.*`
   directly to get a v43-typed pydantic model.
3. Pin the client up-front with `version=Dhis2.V43` to skip auto-detect.

For the full per-resource diff and the breaking-shape schema list, see
`docs/architecture/schema-diff-v42-v43.md`. The narrative version of the
patterns below is at `docs/architecture/versioning.md`.

Usage:
    # Run against whichever profile is active (works on v42 or v43)
    uv run python examples/client/version_aware_access.py

    # Force v43 — use a profile pointing at a v43 instance
    DHIS2_PROFILE=v43-play uv run python examples/client/version_aware_access.py
"""

from __future__ import annotations

from typing import Any

from _runner import run_example
from dhis2w_client.generated.v43.schemas.tracked_entity_attribute import (
    TrackedEntityAttribute as TrackedEntityAttributeV43,
)
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env


async def main() -> None:
    """Walk the three patterns for accessing v43-specific fields."""
    async with open_client(profile_from_env()) as client:
        version = client.version_key
        info = await client.system.info()
        print(f"connected to DHIS2 {info.version} -> module {version}")

        # Pattern 1 — branch on `client.version_key`. The hand-written
        # `client.dashboards` accessor returns a v42-typed `Dashboard`. On
        # v43 wire data the renamed `users` field on each `DashboardItem`
        # ends up under `model_extra`, because the v42 model has a singular
        # `user` field instead. Same dashboard object, different access path.
        dashboards = await client.dashboards.list_all()
        if not dashboards:
            print("no dashboards on this instance — skipping dashboard demo")
        else:
            dashboard = dashboards[0]
            print(f"dashboard {dashboard.id} name={dashboard.name!r}")
            for item in dashboard.dashboardItems or []:
                if version == "v43":
                    extras: dict[str, Any] = item.model_extra or {}
                    users = extras.get("users") or []
                    user_label = f"users={[u.get('id') for u in users]}"
                else:
                    user_label = f"user={getattr(item.user, 'id', None)!r}"
                print(f"  item {item.id} type={item.type} {user_label}")

        # Pattern 2 — direct `dhis2w_client.generated.v43.*` import. The
        # v42-pinned helper would parse this against the v42
        # `TrackedEntityAttribute` (where `favorite: bool` and the new
        # search-tuning fields don't exist). Going through the v43 model
        # directly gets typed access to `favorites: list[str]` plus
        # `trigramIndexed`, `minCharactersToSearch`, etc.
        if version == "v43":
            existing = await client.tracked_entity_attributes.list_all(page_size=1)
            if existing:
                uid = existing[0].id or ""
                raw = await client.get_raw(f"/api/trackedEntityAttributes/{uid}")
                attribute_v43 = TrackedEntityAttributeV43.model_validate(raw)
                print(
                    f"TEA {attribute_v43.id} favorites={attribute_v43.favorites} "
                    f"trigramIndexed={attribute_v43.trigramIndexed} "
                    f"minCharactersToSearch={attribute_v43.minCharactersToSearch}"
                )
            else:
                print("no tracked-entity attributes on this instance — skipping TEA demo")
        else:
            print(f"server is {version}; v43-typed TEA demo skipped (would parse against the wrong shape)")

        # Pattern 3 — pin the client to a known version. Useful when you
        # control the deployment and want to skip the /api/system/info
        # round-trip on connect, or you want connect() to fail fast against
        # a server you didn't expect. See the docstring on `Dhis2Client`
        # for `version=Dhis2.V42` / `Dhis2.V43`.
        print("pattern 3 (pin via version=Dhis2.V43) is shown in the docstring; not run here")


if __name__ == "__main__":
    run_example(main)
