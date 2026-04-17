"""Service layer for the `metadata` plugin — thin wrapper over generated resources."""

from __future__ import annotations

import re
from typing import Any

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")


class UnknownResourceError(LookupError):
    """Raised when a caller asks for a metadata resource not present on this instance."""


def _attr_name(resource: str) -> str:
    """Convert a DHIS2 resource name (camelCase plural) to a Resources attribute name."""
    return _CAMEL_RE.sub("_", resource).lower()


def _resource_names(resources: object) -> list[str]:
    return sorted(name for name in dir(resources) if not name.startswith("_"))


async def list_resource_types(profile: Profile) -> list[str]:
    """Return every metadata resource type exposed by the instance's generated client."""
    async with open_client(profile) as client:
        return _resource_names(client.resources)


async def list_metadata(
    profile: Profile,
    resource: str,
    *,
    fields: str | None = None,
    filter: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """List a metadata resource (e.g. `dataElements`, `indicators`).

    Returns dumped-dict form so MCP tool calls can serialise the result. The
    `limit` is applied client-side because not every DHIS2 resource honours
    `pageSize` in the single-page shape we use.
    """
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        models = await accessor.list(fields=fields, filter=filter)
        if limit is not None:
            models = models[:limit]
        return [_dump(model) for model in models]


async def get_metadata(
    profile: Profile,
    resource: str,
    uid: str,
    *,
    fields: str | None = None,
) -> dict[str, Any]:
    """Fetch one metadata object by UID; returns the dumped-dict form."""
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        model = await accessor.get(uid, fields=fields)
        return _dump(model)


def _resolve_accessor(resources: object, resource: str) -> Any:
    attr = _attr_name(resource)
    accessor = getattr(resources, attr, None)
    if accessor is None:
        available = _resource_names(resources)
        raise UnknownResourceError(
            f"unknown metadata resource {resource!r} (tried attribute {attr!r}); "
            f"this instance exposes {len(available)} types — call `list_resource_types` to see them"
        )
    return accessor


def _dump(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        dumped = model.model_dump(by_alias=True, exclude_none=True, mode="json")
        if isinstance(dumped, dict):
            return dumped
    if isinstance(model, dict):
        return model
    raise TypeError(f"cannot dump {type(model).__name__} to a dict")
