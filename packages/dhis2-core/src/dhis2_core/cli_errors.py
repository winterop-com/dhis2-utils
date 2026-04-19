"""Clean-error rendering for CLI commands.

Expected user-facing errors get printed as a one-line message (in red, on
stderr) plus a short hint block, then exit 1. Programming bugs (AssertionError,
KeyError, etc.) still propagate and show a full traceback so they can be
triaged.
"""

from __future__ import annotations

import sys
from typing import NoReturn

import typer
from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.errors import AuthenticationError, Dhis2ApiError, Dhis2ClientError

from dhis2_core.plugins.profile.service import ProfileAlreadyExistsError
from dhis2_core.profile import (
    InvalidProfileNameError,
    NoProfileError,
    UnknownProfileError,
)

_NO_PROFILE_HINT = [
    "run `dhis2 profile --help` for setup options, or try:",
    "  dhis2 profile list                             # see what's configured",
    "  dhis2 profile add <name> --scope global \\",
    "      --url https://dhis2.example.org \\",
    "      --auth pat --token d2p_... --default",
    "  dhis2 profile verify <name>                    # confirm auth works",
]

_UNKNOWN_PROFILE_HINT = [
    "run `dhis2 profile list` to see available profiles",
    "or `dhis2 profile add <name> ...` to create one",
]

_INVALID_NAME_HINT = [
    "profile names must start with a letter and contain only letters,",
    "digits, and underscores (e.g. 'local', 'prod_eu', 'laohis42').",
]

_AUTH_HINT = [
    "run `dhis2 profile verify <name>` to confirm auth",
    "or `dhis2 profile show <name>` to inspect the stored credentials",
]

_ALREADY_EXISTS_HINT = [
    "run `dhis2 profile list` to see existing profiles",
    "or `dhis2 profile remove <name>` first to free the name",
]


def run_app(app: typer.Typer) -> NoReturn:
    """Invoke a Typer app with clean error rendering for known exceptions."""
    try:
        app()
    except NoProfileError as exc:
        _render("error", str(exc), _NO_PROFILE_HINT)
    except UnknownProfileError as exc:
        _render("error", str(exc), _UNKNOWN_PROFILE_HINT)
    except InvalidProfileNameError as exc:
        _render("error", str(exc), _INVALID_NAME_HINT)
    except ProfileAlreadyExistsError as exc:
        _render("error", str(exc), _ALREADY_EXISTS_HINT)
    except AuthenticationError as exc:
        _render("auth error", str(exc), _AUTH_HINT)
    except Dhis2ApiError as exc:
        _render_api_error(exc)
    except Dhis2ClientError as exc:
        _render("DHIS2 error", str(exc))
    sys.exit(0)


def _render_api_error(exc: Dhis2ApiError) -> NoReturn:
    """Render a Dhis2ApiError — extract the WebMessage envelope when DHIS2 ships one."""
    envelope = exc.web_message
    detail = exc.message or ""
    body_msg = envelope.message if envelope and envelope.message else _extract_body_message(exc.body)
    if body_msg:
        detail = f"{detail}: {body_msg}" if detail else body_msg
    extras = _webmessage_detail_lines(envelope) if envelope else []
    _render(f"DHIS2 API error ({exc.status_code})", detail or "(no further detail)", extras=extras)


def _webmessage_detail_lines(envelope: WebMessageResponse) -> list[str]:
    """Format the useful bits of a WebMessageResponse for end-user output.

    Covers import-count summary, per-row conflicts (with errorCode when set),
    and the list of rejected payload indexes — everything DHIS2 tucks under
    `response.*` on a /api/dataValueSets or /api/tracker rejection.
    """
    lines: list[str] = []
    counts = envelope.import_count()
    if counts is not None and any((counts.imported, counts.updated, counts.ignored, counts.deleted)):
        lines.append(
            f"import_count: imported={counts.imported} updated={counts.updated} "
            f"ignored={counts.ignored} deleted={counts.deleted}"
        )
    conflicts = envelope.conflicts()
    if conflicts:
        lines.append(f"{len(conflicts)} conflict{'s' if len(conflicts) != 1 else ''}:")
        for conflict in conflicts:
            target = conflict.property or conflict.object or "?"
            message = conflict.value or "(no detail)"
            code = f" [{conflict.errorCode}]" if conflict.errorCode else ""
            lines.append(f"  - {target}: {message}{code}")
    rejected = envelope.rejected_indexes()
    if rejected:
        lines.append(f"rejected_indexes: {rejected}")
    return lines


def _render(label: str, message: str, hint: list[str] | None = None, extras: list[str] | None = None) -> NoReturn:
    """Print `label: message` + optional extras + optional hint block to stderr and exit 1."""
    typer.secho(f"{label}: {message}", err=True, fg=typer.colors.RED)
    if extras:
        for line in extras:
            typer.echo(line, err=True)
    if hint:
        typer.echo("", err=True)
        typer.echo("hint:", err=True)
        for line in hint:
            typer.echo(f"  {line}", err=True)
    sys.exit(1)


def _extract_body_message(body: object) -> str | None:
    """Pull a useful error message out of the DHIS2 JSON body, if present."""
    if isinstance(body, dict):
        message = body.get("message")
        if isinstance(message, str) and message:
            return message
    return None
