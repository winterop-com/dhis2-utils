"""Typer sub-app for `dhis2 dev` — codegen, uid, oauth2 + PAT provisioning, sample fixtures."""

from __future__ import annotations

import asyncio
import os
import time
from typing import Annotated, Any

import typer
from dhis2_client import Dhis2Client, PatAuth
from dhis2_codegen.cli import app as codegen_app

from dhis2_core.client_context import open_client
from dhis2_core.oauth2_registration import build_admin_auth, register_oauth2_client
from dhis2_core.pat_registration import register_pat
from dhis2_core.plugins.route import service as route_service
from dhis2_core.plugins.system import service as system_service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Developer/operator tools.", no_args_is_help=True)
app.add_typer(codegen_app, name="codegen", help="Generate version-aware DHIS2 client code from /api/schemas.")

oauth2_app = typer.Typer(help="Manage DHIS2 OAuth2 clients on the server (admin ops).", no_args_is_help=True)
oauth2_client_app = typer.Typer(help="OAuth2 client registrations at /api/oAuth2Clients.", no_args_is_help=True)
oauth2_app.add_typer(oauth2_client_app, name="client")
app.add_typer(oauth2_app, name="oauth2")

pat_app = typer.Typer(help="Personal Access Tokens — provision PATs on DHIS2.", no_args_is_help=True)
app.add_typer(pat_app, name="pat")

sample_app = typer.Typer(
    help="Inject known-good fixtures to verify the stack end-to-end (route, data, pat).",
    no_args_is_help=True,
)
app.add_typer(sample_app, name="sample")


def _resolve_admin_auth(admin_user: str | None) -> Any:
    """Build an admin auth provider from env + prompt — NEVER from argv secrets."""
    admin_pat = os.environ.get("DHIS2_ADMIN_PAT")
    admin_pass = os.environ.get("DHIS2_ADMIN_PASSWORD")
    if not admin_pat and not admin_pass:
        if admin_user or typer.confirm("Bootstrap with username+password? (no = PAT)", default=True):
            if not admin_user:
                admin_user = typer.prompt("Admin username", default="admin")
            admin_pass = typer.prompt("Admin password", hide_input=True)
        else:
            admin_pat = typer.prompt("Admin PAT", hide_input=True)
    return build_admin_auth(pat=admin_pat, username=admin_user, password=admin_pass)


@app.command("uid")
def uid_command(
    count: Annotated[
        int,
        typer.Option("--count", "-n", min=1, max=10000, help="How many UIDs to generate."),
    ] = 1,
) -> None:
    """Generate fresh 11-char DHIS2 UIDs via `/api/system/id` — one per line."""
    codes = asyncio.run(system_service.generate_uids(profile_from_env(), limit=count))
    for code in codes:
        typer.echo(code)


@oauth2_client_app.command("register")
def oauth2_client_register_command(
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    client_id: Annotated[str, typer.Option("--client-id")] = "dhis2-utils-local",
    redirect_uri: Annotated[str, typer.Option("--redirect-uri")] = "http://localhost:8765",
    scope: Annotated[str, typer.Option("--scope")] = "ALL",
    display_name: Annotated[str | None, typer.Option("--name")] = None,
) -> None:
    """Register an OAuth2 client on DHIS2 via POST /api/oAuth2Clients.

    Secrets (admin credentials, client_secret) come from env or interactive
    prompt — never argv.

    Prints `client_id` + metadata UID so they can be piped into
    `dhis2 profile add --auth oauth2 ...`. For a one-shot bootstrap (register
    + save profile + log in) use `dhis2 profile bootstrap` instead.
    """
    resolved_url: str = url or os.environ.get("DHIS2_URL") or typer.prompt("DHIS2 base URL")
    admin_auth = _resolve_admin_auth(admin_user)
    client_secret = os.environ.get("DHIS2_OAUTH_CLIENT_SECRET") or typer.prompt(
        f"New client_secret for {client_id!r}", hide_input=True
    )
    creds = asyncio.run(
        register_oauth2_client(
            base_url=resolved_url,
            admin_auth=admin_auth,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            display_name=display_name,
        )
    )
    typer.echo(f"registered oauth2 client at {resolved_url}")
    typer.echo(f"  uid={creds.uid}")
    typer.echo(f"  client_id={creds.client_id}")
    typer.echo(f"  redirect_uri={creds.redirect_uri}")
    typer.echo(f"  scope={creds.scope}")
    typer.secho(
        "  client_secret not echoed — export as DHIS2_OAUTH_CLIENT_SECRET or use profile add", fg=typer.colors.YELLOW
    )


