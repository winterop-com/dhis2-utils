"""Typer sub-app for `dhis2 files` — documents + fileResources management."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated, Any

import typer
from dhis2_client import FileResourceDomain
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.files import service
from dhis2_core.profile import profile_from_env

_console = Console()

documents_app = typer.Typer(
    help="DHIS2 /api/documents — user-uploaded attachments + external URL links.",
    no_args_is_help=True,
)

resources_app = typer.Typer(
    help="DHIS2 /api/fileResources — typed binary blobs (DATA_VALUE, ICON, MESSAGE_ATTACHMENT).",
    no_args_is_help=True,
)

app = typer.Typer(
    help="DHIS2 file management — documents + file resources.",
    no_args_is_help=True,
)
app.add_typer(documents_app, name="documents", help="Documents (/api/documents).")
app.add_typer(resources_app, name="resources", help="File resources (/api/fileResources).")


# ---- documents ------------------------------------------------------


@documents_app.command("list")
@documents_app.command("ls", hidden=True)
def documents_list_command(
    filter_expr: Annotated[
        str | None,
        typer.Option("--filter", help="DHIS2 filter, e.g. `name:like:Annual`."),
    ] = None,
    page: Annotated[int | None, typer.Option("--page", help="1-indexed page number.")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size", help="Rows per page (default 50).")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List documents."""
    docs = asyncio.run(
        service.list_documents(profile_from_env(), filter=filter_expr, page=page, page_size=page_size),
    )
    if as_json:
        typer.echo("[" + ",".join(doc.model_dump_json(exclude_none=True) for doc in docs) + "]")
        return
    if not docs:
        typer.echo("no documents found")
        return
    table = Table(title=f"DHIS2 documents ({len(docs)})")
    table.add_column("id")
    table.add_column("type")
    table.add_column("name", overflow="fold")
    table.add_column("url or file", overflow="fold")
    for doc in docs:
        kind = "EXTERNAL_URL" if doc.external else "UPLOAD_FILE"
        table.add_row(doc.id or "", kind, doc.name or "", doc.url or "")
    _console.print(table)


@documents_app.command("get")
def documents_get_command(uid: Annotated[str, typer.Argument(help="Document UID.")]) -> None:
    """Show metadata for one document."""
    doc = asyncio.run(service.get_document(profile_from_env(), uid))
    typer.echo(doc.model_dump_json(indent=2, exclude_none=True))


@documents_app.command("upload")
def documents_upload_command(
    file: Annotated[Path, typer.Argument(help="File to upload.")],
    name: Annotated[
        str | None,
        typer.Option("--name", help="Document name (defaults to filename)."),
    ] = None,
) -> None:
    """Upload a binary document — prints the new UID."""
    if not file.is_file():
        raise typer.BadParameter(f"{file} is not a file")
    doc = asyncio.run(service.upload_document(profile_from_env(), file, name=name))
    typer.echo(f"uploaded {doc.id}  {doc.name}")


@documents_app.command("upload-url")
def documents_upload_url_command(
    name: Annotated[str, typer.Argument(help="Document display name.")],
    url: Annotated[str, typer.Argument(help="External URL DHIS2 will link to.")],
) -> None:
    """Create an EXTERNAL_URL document — no bytes uploaded; DHIS2 links out to `url`."""
    doc = asyncio.run(service.create_external_document(profile_from_env(), name=name, url=url))
    typer.echo(f"created {doc.id}  {doc.name}  -> {url}")


@documents_app.command("download")
def documents_download_command(
    uid: Annotated[str, typer.Argument(help="Document UID.")],
    destination: Annotated[Path, typer.Argument(help="Output file path.")],
) -> None:
    """Download the binary payload to `destination`."""
    written = asyncio.run(service.download_document(profile_from_env(), uid, destination))
    typer.echo(f"wrote {written} bytes to {destination}")


@documents_app.command("delete")
def documents_delete_command(uid: Annotated[str, typer.Argument(help="Document UID.")]) -> None:
    """Delete one document."""
    asyncio.run(service.delete_document(profile_from_env(), uid))
    typer.echo(f"deleted {uid}")


# ---- file resources -------------------------------------------------


@resources_app.command("upload")
def resources_upload_command(
    file: Annotated[Path, typer.Argument(help="File to upload as a fileResource.")],
    domain: Annotated[
        FileResourceDomain,
        typer.Option(
            "--domain",
            help="FileResource domain (DATA_VALUE, ICON, MESSAGE_ATTACHMENT, ...).",
            case_sensitive=False,
        ),
    ] = FileResourceDomain.DATA_VALUE,
) -> None:
    """Upload a file resource; prints the new UID (reference it from the owning metadata object)."""
    if not file.is_file():
        raise typer.BadParameter(f"{file} is not a file")
    fr = asyncio.run(service.upload_file_resource(profile_from_env(), file, domain=domain))
    typer.echo(f"uploaded {fr.id}  domain={fr.domain}  name={fr.name}")


@resources_app.command("get")
def resources_get_command(uid: Annotated[str, typer.Argument(help="FileResource UID.")]) -> None:
    """Show metadata for one file resource."""
    fr = asyncio.run(service.get_file_resource(profile_from_env(), uid))
    typer.echo(fr.model_dump_json(indent=2, exclude_none=True))


@resources_app.command("download")
def resources_download_command(
    uid: Annotated[str, typer.Argument(help="FileResource UID.")],
    destination: Annotated[Path, typer.Argument(help="Output file path.")],
) -> None:
    """Download the file-resource payload to `destination`."""
    written = asyncio.run(service.download_file_resource(profile_from_env(), uid, destination))
    typer.echo(f"wrote {written} bytes to {destination}")


def register(parent_app: Any) -> None:
    """Mount `dhis2 files` on the root CLI."""
    parent_app.add_typer(app, name="files", help="Manage DHIS2 documents + file resources.")
