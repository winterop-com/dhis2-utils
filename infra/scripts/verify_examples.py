"""Run every non-interactive example + summarise PASS / FAIL / TIMEOUT / SKIP.

Targets every script under `examples/{cli,client,mcp}/` (ignoring files that
start with `_`, which are helper modules like `_runner.py`). Each example
runs via `bash <path>` for `.sh` and `uv run python <path>` for `.py`,
inheriting the parent environment plus `DHIS2_PROFILE` so profile-driven
examples pick the right stack.

Known-interactive scripts (OIDC login flows, Playwright browser captures,
external-network ones) are skipped by default because they block on human
input or unreliable dependencies. `--include-browser` opts browser-driven
entries back in.

Usage:
    uv run python infra/scripts/verify_examples.py [--profile NAME] [--timeout SECS]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from rich.console import Console
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Examples that need Chromium (Playwright), a human-clicked OIDC login,
# external network dependencies, or run slow server-side jobs unsuitable
# for a batch pass. Skipped by default; `--include-browser` opts the full
# UI-driven set back in.
SKIP_BY_DEFAULT: frozenset[str] = frozenset(
    {
        # --- UI-driven (opt in via --include-browser) -------------------
        # OIDC: opens a browser tab + runs a local redirect receiver,
        # needs a human to complete the login at the IdP.
        "examples/cli/profile_oidc_login.sh",
        "examples/client/oidc_login.py",
        # Playwright browser workflows: open Chromium, drive UI.
        "examples/cli/dev_pat.sh",
        "examples/cli/map_screenshot.sh",
        "examples/cli/visualization_screenshot.sh",
        "examples/client/oidc_playwright_login.py",
        # --- External network / non-deterministic -----------------------
        # Hits httpbin.org over the public internet.
        "examples/cli/route_register_and_run.sh",
        # --- Slow server-side jobs --------------------------------------
        # Kicks `dhis2 maintenance refresh analytics --watch`; analytics
        # rebuilds legitimately take several minutes on a populated stack.
        "examples/cli/maintenance.sh",
        # --- Fixture gaps in the play42 seed ----------------------------
        # `dev_sample` writes a demo DE + data value through a UID the
        # seed doesn't carry — tied to Norway fixtures (NORMonthDS1).
        "examples/cli/dev_sample.sh",
        # Outlier detection requires per-program data distributions the
        # 1-year Child Programme sample doesn't have enough volume for —
        # the CLI + library wrap the same endpoint, skip both.
        "examples/cli/analytics_outlier_tracked_entities.sh",
        "examples/client/analytics_outlier_tracked_entities.py",
        "examples/mcp/analytics_outlier_tracked_entities.py",
    },
)

DEFAULT_PROFILE = "local_basic"
DEFAULT_TIMEOUT_SECONDS = 180.0


class ExampleResult(BaseModel):
    """One example run's outcome — path + status + wall-clock."""

    model_config = ConfigDict(frozen=True)

    path: str
    surface: str
    status: str  # PASS / FAIL / TIMEOUT / SKIP
    seconds: float
    stderr_tail: str = ""


def discover_examples() -> list[Path]:
    """Return every example file under `examples/{cli,client,mcp}/`, sorted by path."""
    paths: list[Path] = []
    for subdir in ("cli", "client", "mcp"):
        root = REPO_ROOT / "examples" / subdir
        if not root.exists():
            continue
        for entry in sorted(root.iterdir()):
            if entry.name.startswith("_") or entry.name.startswith("."):
                continue
            if entry.suffix in {".sh", ".py"}:
                paths.append(entry)
    return paths


def _run_one(path: Path, *, profile: str, timeout_seconds: float) -> ExampleResult:
    """Invoke one example with the given profile + timeout; capture result."""
    surface = path.parent.name
    rel = path.relative_to(REPO_ROOT).as_posix()
    env = {**os.environ, "DHIS2_PROFILE": profile}
    cmd: list[str] = ["bash", str(path)] if path.suffix == ".sh" else ["uv", "run", "python", str(path)]
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout_seconds,
            env=env,
            cwd=REPO_ROOT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return ExampleResult(path=rel, surface=surface, status="TIMEOUT", seconds=time.monotonic() - start)
    elapsed = time.monotonic() - start
    if proc.returncode == 0:
        return ExampleResult(path=rel, surface=surface, status="PASS", seconds=elapsed)
    stderr = proc.stderr.decode(errors="replace").strip()
    stdout = proc.stdout.decode(errors="replace").strip()
    tail = "\n".join((stderr or stdout).splitlines()[-6:])
    return ExampleResult(path=rel, surface=surface, status="FAIL", seconds=elapsed, stderr_tail=tail)


