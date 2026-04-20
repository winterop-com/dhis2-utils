# dhis2-browser — Playwright helpers for DHIS2 UI automation

A separate workspace member so API-only callers of `dhis2-client` never pull
in Chromium. Today ships a login helper + PAT minting; the package is set up
to grow into the first real home for workflows that DHIS2 only exposes
through its web UI.

## Surfaces

| Layer | Entry point | Where |
| --- | --- | --- |
| Library (low-level) | `dhis2_browser.logged_in_page` | `packages/dhis2-browser/src/dhis2_browser/session.py` |
| Library (low-level) | `dhis2_browser.session_from_cookie` | `packages/dhis2-browser/src/dhis2_browser/session.py` |
| Library (low-level) | `dhis2_browser.create_pat` | `packages/dhis2-browser/src/dhis2_browser/pat.py` |
| Service (profile-aware) | `dhis2_core.plugins.browser.service.authenticated_session` | `packages/dhis2-core/src/dhis2_core/plugins/browser/service.py` |
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

## Auth + session cookies — what works for browser workflows

DHIS2's web apps (dashboard, data entry, capture, maintenance) are React
SPAs that authenticate via a `JSESSIONID` cookie. An `Authorization: ApiToken`
header doesn't mint a session — PATs are deliberately stateless, so they
work for one-shot API calls but **cannot** drive the browser. Any workflow
that navigates into a DHIS2 app needs a session cookie first.

Three ways to get one, each matching a profile auth type:

| Profile auth | API calls | Browser session available via |
| --- | --- | --- |
| **Basic** (username + password) | Yes | Either (a) drive the React login form, or (b) one `GET /api/me` with `Authorization: Basic ...` — DHIS2 mints a `JSESSIONID` in the response `Set-Cookie` and we inject it into `BrowserContext.add_cookies(...)`. Path (b) is faster + fully headless + doesn't depend on login-form selectors. |
| **PAT** | Yes | **Not supported for browser workflows.** PATs don't mint sessions. A browser flow on a PAT profile has to fall back to prompting for a password; the profile itself can't drive it. |
| **OAuth2 / OIDC** | Yes | Probably path (b) with `Authorization: Bearer <access_token>` — DHIS2 should mint a session the same way it does for Basic, but this is unverified as of today; track in BUGS.md if it doesn't. |

Both paths are implemented:

- `dhis2_browser.logged_in_page(url, user, pass)` — path (a), drives the
  React login form. Use when path (b) isn't available (e.g. Basic API
  auth disabled server-side).
- `dhis2_browser.session_from_cookie(url, jsessionid)` — path (b)'s
  browser half, given a pre-minted cookie. Fast + fully headless.

The profile-aware wrapper `dhis2_core.plugins.browser.service.authenticated_session(profile)`
dispatches on auth type: Basic → hit `GET /api/me` with `BasicAuth(...)`,
grab the `Set-Cookie: JSESSIONID`, call `session_from_cookie`. OIDC
raises `NotImplementedError` for now (needs a Bearer-to-session smoke
test). PAT profiles raise `BrowserWorkflowNotSupported` with a message
pointing users at a Basic profile.

## `dhis2 browser pat` vs `dhis2 dev pat create`

Both commands mint a DHIS2 Personal Access Token V2 by hitting
`POST /api/apiToken`. They differ in how they authenticate:

| Command | Auth mechanism | When to use |
| --- | --- | --- |
| `dhis2 dev pat create` | Admin auth (Basic or PAT) via the plain API | **Default.** No Playwright, no Chromium, one HTTP call. Fast. |
| `dhis2 browser pat` | Drive the React login form, hit `POST /api/apiToken` inside the resulting browser session | Only when Basic API auth is disabled on the instance, or when you're already in a browser flow and don't want a second trip through the API |

For the common case ("I have admin credentials and I want a PAT"),
`dhis2 dev pat create` is simpler + faster. `dhis2 browser pat` remains the
canonical workflow for the edge cases.

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
The current near-term list is empty: every browser workflow I'd have
called out next turned out to have a REST API already (App Hub
install, maintenance-app "regenerate analytics," PAT creation). What
stays genuinely UI-only: dashboard creation / layout editing,
org-unit-tree drag-drop, and a few maintenance-app actions without
REST analogues. Deferred to long-term / exploratory until a concrete
need appears.
