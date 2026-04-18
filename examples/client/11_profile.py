"""Use a DHIS2 profile from Python (via dhis2-core's `open_client`).

`dhis2-client` stays deliberately profile-agnostic — it takes a base URL
and an `AuthProvider` and that's it. The profile layer (TOML discovery,
Basic/PAT/OAuth2 resolution, token storage) lives in `dhis2-core`.

If you want profiles in your own Python script, import `dhis2-core`'s
`open_client` — same helper the CLI and MCP plugins use internally. Pass
a profile name (or `None` for the default from `profiles.toml` /
`DHIS2_PROFILE` env) and you get back a connected `Dhis2Client`.

Usage:
    uv run python examples/client/11_profile.py            # default profile
    uv run python examples/client/11_profile.py local      # by name

Requires a profile configured, e.g.
    dhis2 profile add local --url http://localhost:8080 --auth pat --token "$DHIS2_PAT" --default
"""

from __future__ import annotations

import asyncio
import sys

from dhis2_core.client_context import open_client
from dhis2_core.profile import resolve


async def main(profile_name: str | None) -> None:
    """Resolve the profile, open a client against it, call /api/me."""
    resolved = resolve(profile_name)  # uses the full precedence ladder
    print(f"profile: {resolved.name}  source: {resolved.source}  url: {resolved.profile.base_url}")
    async with open_client(resolved.profile, profile_name=resolved.name) as client:
        me = await client.system.me()
        info = await client.system.info()
        print(f"  DHIS2 {info.version} — {me.username} ({me.displayName or '-'})")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None))
