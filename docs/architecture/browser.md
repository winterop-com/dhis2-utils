# dhis2-browser — Playwright helpers for DHIS2 UI automation

A separate workspace member so API-only callers of `dhis2-client` never pull
in Chromium. Today ships a login helper + PAT minting; the package is set up
to grow into the first real home for workflows that DHIS2 only exposes
through its web UI.

## Surfaces

| Layer | Entry point | Where |
| --- | --- | --- |
| Library | `dhis2_browser.logged_in_page` | `packages/dhis2-browser/src/dhis2_browser/session.py` |
| Library | `dhis2_browser.create_pat` | `packages/dhis2-browser/src/dhis2_browser/pat.py` |
| CLI | `dhis2 browser pat` | `packages/dhis2-core/src/dhis2_core/plugins/browser/cli.py` |

The browser plugin mounts under the main `dhis2` CLI alongside every other
plugin (`files`, `messaging`, `metadata`, …) — there's no separate
`dhis2-browser` binary. Chromium stays optional: users who install
`dhis2-cli` (or `dhis2-mcp`) without the `[browser]` extra never pull
Playwright. `service.require_browser()` checks for the library at call
time and raises a clear install hint if it's missing.

## Layering

The split between `dhis2-core`'s `browser` plugin and the `dhis2-browser`
library follows the same pattern every plugin uses:

```
user runs:    dhis2 browser pat ...
              │
              ▼
dhis2-cli:    main.py → discovers plugins → mounts them
              │
              ▼
dhis2-core:   plugins/browser/cli.py  (Typer sub-app for `dhis2 browser ...`)
              │
              ▼
dhis2-core:   plugins/browser/service.py  (guarded wrapper + install hint)
              │
              ▼
dhis2-browser: create_pat / logged_in_page  (actual Playwright work)
```

Keeping `dhis2-browser` as a separate workspace member stops the Chromium
dependency chain from leaking into `dhis2-client`. The plugin in
`dhis2-core` stays tiny — it's a thin Typer facade over the library's
typed entry points.

## Why PAT minting goes through the UI

DHIS2 gates `POST /api/apiToken` behind a logged-in session cookie. An
`Authorization: Basic ...` header on that endpoint returns 401 / redirects
to the login form. The V2 token value (`d2p_...`) is only returned **once**
at creation — there is no "show me the token again" endpoint. So the only
way to get a PAT programmatically from outside the DHIS2 UI is:

1. Drive the React login form at `/dhis-web-login/` with a real browser.
2. Let DHIS2 set the `JSESSIONID` cookie.
3. Call `POST /api/apiToken` inside that session via `page.request.post(...)`.
4. Read the token value from the response body.
5. Store it — it is gone from the server after this.

`create_pat` wraps all five steps. The response-shape parser tolerates
slight variation across DHIS2 versions (some builds return the token at
`response.key`, some at `token`, some at `key` top-level).

## Headless vs headful

`session.resolve_headless()` is the single source of truth. Precedence:

1. Explicit `headless=True | False` kwarg wins.
2. `DHIS2_HEADFUL=1` env var → visible.
3. Default → headless.

Library entry points (`logged_in_page`, `create_pat`) are headless by
default; tests and automation benefit from that. The `dhis2 browser pat`
CLI command flips the default to **headful** so first-time users can watch
the login; pass `--headless` to flip.

Decision recorded in `docs/decisions.md` 2026-04-17.

## Test coverage

One `@pytest.mark.slow` integration test at
`packages/dhis2-browser/tests/test_pat.py` runs the full `create_pat`
pipeline against the live seeded stack and verifies the minted token
authenticates on `/api/me` via `PatAuth`. Not in `make test` (Playwright +
live DHIS2 are out of scope for the fast suite); runs in `make test-slow`
nightly alongside the other `--watch` integration tests.

## Roadmap

See `docs/roadmap.md` — **Strategic options → 4. `dhis2-browser` expansion**.
Three concrete next bricks:

1. Wire the existing `create_pat` into `dhis2 init` so first-time setup can
   choose "mint a PAT for me" and the browser flow runs automatically.
2. A profile-aware `authenticated_session(profile)` helper that dispatches
   by auth type — Basic drives the login form, PAT prompts for the
   password (PATs are stateless in DHIS2 and don't create sessions), OIDC
   exchanges the access token for a `JSESSIONID` via Bearer auth on
   `/api/me`. Prerequisite for every later multi-step workflow.
3. `dhis2-browser dashboard screenshot` — full-page capture of every
   DHIS2 dashboard, with lazy-load triggering, render-completion probes,
   chrome hiding, banner annotation, background trimming.
