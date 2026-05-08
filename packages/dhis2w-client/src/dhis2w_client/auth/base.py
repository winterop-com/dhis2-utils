"""AuthProvider protocol for pluggable DHIS2 authentication."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class AuthProvider(Protocol):
    """Injects authentication headers into outgoing DHIS2 requests."""

    async def headers(self) -> dict[str, str]:
        """Return headers to apply to the next request."""
        ...

    async def refresh_if_needed(self) -> None:
        """Refresh credentials when close to expiry; no-op for static auth."""
        ...