@pat_app.command("create")
def pat_create_command(
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    expires_in_days: Annotated[int | None, typer.Option("--expires-in-days")] = None,
    allowed_ip: Annotated[
        list[str] | None,
        typer.Option("--allowed-ip", help="IP allowlist entry; repeat for multiple."),
    ] = None,
    allowed_method: Annotated[
        list[str] | None,
        typer.Option("--allowed-method", help="HTTP method allowlist; repeat for each method."),
    ] = None,
    allowed_referrer: Annotated[
        list[str] | None,
        typer.Option("--allowed-referrer", help="Referer allowlist entry; repeat for multiple."),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Print only the PAT value, suitable for $(command substitution)."),
    ] = False,
) -> None:
    """Create a DHIS2 Personal Access Token via POST /api/apiToken.

    Admin creds come from env or prompt (never argv). The PAT value is only
    returned once by DHIS2 — capture it here and pipe into a profile:

        export DHIS2_PAT=$(dhis2 dev pat create --url $URL -q)
        dhis2 profile add local --url $URL --auth pat

    Or use `dhis2 profile bootstrap --auth pat` for a one-shot setup.
    """
    resolved_url: str = url or os.environ.get("DHIS2_URL") or typer.prompt("DHIS2 base URL")
    admin_auth = _resolve_admin_auth(admin_user)
    creds = asyncio.run(
        register_pat(
            base_url=resolved_url,
            admin_auth=admin_auth,
            description=description,
            expires_in_days=expires_in_days,
            allowed_ips=allowed_ip,
            allowed_methods=allowed_method,
            allowed_referrers=allowed_referrer,
        )
    )
    if quiet:
        typer.echo(creds.token)
    else:
        typer.echo(f"registered PAT at {resolved_url}")
        typer.echo(f"  uid={creds.uid}")
        if creds.description:
            typer.echo(f"  description={creds.description}")
        typer.echo(f"  token={creds.token}")
        typer.secho(
            "  this value is shown ONCE by DHIS2 — save it now (export DHIS2_PAT=... or profile add)",
            fg=typer.colors.YELLOW,
        )


def _ok(msg: str) -> None:
    typer.secho(f"  OK  {msg}", fg=typer.colors.GREEN)


def _fail(msg: str) -> None:
    typer.secho(f"  FAIL  {msg}", fg=typer.colors.RED)


def _step(label: str) -> None:
    typer.secho(f"- {label}", fg=typer.colors.CYAN)


@sample_app.command("route")
def sample_route_command(
    target_url: Annotated[
        str, typer.Option("--url", help="URL the sample route will proxy to.")
    ] = "https://httpbin.org/get",
    code: Annotated[str, typer.Option("--code")] = "SMOKE_ROUTE",
    keep: Annotated[bool, typer.Option("--keep", help="Don't delete the sample route afterwards.")] = False,
) -> None:
    """Create a sample route, run it, and (unless --keep) delete it.

    Verifies the full /api/routes lifecycle end-to-end: create -> run (proxy
    to target URL) -> delete. Prints PASS/FAIL per step with timings.
    """
    started = time.perf_counter()
    profile = profile_from_env()
    _step(f"create route code={code!r} -> {target_url}")
    created = asyncio.run(route_service.add_route(profile, {"code": code, "name": f"sample {code}", "url": target_url}))
    uid = created.get("response", {}).get("uid") or created.get("id") or ""
    if not uid:
        _fail(f"no uid in POST response: {created}")
        raise typer.Exit(1)
    _ok(f"created uid={uid}")

    try:
        _step("run route (DHIS2 proxies to target)")
        response = asyncio.run(route_service.run_route(profile, uid))
        preview = str(response)[:200]
        _ok(f"ran -> {preview}{'...' if len(str(response)) > 200 else ''}")
    finally:
        if keep:
            _ok(f"--keep set; route {uid} left in place (delete with `dhis2 route delete {uid}`)")
        else:
            _step(f"delete route {uid}")
            asyncio.run(route_service.delete_route(profile, uid))
            _ok("deleted")

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    typer.secho(f"PASS ({elapsed_ms} ms)", fg=typer.colors.GREEN, bold=True)


