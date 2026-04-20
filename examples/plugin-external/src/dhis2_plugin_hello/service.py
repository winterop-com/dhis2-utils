"""Service layer — where an external plugin does its work.

Imports `dhis2-core`'s `open_client` + `Profile` the same way first-party
plugins do. No difference in API surface between first-party and external.
"""

from __future__ import annotations

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


async def greet(profile: Profile, *, greeting: str = "Hello") -> str:
    """Greet the authenticated user by their displayName."""
    async with open_client(profile) as client:
        me = await client.system.me()
    name = me.displayName or me.username or "stranger"
    return f"{greeting}, {name}!"
