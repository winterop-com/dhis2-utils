# Testing strategy

Tests fall into two tiers. Both run through `make test` / `make test-slow`.

## Tier 1: fast unit tests (`make test`)

Use **respx** to mock httpx responses. Cover:

- Every auth provider returns the right headers.
- OAuth2 token caching and refresh paths.
- Dhis2Client parses typed pydantic responses, surfaces error hierarchy correctly.
- `available_versions()` discovers generated modules from the filesystem.
- `Dhis2Client.connect()` version-dispatch logic: strict refusal vs nearest-lower fallback.
- Codegen name/type mapping (pure functions).
- Generated resources' CRUD verbs (GET/POST/PUT/DELETE) hit the right paths with the right HTTP verbs.

Fast — currently runs in <0.5s.

## Tier 2: slow integration tests (`make test-slow`)

Hit the live DHIS2 **play/dev** instance. Read-only by default (no destructive writes against a shared demo server). Cover:

- Raw HTTP auth/discovery round trips with Basic auth.
- Full codegen pipeline: discover → emit → import generated module → inspect.
- Connected client: `client.system.info()`, `client.system.me()`, and `client.resources.data_elements.list()` / `get()` against real data.

Marked with `@pytest.mark.slow` so the default `make test` skips them. They run in ~3s and confirm the full chain works against real DHIS2.

## Test connection details

Defaults:

```
DHIS2_PLAY_URL=https://play.im.dhis2.org/dev
DHIS2_PLAY_USER=system
DHIS2_PLAY_PASS=System123
```

Overridable via environment variables. Tests are parameterised through session-scoped fixtures in each member's `tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def play_url() -> str: ...

@pytest.fixture(scope="session")
def play_username() -> str: ...

@pytest.fixture(scope="session")
def play_password() -> str: ...
```

Simple strings, not dataclasses — this sidesteps mypy's "duplicate conftest module" problem across workspace members.

## Destructive writes

Currently none. Any test that creates or deletes real resources needs to:

- Use a unique, obviously-test name prefix (e.g. `dhis2-utils-test-<uuid>`).
- Clean up in a try/finally.
- Be clearly marked in its docstring.

Until that policy is formalised, CRUD write tests live in the unit tier (respx-mocked) only.

## What we don't test (yet)

- OAuth2 end-to-end against a real DHIS2 instance — requires an OAuth client to be registered on the server. Covered by unit tests (cached token + refresh paths); the interactive browser flow is harder to automate and is skipped.
- Playwright screenshot capture — scoped to `dhis2-browser` tests when that member grows beyond scaffolding.
- Tracker / data values / analytics — modules don't exist yet.
