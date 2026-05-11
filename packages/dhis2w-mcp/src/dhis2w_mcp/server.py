"""FastMCP server entry for dhis2w-mcp — mounts plugins from dhis2w-core."""

from __future__ import annotations

import typing

from dhis2w_core.plugin import discover_plugins, resolve_startup_version
from fastmcp import FastMCP
from pydantic import BaseModel


def build_server() -> FastMCP:
    """Create the FastMCP instance with every discovered plugin registered."""
    server = FastMCP(name="dhis2")
    for plugin in discover_plugins(resolve_startup_version()):
        plugin.register_mcp(server)
    _eager_rebuild_tool_return_types(server)
    return server


def main() -> None:
    """Console-script entrypoint: build the server and run it over stdio."""
    build_server().run()


def _eager_rebuild_tool_return_types(server: FastMCP) -> None:
    """Resolve forward refs on every pydantic class reachable from a tool return type.

    Pydantic v2 lazily builds `__pydantic_validator__` on first
    `model_validate`, but `__pydantic_serializer__` stays as `MockValSer`
    until `model_rebuild()` runs explicitly. FastMCP serializes tool
    returns directly through the model serializer (no prior validation
    happens on the path), so any class declared with `defer_build=True`
    raises `'MockValSer' object is not an instance of 'SchemaSerializer'`.

    Every OAS-emitted pydantic class uses `defer_build=True` to keep
    `dhis2 --help` startup fast (skipping the eager rebuild loop saves
    ~900 ms of CLI boot time). MCP server boot is the right place to
    pay that cost — this server is long-lived, the rebuild happens once,
    and skipping it leaves tool returns silently broken.

    Walks every registered tool's return-type annotation and calls
    `model_rebuild()` on every pydantic class encountered (including
    inside `list[X]`, `dict[..., X]`, `X | Y` unions, and similar
    generics). Reads from `server.providers[*]._components` so this
    runs synchronously even when `build_server()` is called inside an
    async context (in-process MCP integration tests + examples).
    """
    seen: set[type[BaseModel]] = set()

    def _rebuild(annotation: object) -> None:
        if annotation is None or annotation is type(None):
            return
        if isinstance(annotation, type) and issubclass(annotation, BaseModel) and annotation not in seen:
            seen.add(annotation)
            annotation.model_rebuild()
            return
        for arg in typing.get_args(annotation):
            _rebuild(arg)

    for provider in server.providers:
        # FastMCP exposes only an async `list_tools()`; the sync source of truth
        # is `_components` on each LocalProvider. Read via `getattr` so the
        # type-checker doesn't reject the protocol-typed `provider` here.
        components = getattr(provider, "_components", None)
        if not components:
            continue
        for component in components.values():
            _rebuild(getattr(component, "return_type", None))


if __name__ == "__main__":
    main()
