"""v41-only — read `app.displayName` from a typed `App`.

The v41 OAS catalogue doesn't declare `displayName` on `App`, but DHIS2's
v41 runtime emits it on `/api/apps` responses regardless. This repo's
`dhis2w_client.v41.apps.App` subclasses the generated `App` and adds
the field locally, plus calls `model_rebuild()` so the subclass
materialises under the parent's `defer_build=True` config.

Without that local override:
- `app.displayName` would fall through to pydantic's `model_extra`
  escape hatch (`app.model_extra["displayName"]`) — untyped.
- Subclass instantiation would raise `App is not fully defined`
  because the parent defers validator build.

This example runs the v41 path so callers see the difference in the
return type. v42 + v43 don't need the override — their OAS lists
`displayName` natively.

Usage:
    uv run python examples/v41/client/v41_apps_display_name.py
"""

from __future__ import annotations

from _runner import run_example
from dhis2w_client.v41 import Dhis2Client
from dhis2w_client.v41.apps import App
from dhis2w_core.client_context import build_auth_for_name
from dhis2w_core.profile import resolve


async def main() -> None:
    """Fetch installed apps via the v41-pinned client and show `displayName` is typed."""
    resolved = resolve()
    _, auth = build_auth_for_name(resolved.name)
    async with Dhis2Client(resolved.profile.base_url, auth=auth) as client:
        installed = await client.apps.list_apps()
        print(f"v41 installed apps ({len(installed)}):")
        for app in installed[:5]:
            # `app.displayName` is typed (Optional[str]) thanks to the v41 subclass.
            # On v42/v43 it would be available via the generated class directly.
            assert isinstance(app, App)
            name = app.displayName or app.name or "(unnamed)"
            print(f"  {app.key or '?':30s}  displayName={name!r}")


if __name__ == "__main__":
    run_example(main)
