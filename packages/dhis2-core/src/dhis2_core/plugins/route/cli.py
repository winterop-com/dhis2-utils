"""Typer sub-app for the `route` plugin (mounted under `dhis2 route`)."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any

import typer

from dhis2_core.plugins.route import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="DHIS2 Route API — register + run integration routes (proxies to external services).",
    no_args_is_help=True,
)


def _print(payload: Any) -> None:
    typer.echo(json.dumps(payload, indent=2))


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    fields: Annotated[str, typer.Option("--fields")] = "id,code,name,url,disabled",
) -> None:
    """List registered routes."""
    _print(asyncio.run(service.list_routes(profile_from_env(), fields=fields)))


@app.command("get")
def get_command(
    uid: Annotated[str, typer.Argument()],
    fields: Annotated[str | None, typer.Option("--fields")] = None,
) -> None:
    """Fetch one route by UID."""
    _print(asyncio.run(service.get_route(profile_from_env(), uid, fields=fields)))


@app.command("add")
def add_command(
    file: Annotated[
        Path | None,
        typer.Option(
            "--file",
            help="JSON file with the route definition (at minimum: code, name, url).",
        ),
    ] = None,
    code: Annotated[str | None, typer.Option("--code")] = None,
    name: Annotated[str | None, typer.Option("--name")] = None,
    url: Annotated[str | None, typer.Option("--url", help="Target URL the route proxies to.")] = None,
    authorities: Annotated[
        str | None,
        typer.Option("--authorities", help="Comma-separated DHIS2 authorities allowed to run this route."),
    ] = None,
) -> None:
    """Create a route via POST /api/routes.

    Either pass a full JSON spec with `--file`, or use the convenience flags
    `--code/--name/--url` for a basic unauthenticated route.
    """
    payload: dict[str, Any]
    if file is not None:
        payload = json.loads(file.read_text(encoding="utf-8"))
    else:
        if not code:
            code = typer.prompt("Route code (stable identifier)")
        if not name:
            name = typer.prompt("Route display name")
        if not url:
            url = typer.prompt("Target URL")
        payload = {"code": code, "name": name, "url": url}
        if authorities:
            payload["authorities"] = [a.strip() for a in authorities.split(",") if a.strip()]
    _print(asyncio.run(service.add_route(profile_from_env(), payload)))


@app.command("update")
def update_command(
    uid: Annotated[str, typer.Argument()],
    file: Annotated[Path, typer.Option("--file", help="JSON file with the full route spec (PUT semantics).")],
) -> None:
    """Replace a route via PUT /api/routes/{uid}.

    DHIS2 PUT expects the complete object. For partial updates use `patch`.
    """
    payload = json.loads(file.read_text(encoding="utf-8"))
    _print(asyncio.run(service.update_route(profile_from_env(), uid, payload)))


@app.command("patch")
def patch_command(
    uid: Annotated[str, typer.Argument()],
    file: Annotated[Path, typer.Option("--file", help="JSON Patch array (RFC 6902).")],
) -> None:
    """Apply a JSON Patch to a route via PATCH /api/routes/{uid}."""
    patch = json.loads(file.read_text(encoding="utf-8"))
    _print(asyncio.run(service.patch_route(profile_from_env(), uid, patch)))


@app.command("delete")
def delete_command(
    uid: Annotated[str, typer.Argument()],
) -> None:
    """Delete a route."""
    _print(asyncio.run(service.delete_route(profile_from_env(), uid)))


@app.command("run")
def run_command(
    uid: Annotated[str, typer.Argument()],
    method: Annotated[str, typer.Option("--method", "-X")] = "GET",
    body_file: Annotated[
        Path | None,
        typer.Option("--body", help="JSON body file for POST/PUT."),
    ] = None,
    sub_path: Annotated[
        str | None,
        typer.Option("--path", help="Additional path segment appended to the route's target URL."),
    ] = None,
) -> None:
    """Execute a route — DHIS2 proxies the request to the configured target URL."""
    body = json.loads(body_file.read_text(encoding="utf-8")) if body_file is not None else None
    _print(
        asyncio.run(
            service.run_route(profile_from_env(), uid, method=method, body=body, sub_path=sub_path),
        )
    )


def register(root_app: Any) -> None:
    """Mount under `dhis2 route`."""
    root_app.add_typer(app, name="route", help="DHIS2 integration routes.")
