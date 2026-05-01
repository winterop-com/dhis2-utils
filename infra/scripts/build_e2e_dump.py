"""Build the committed e2e DHIS2 dump from the Sierra Leone immunization snapshot.

Usage (from repo root): `make dhis2-build-e2e-dump` — brings up an empty
DHIS2, loads the typed metadata / geometry / data-value / tracker fixtures
under `infra/fixtures/play/` via the client's pydantic validators, triggers
analytics, seeds OAuth2 + admin openId mapping + login-page branding, and
pg_dump's the result into `infra/dhis-v{DHIS2_VERSION}.sql.gz`.

The actual metadata + data is pulled once from play.dhis2.org (Sierra
Leone) by `infra/scripts/pull_play_fixtures.py` and committed to
`infra/fixtures/play/`. This script only imports those fixtures —
`make dhis2-build-e2e-dump` is fully offline after the fixtures land on
disk. Re-run the puller to refresh against play drift.

Produces a gzipped dump small enough to commit next to the compose file,
so `make dhis2-up` on a fresh clone gives a ready-to-login DHIS2 with
1332 org units, 188 k aggregate values, 500 tracker entities, 3
immunization dashboards, 23 visualizations, 8 maps, and every piece of
metadata transitively wired through them.
"""

from __future__ import annotations

import argparse
import asyncio
import gzip
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _seed_login_customization import apply_login_customization  # noqa: E402
from dhis2_client.auth.basic import BasicAuth  # noqa: E402
from dhis2_client.client import Dhis2Client  # noqa: E402
from seed import seed_play  # noqa: E402
from seed_auth import ensure_user_openid_mapping, upsert_oauth2_client, wait_for_ready  # noqa: E402

POSTGRES_CONTAINER_DEFAULT = "dhis2-docker-postgresql-1"


def default_dump_path(dhis2_version: str) -> Path:
    """Return the canonical committed-dump path for a given DHIS2 major."""
    return Path(__file__).resolve().parents[1] / f"dhis-v{dhis2_version}.sql.gz"


def run_analytics(analytics_container: str = "analytics-trigger") -> None:
    """Trigger analytics by restarting the `analytics-trigger` sidecar + waiting for exit."""
    print(f"    restarting {analytics_container} to populate analytics tables")
    subprocess.run(["docker", "restart", analytics_container], check=True, capture_output=True)
    print("    waiting for analytics task to finish (docker wait)...")
    result = subprocess.run(
        ["docker", "wait", analytics_container],
        check=True,
        capture_output=True,
        text=True,
    )
    exit_code = int(result.stdout.strip() or "1")
    if exit_code != 0:
        logs = subprocess.run(
            ["docker", "logs", "--tail", "50", analytics_container],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
        raise RuntimeError(f"analytics-trigger exited with {exit_code}:\n{logs}")
    print("    analytics tables populated")


def pg_dump(container: str, output: Path, *, postgres_user: str, postgres_db: str) -> None:
    """Run `pg_dump | gzip` via `docker exec` and write the result to `output`."""
    print(f">>> Dumping database to {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "docker",
        "exec",
        container,
        "pg_dump",
        "--no-owner",
        "--no-privileges",
        "--no-sync",
        "--clean",
        "--if-exists",
        "--exclude-table=analytics_*",
        "--exclude-table=aggregated_*",
        "--exclude-table=completeness_*",
        "--exclude-table=_*",
        "-U",
        postgres_user,
        "-d",
        postgres_db,
    ]
    with output.open("wb") as gz_handle, gzip.GzipFile(fileobj=gz_handle, mode="wb", compresslevel=9) as gz:
        proc = subprocess.run(cmd, check=True, capture_output=True)
        gz.write(proc.stdout)
    size = output.stat().st_size
    print(f">>> Wrote {size:,} bytes to {output}")


def detect_postgres_container(default: str) -> str:
    """Return the running postgres container name, falling back to `default`."""
    if shutil.which("docker") is None:
        raise RuntimeError("`docker` CLI not found — need it for pg_dump")
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        check=True,
    )
    names = [line.strip() for line in result.stdout.splitlines()]
    candidates = [n for n in names if "postgres" in n.lower()]
    if default in names:
        return default
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        print(f"!!! multiple postgres containers found: {candidates}; defaulting to {candidates[0]}")
        return candidates[0]
    raise RuntimeError(f"no running postgres container detected; expected {default!r}")


async def build(url: str, username: str, password: str, output: Path, container: str) -> None:
    """End-to-end: seed Sierra Leone fixtures + auth + branding → pg_dump."""
    print(f">>> Waiting for DHIS2 at {url}")
    await wait_for_ready(url, username, password)
    async with Dhis2Client(url, BasicAuth(username=username, password=password)) as client:
        info = await client.system.info()
        print(f">>> Connected to DHIS2 {info.version} as {username}")

        print(">>> Seeding Sierra Leone immunization fixture (infra/fixtures/play/)")
        await seed_play(client)

        print(">>> Running analytics")
        run_analytics()

        print(">>> Seeding OAuth2 client + admin openId mapping")
        await upsert_oauth2_client(client)
        await ensure_user_openid_mapping(client, username)

        print(">>> Applying login-page branding preset")
        await apply_login_customization(client)

    pg_dump(container, output, postgres_user="dhis", postgres_db="dhis")


def main() -> int:
    """Parse args and run the build."""
    default_version = os.environ.get("DHIS2_VERSION", "42")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8080")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", default="district")
    parser.add_argument(
        "--dhis2-version",
        default=default_version,
        help="DHIS2 major version used to name the dump (default: env DHIS2_VERSION or '42')",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="where to write the gzipped dump (default: infra/dhis-v{dhis2-version}.sql.gz)",
    )
    parser.add_argument(
        "--container",
        default=POSTGRES_CONTAINER_DEFAULT,
        help="name of the running postgres container (auto-detected if not found)",
    )
    args = parser.parse_args()

    output_path = Path(args.output).resolve() if args.output else default_dump_path(args.dhis2_version)
    container = detect_postgres_container(args.container)

    try:
        asyncio.run(build(args.url, args.username, args.password, output_path, container))
    except Exception as exc:  # noqa: BLE001 — top-level runner
        print(f"!!! build failed: {exc}", file=sys.stderr)
        return 1
    print(">>> Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
