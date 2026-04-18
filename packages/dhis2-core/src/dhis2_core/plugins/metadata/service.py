"""Service layer for the `metadata` plugin — thin wrapper over generated resources."""

from __future__ import annotations

import re
from collections.abc import AsyncIterator
from typing import Any

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")
_STREAM_PAGE_SIZE = 500


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
    filters: list[str] | None = None,
    root_junction: str | None = None,
    order: list[str] | None = None,
    page: int | None = None,
    page_size: int | None = None,
    paging: bool | None = None,
    translate: bool | None = None,
    locale: str | None = None,
) -> list[dict[str, Any]]:
    """List a metadata resource (e.g. `dataElements`, `indicators`).

    Every DHIS2 `/api/<resource>` query parameter is forwarded. `filters` and
    `order` may repeat — a list of strings becomes `?filter=a&filter=b`.
    `root_junction` is `"AND"` (default) or `"OR"`. `paging=False` returns the
    full catalog in one response; for memory-friendly streaming use
    `iter_metadata`.

    Returns dumped-dict form so MCP tool calls can serialise the result.
    """
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        models = await accessor.list(
            fields=fields,
            filters=filters,
            root_junction=root_junction,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
            translate=translate,
            locale=locale,
        )
        return [_dump(model) for model in models]


async def iter_metadata(
    profile: Profile,
    resource: str,
    *,
    fields: str | None = None,
    filters: list[str] | None = None,
    root_junction: str | None = None,
    order: list[str] | None = None,
    page_size: int = _STREAM_PAGE_SIZE,
    translate: bool | None = None,
    locale: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Stream every row of a metadata resource as dumped dicts, one at a time.

    Walks successive pages server-side (`page=1`, `page=2`, ...) stopping when
    a page returns fewer rows than `page_size`. `page_size` defaults to 500 —
    large enough to keep request count low, small enough not to blow memory on
    heavy fields selectors.
    """
    page = 1
    async with open_client(profile) as client:
        accessor = _resolve_accessor(client.resources, resource)
        while True:
            models = await accessor.list(
                fields=fields,
                filters=filters,
                root_junction=root_junction,
                order=order,
                page=page,
                page_size=page_size,
                paging=True,
                translate=translate,
                locale=locale,
            )
            if not models:
                return
            for model in models:
                yield _dump(model)
            if len(models) < page_size:
                return
            page += 1


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