def run_suite(
    *,
    profile: str = DEFAULT_PROFILE,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    include_browser: bool = False,
    extra_skip: frozenset[str] = frozenset(),
    console: Console | None = None,
) -> list[ExampleResult]:
    """Run every discovered example, stream per-example status lines, return results."""
    skip = SKIP_BY_DEFAULT | extra_skip if not include_browser else extra_skip
    console = console or Console()
    examples = discover_examples()
    console.print(
        f"running [bold]{len(examples)}[/bold] examples "
        f"(profile=[cyan]{profile}[/cyan], timeout={int(timeout_seconds)}s, "
        f"skip-default={'on' if not include_browser else 'off'})",
    )
    results: list[ExampleResult] = []
    for path in examples:
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel in skip:
            result = ExampleResult(path=rel, surface=path.parent.name, status="SKIP", seconds=0.0)
        else:
            result = _run_one(path, profile=profile, timeout_seconds=timeout_seconds)
        badge = {
            "PASS": "green",
            "FAIL": "red",
            "TIMEOUT": "yellow",
            "SKIP": "dim",
        }[result.status]
        console.print(f"  [{badge}]{result.status:8s}[/{badge}] {result.seconds:6.2f}s  {result.path}")
        results.append(result)
    return results


def render_summary(results: list[ExampleResult], *, console: Console | None = None) -> int:
    """Print a per-surface summary table + per-failure tails. Return 0 iff every example passed."""
    console = console or Console()
    by_surface: dict[str, dict[str, int]] = {}
    for result in results:
        counts = by_surface.setdefault(result.surface, {"PASS": 0, "FAIL": 0, "TIMEOUT": 0, "SKIP": 0})
        counts[result.status] += 1
    table = Table(title=f"example verification summary ({len(results)} total)")
    table.add_column("surface", style="cyan")
    table.add_column("pass", justify="right", style="green")
    table.add_column("fail", justify="right", style="red")
    table.add_column("timeout", justify="right", style="yellow")
    table.add_column("skip", justify="right", style="dim")
    totals = {"PASS": 0, "FAIL": 0, "TIMEOUT": 0, "SKIP": 0}
    for surface, counts in sorted(by_surface.items()):
        table.add_row(
            surface,
            str(counts["PASS"]),
            str(counts["FAIL"]),
            str(counts["TIMEOUT"]),
            str(counts["SKIP"]),
        )
        for key in totals:
            totals[key] += counts[key]
    table.add_row(
        "TOTAL",
        str(totals["PASS"]),
        str(totals["FAIL"]),
        str(totals["TIMEOUT"]),
        str(totals["SKIP"]),
        style="bold",
    )
    console.print(table)
    failures = [r for r in results if r.status in {"FAIL", "TIMEOUT"}]
    if failures:
        console.print(f"\n[red bold]{len(failures)} failure(s)[/red bold]:")
        for result in failures:
            console.print(f"  [red]{result.status:8s}[/red] {result.path}")
            if result.stderr_tail:
                for line in result.stderr_tail.splitlines():
                    console.print(f"    [dim]{line}[/dim]")
        return 1
    console.print("[green bold]all green[/green bold]")
    return 0


def main() -> int:
    """CLI entry point — parse args, run suite, emit summary, exit with aggregated status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default=DEFAULT_PROFILE, help="DHIS2_PROFILE to pass through")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Per-example timeout in seconds (default: 180)",
    )
    parser.add_argument(
        "--include-browser",
        action="store_true",
        help="Also run OIDC / Playwright / external-network examples that are skipped by default.",
    )
    args = parser.parse_args()
    console = Console()
    results = run_suite(
        profile=args.profile,
        timeout_seconds=args.timeout,
        include_browser=args.include_browser,
        console=console,
    )
    return render_summary(results, console=console)


if __name__ == "__main__":
    sys.exit(main())