@sample_app.command("pat")
def sample_pat_command(
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    keep: Annotated[bool, typer.Option("--keep", help="Don't delete the sample PAT afterwards.")] = False,
) -> None:
    """Create a sample PAT, use it to call /api/me, then (unless --keep) delete it.

    End-to-end PAT lifecycle: POST /api/apiToken -> GET /api/me with the new
    token -> DELETE /api/apiToken/{uid}. Confirms both provisioning and
    bearer-token acceptance.
    """
    started = time.perf_counter()
    resolved_url: str = (
        url or os.environ.get("DHIS2_URL") or profile_from_env().base_url or typer.prompt("DHIS2 base URL")
    )
    admin_auth = _resolve_admin_auth(admin_user)

    _step("create PAT via /api/apiToken")
    creds = asyncio.run(
        register_pat(
            base_url=resolved_url,
            admin_auth=admin_auth,
            description="dhis2 dev sample pat (smoke test)",
        )
    )
    _ok(f"uid={creds.uid}, token={creds.token[:12]}... (redacted)")

    async def _use_pat_and_maybe_delete() -> None:
        _step("call /api/me with the new PAT")
        pat_auth = PatAuth(token=creds.token)
        async with Dhis2Client(resolved_url, auth=pat_auth) as probe:
            me = await probe.get_raw("/api/me")
        _ok(f"authenticated as {me.get('username')!r} via the new PAT")
        if keep:
            _ok(f"--keep set; PAT {creds.uid} left in place")
            return
        _step(f"delete PAT {creds.uid}")
        async with Dhis2Client(resolved_url, auth=admin_auth) as admin:
            await admin.delete_raw(f"/api/apiToken/{creds.uid}")
        _ok("deleted")

    asyncio.run(_use_pat_and_maybe_delete())
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    typer.secho(f"PASS ({elapsed_ms} ms)", fg=typer.colors.GREEN, bold=True)


@sample_app.command("data-value")
def sample_data_value_command(
    data_element: Annotated[str, typer.Option("--de", help="DataElement UID.")] = "DEancVisit1",
    org_unit: Annotated[str, typer.Option("--ou", help="OrganisationUnit UID.")] = "NOROsloProv",
    period: Annotated[str, typer.Option("--pe", help="Period (e.g. 202603).")] = "202603",
    value: Annotated[str, typer.Option("--value")] = "42",
    keep: Annotated[bool, typer.Option("--keep", help="Don't delete the sample data value afterwards.")] = False,
) -> None:
    """Write a sample data value, read it back, and (unless --keep) delete it.

    Uses the seeded NORMonthDS1 fixture by default — override with --de/--ou/--pe
    to target different scope. Verifies both the write path (/api/dataValueSets)
    and the read path (/api/dataValueSets.json?dataElement=...&orgUnit=...&period=...).
    """
    started = time.perf_counter()
    profile = profile_from_env()

    async def _run() -> None:
        async with open_client(profile) as client:
            _step(f"POST /api/dataValueSets  {data_element}/{period}/{org_unit} = {value}")
            payload = {
                "dataValues": [{"dataElement": data_element, "period": period, "orgUnit": org_unit, "value": value}]
            }
            response = await client.post_raw("/api/dataValueSets", payload)
            import_count = response.get("response", {}).get("importCount", {})
            _ok(f"import_count={import_count}")

            _step("GET /api/dataValueSets.json (read-back)")
            read = await client.get_raw(
                "/api/dataValueSets.json",
                params={"dataElement": data_element, "orgUnit": org_unit, "period": period},
            )
            values = read.get("dataValues", [])
            matched = [v for v in values if v.get("value") == value]
            if not matched:
                _fail(f"wrote {value!r} but did not see it in {values}")
                raise typer.Exit(1)
            _ok(f"read-back contains value={matched[0].get('value')!r}")

            if keep:
                _ok("--keep set; data value left in place")
                return
            _step("delete via importStrategy=DELETE")
            await client.post_raw("/api/dataValueSets", payload, params={"importStrategy": "DELETE"})
            _ok("deleted (soft-delete — DHIS2 keeps the row marked deleted=true; see BUGS.md #2)")

    asyncio.run(_run())
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    typer.secho(f"PASS ({elapsed_ms} ms)", fg=typer.colors.GREEN, bold=True)


@sample_app.command("all")
def sample_all_command(
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    keep: Annotated[bool, typer.Option("--keep", help="Don't delete the fixtures afterwards.")] = False,
) -> None:
    """Run every sample in sequence — route, data-value, pat — against the default profile."""
    typer.secho("=== dhis2 dev sample route ===", fg=typer.colors.MAGENTA, bold=True)
    sample_route_command(keep=keep)
    typer.echo()
    typer.secho("=== dhis2 dev sample data-value ===", fg=typer.colors.MAGENTA, bold=True)
    sample_data_value_command(keep=keep)
    typer.echo()
    typer.secho("=== dhis2 dev sample pat ===", fg=typer.colors.MAGENTA, bold=True)
    sample_pat_command(url=url, admin_user=admin_user, keep=keep)


def register(root_app: Any) -> None:
    """Mount under `dhis2 dev`."""
    root_app.add_typer(app, name="dev", help="Developer/operator tools.")
