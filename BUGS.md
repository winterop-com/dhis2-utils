# Upstream DHIS2 quirks

Running list of DHIS2 behaviours that look like bugs or design surprises, found
while building + testing this workspace against a live v42 stack. Each entry is
written so a DHIS2 maintainer can paste the repro and decide whether to fix,
document, or close as working-as-intended.

**How to use this file:**
- When you hit DHIS2 behaviour that surprises you, add an entry. Don't
  pre-filter — it's cheaper to record and later mark as WAI than to rediscover.
- Each entry has: Observed on, Repro (copy-pasteable), Expected, Actual,
  Impact, Workaround in this repo, and (where known) a pointer at the DHIS2
  source-level symptom (class / error code / config key).

---

## 1. `/api/analytics/rawData` and `/api/analytics/dataValueSet` require the `.json` URL suffix

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, build revision `eaf4b70`, build time `2026-01-30`).

**Repro (against any v42 instance):**

```bash
# Parent resource — content negotiation works, extension not required:
curl -s -u admin:district -H 'Accept: application/json' \
  'http://localhost:8080/api/analytics?dimension=dx:DEancVisit1&dimension=pe:LAST_12_MONTHS&dimension=ou:NORNorway01' \
  -o /dev/null -w '%{http_code}  %{content_type}\n'
# 200  application/json;charset=UTF-8

# Sub-resource rawData — Accept header ignored:
curl -s -u admin:district -H 'Accept: application/json' \
  'http://localhost:8080/api/analytics/rawData?dimension=dx:DEancVisit1&dimension=pe:LAST_12_MONTHS&dimension=ou:NORNorway01' \
  -o /dev/null -w '%{http_code}  %{content_type}\n'
# 404  text/html;charset=utf-8     <-- Tomcat "no static resource" page

# Add .json and it works:
curl -s -u admin:district \
  'http://localhost:8080/api/analytics/rawData.json?dimension=dx:DEancVisit1&dimension=pe:LAST_12_MONTHS&dimension=ou:NORNorway01' \
  -o /dev/null -w '%{http_code}  %{content_type}\n'
# 200  application/json;charset=UTF-8

# Same on dataValueSet:
curl -s -u admin:district -H 'Accept: application/json' \
  'http://localhost:8080/api/analytics/dataValueSet?dimension=dx:...' \
  -o /dev/null -w '%{http_code}\n'
# 404
```

**Expected:** Accept-based content negotiation on every `/api/analytics/*`
sub-resource, matching the parent endpoint. Alternatively, if the explicit
extension is intentional, the mapping should at least 406 with a clear
message — not 404 — so callers know the route exists but the representation
doesn't.

**Actual:** Silent 404 that looks like "endpoint doesn't exist", when really
it's "endpoint exists but MVC mapping only accepts extension-suffixed paths".
Almost certainly a `@RequestMapping` / `ResourceHandler` mismatch in DHIS2's
`AnalyticsController` — the sub-path mappings appear to be registered with
`.json` / `.xml` only, whereas `/api/analytics` has a catch-all registered
that does content negotiation.

**Impact:** Any HTTP client doing the standards-compliant thing (send
`Accept: application/json`, no URL extension) silently fails. Painful to
debug because the error body is Tomcat's 404 page, not a JSON error from
DHIS2.

**Workaround in this repo:** Hardcode `.json` in the service-layer URLs —
`packages/dhis2-core/src/dhis2_core/plugins/analytics/service.py:113,139`.
Revisit and remove when DHIS2 fixes the mapping.

**How to know it's fixed:** the first `curl` above (with `Accept:
application/json`, no extension) returns `200 application/json`.

---

## 2. `importStrategy=DELETE` on `/api/dataValueSets` is a soft-delete that still blocks parent metadata deletion

**Observed on:** DHIS2 `2.42.4`.

**Repro:**

```bash
# Setup — create a DE, an OU (under a writable parent), a DS that links them.
# ... (see examples/client/09_bootstrap.py for the full setup). Let:
DE=H0HdkBJ0EYy
OU=Q0WlKDIgZ34
DS=FvsZyFz8cbq

# Write a data value:
curl -s -u admin:district -X POST http://localhost:8080/api/dataValueSets \
  -H 'Content-Type: application/json' \
  -d "{\"dataValues\":[{\"dataElement\":\"$DE\",\"period\":\"202603\",\"orgUnit\":\"$OU\",\"value\":\"42\"}]}"
# -> importCount {"imported": 1, ...}

# "Delete" the data value via importStrategy=DELETE:
curl -s -u admin:district -X POST \
  "http://localhost:8080/api/dataValueSets?importStrategy=DELETE" \
  -H 'Content-Type: application/json' \
  -d "{\"dataValues\":[{\"dataElement\":\"$DE\",\"period\":\"202603\",\"orgUnit\":\"$OU\",\"value\":\"42\"}]}"
# -> importCount {"deleted": 1, ...}

# The row is still there — just flagged deleted=true:
curl -s -u admin:district \
  "http://localhost:8080/api/dataValueSets.json?dataElement=$DE&orgUnit=$OU&period=202603&includeDeleted=true"
# -> {"dataValues":[{"dataElement":"...","period":"202603","orgUnit":"...","value":"42",
#                   "storedBy":"admin","deleted":true}]}

# Now try to delete the DE that the (soft-deleted) row references:
curl -s -u admin:district -X DELETE http://localhost:8080/api/dataElements/$DE
# -> 409 Conflict
# -> errorCode E4030
# -> "Object could not be deleted because it is associated with another object: DataValue"
```

**Expected:** After an explicit `importStrategy=DELETE`, referenced parent
metadata (DE, OU) should be deletable — either because (a) `DELETE` means
hard-delete when audits/changelogs are off, or (b) DHIS2 ignores
`deleted=true` rows when computing E4030 reference checks on metadata
deletion. The current behaviour is surprising to anyone who expects
`DELETE` semantics.

**Actual:** Data value persists forever at DB level (row is never removed,
only flagged). Parent metadata becomes permanently undeletable through the
API. The only recovery is direct SQL (`DELETE FROM datavalue WHERE
dataelementid = ...`) which bypasses DHIS2 entirely.

**Impact:**
- Every automated test harness that writes + tears down metadata leaks
  orphan DE/OU rows on the server, cluttering subsequent test runs unless
  the caller mints fresh UIDs every time.
- There is no API-driven way to fully tear down a dataset pipeline. Dev
  cycles (the whole point of a "zero-to-data" bootstrap example) require
  either DB access or a full stack reset.

**Workaround in this repo:** `examples/client/09_bootstrap.py` executes the
soft-delete + DS delete, then documents that DE + OU are left behind, with
a pointer here. Rerunning the bootstrap mints fresh UIDs so no collision.

**Relevant DHIS2 source-side pointer:** error code `E4030` is raised by
`org.hisp.dhis.dbms.DbmsManager` (or similar); the reference-check almost
certainly uses a `SELECT 1 FROM datavalue WHERE ...` without a `deleted =
false` predicate. That missing predicate is probably a one-line fix.

**How to know it's fixed:** After the curl repro above, `DELETE
/api/dataElements/$DE` returns `200 OK` (or at least something other than
`E4030: associated with another object: DataValue`).

---

## 3. Blank `audit.metadata` / `audit.tracker` / `audit.aggregate` in `dhis.conf` silently fall back to audit-enabled defaults

**Observed on:** DHIS2 `2.42.4`.

**Repro:**

1. Put the following in `dhis.conf` (blank right-hand side):
   ```properties
   audit.metadata =
   audit.tracker =
   audit.aggregate =
   ```
2. Restart DHIS2.
3. Write a data value via `/api/dataValueSets`, then try to delete the
   referenced `DataElement`:
   ```
   DELETE /api/dataElements/<DE>
   -> 409  errorCode E4030
   -> "Object could not be deleted because it is associated with another object: DataValueAudit"
   ```
   A `DataValueAudit` row was written, even though the caller had blanked
   out every `audit.*` key.

4. Now change `dhis.conf` to explicit sentinel values and restart:
   ```properties
   audit.metadata = DISABLED
   audit.tracker = DISABLED
   audit.aggregate = DISABLED
   ```
5. Repeat step 3. The 409 now refers to `DataValue` (not `DataValueAudit`)
   — i.e. the audit writer is genuinely off.

**Expected:** Blank keys in `dhis.conf` either (a) mean "empty audit scope
= log nothing", which is the intuitive reading, or (b) cause DHIS2 to
refuse to start with a clear error ("audit.metadata is set but empty;
valid values are ..."). Silently falling back to a code-default that
enables audits is the worst of both worlds — the operator *thought* they
had turned auditing off.

**Actual:** Blank RHS is parsed as "use the code default", which for
`AuditMatrix` is `CREATE;UPDATE;DELETE`. No log message indicates the
fallback happened.

**Impact:** Anyone disabling DHIS2 auditing for a dev stack (to work
around bug #2 above, for instance) has to know that `key =` is not
equivalent to `key = <empty scope>`. This is not documented in the
`dhis.conf` template shipped with DHIS2.

**Workaround in this repo:** `infra/home/dhis.conf` uses explicit
`audit.metadata = DISABLED` (and the matching tracker + aggregate keys).
The file has a comment pointing at this entry.

**Relevant DHIS2 source-side pointer:** `org.hisp.dhis.audit.AuditMatrix`
parses the semicolon-separated scope list. Suggested fix: treat an empty
string as "no scopes" instead of delegating to the class-level default.

**How to know it's fixed:** Step 3 of the repro — after restart with blank
keys — DE deletion does NOT 409 with `associated with another object:
DataValueAudit`.

---

## 4. DHIS2 OAuth2 Authorization Server requires 10+ undocumented `dhis.conf` keys all set together, or authorize/token silently degrade

**Observed on:** DHIS2 `2.42.4` (but the config surface is the same on 2.40–2.43).

**Repro:**

Start with a `dhis.conf` that has only the minimum documented OAuth2 key:

```properties
oauth2.server.enabled = on
```

Behaviour:

```bash
# AS endpoints 404 or 500 randomly:
curl -sI 'http://localhost:8080/oauth2/authorize?response_type=code&client_id=foo&redirect_uri=http://localhost:8765&scope=openid+email&state=x&code_challenge=y&code_challenge_method=S256'
# -> 500 "No AuthenticationProvider found for UsernamePasswordAuthenticationToken"

# Minting a token works...
curl -s -u foo:bar -X POST http://localhost:8080/oauth2/token -d 'grant_type=authorization_code&...'

# ...but the token is rejected on /api/*:
curl -H 'Authorization: Bearer <minted-token>' http://localhost:8080/api/me
# -> 401 with "Invalid issuer" buried in logs
```

You have to add ALL of the following to get a working flow:

```properties
# 1. Mount the AS:
oauth2.server.enabled = on
# 2. Set the issuer URL that lands in JWT `iss` claims:
server.base.url = http://localhost:8080
# 3. Tell the API-side JWT filter to accept Bearer tokens:
oidc.jwt.token.authentication.enabled = on
# 4. Wire the login form as the AS user-auth front-end:
oidc.oauth2.login.enabled = on
# 5. Register the AS as a generic OIDC provider so the API-side validator
#    can resolve the issuer. 10 keys, all required, NO defaults:
oidc.provider.dhis2.client_id         = ...
oidc.provider.dhis2.client_secret     = ...
oidc.provider.dhis2.issuer_uri        = ...
oidc.provider.dhis2.authorization_uri = ...
oidc.provider.dhis2.token_uri         = ...
oidc.provider.dhis2.jwk_uri           = ...
oidc.provider.dhis2.user_info_uri     = ...
oidc.provider.dhis2.redirect_url      = ...
oidc.provider.dhis2.scopes            = ...
oidc.provider.dhis2.mapping_claim     = ...
```

Omit any of those 10 `oidc.provider.dhis2.*` keys and the generic provider
parser falls back silently — not to a discovery from `issuer_uri` (which
would be reasonable) but to "no provider registered", so minted tokens 401
on the API.

**Expected:**
- `oauth2.server.enabled = on` should be enough to get a working
  self-contained AS + API-side validation loop.
- Or, the `oidc.provider.dhis2.*` keys should auto-derive from
  `issuer_uri` via OIDC discovery (`.well-known/openid-configuration`),
  which is standard.
- Or, at minimum, DHIS2 should log at `WARN` on startup when
  `oauth2.server.enabled = on` but the paired keys are missing, listing
  which ones it needs.

**Actual:** Silent misconfigurations. Errors surface much later (random
500s, 401s with "Invalid issuer" buried in Tomcat logs) rather than at
config-load time.

**Impact:** Every first-time setup of the embedded AS costs hours. The
official docs list the flag but do not enumerate the full set of paired
keys needed for a functional loop.

**Workaround in this repo:** `infra/home/dhis.conf` lists all 14 keys in
one labelled block with a one-line "why this exists" comment per key. See
`packages/dhis2-core/src/dhis2_core/oauth2_preflight.py` for a startup
check that verifies the server actually exposes the AS endpoints before
we try to drive a flow — gives a clean error message when the operator
has forgotten a key.

**Relevant DHIS2 source-side pointer:**
`org.hisp.dhis.security.config.AuthorizationServerEnabledCondition`
guards the AS. The generic OIDC provider is parsed by
`GenericOidcProviderConfigParser` — that's where
`.well-known/openid-configuration` auto-discovery should happen but
currently does not.

**How to know it's fixed:** A DHIS2 `dhis.conf` with only
`oauth2.server.enabled = on` + `server.base.url = <url>` yields a
working authorize/token/API loop, or startup logs list every missing
paired key with one line each.

---

## 4a. OAuth2 `/oauth2/*` endpoints 301-redirect to trailing-slash variants; standard HTTP clients silently drop Authorization on the redirect

**Observed on:** DHIS2 `2.42.4`, same behaviour on 2.40+.

**Repro:**

```bash
# Without trailing slash — DHIS2 301s to the slashed variant:
curl -si -u client:secret -X POST http://localhost:8080/oauth2/token \
  -d 'grant_type=refresh_token&refresh_token=bogus' | head -5
# HTTP/1.1 301 Moved Permanently
# Location: /oauth2/token/
# ...

# With trailing slash — the AS actually responds:
curl -si -u client:secret -X POST http://localhost:8080/oauth2/token/ \
  -d 'grant_type=refresh_token&refresh_token=bogus' | head -5
# HTTP/1.1 400 Bad Request
# Content-Type: application/json
# ...
```

**Expected:** DHIS2 should not 301 on these endpoints — OAuth2 specs (RFC
6749, RFC 7636) use the no-slash form universally. Clients wrote against
the spec and then fail here.

**Actual:** 301 to `/oauth2/token/` and `/oauth2/authorize/`. Two
problems follow:
1. `httpx` (and Python `requests`) don't follow redirects by default.
   Library consumers get a 301 response + body, which they mis-interpret
   as "token endpoint returned something weird".
2. Even with `follow_redirects=True`, any client following a 301
   cross-origin (localhost → localhost is same-origin so this one is
   fine, but reverse-proxied deployments behind CDNs with URL rewriting
   lose the Authorization header per RFC 7231 §6.4.4).

**Impact:** Every OAuth2 library integration has to explicitly enable
redirect following *and* be certain the redirect is same-origin. Third-
party client libraries (mobile apps, enterprise OAuth2 frameworks) will
fail in subtle ways until the integrator notices the 301.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/auth/oauth2.py` creates its
`httpx.AsyncClient` with `follow_redirects=True` specifically for
`_exchange_code` and `_refresh`. A comment points at this entry.

**How to know it's fixed:** The first `curl` above returns 400 (or
whatever the AS error is for a bogus refresh token) without the
intermediate 301.

---

## 4b. `/oauth2/token` on a misconfigured stack returns DHIS2's generic 401 instead of the Spring-AS error JSON

**Observed on:** DHIS2 `2.42.4`.

**Repro:**

Start DHIS2 with `oauth2.server.enabled = off` (the default), then hit
the token endpoint:

```bash
curl -si -u client:secret -X POST http://localhost:8080/oauth2/token \
  -d 'grant_type=refresh_token&refresh_token=bogus'
# HTTP/1.1 401 Unauthorized
# WWW-Authenticate: Basic realm="..."
# Content-Type: text/html
# ...  <-- DHIS2's generic unauth HTML page
```

The same call against a correctly-configured AS returns the Spring
`OAuth2Error` JSON:

```json
{"error":"invalid_grant","error_description":"..."}
```

**Expected:** Both states should return a JSON body with an OAuth2 error
code. Specifically: when the AS is off, the endpoint should 404 (route
not mounted), not 401 (route mounted but authentication failed). Right
now the caller can't distinguish "my refresh token expired" from "the
server doesn't actually have an AS running".

**Actual:** 401 HTML. This is the DHIS2 servlet filter chain catching
the request before the Spring Authorization Server's `/oauth2/*`
mappings are evaluated — and since the AS isn't mounted, nothing later
in the chain overrides the response.

**Impact:** Operators debugging an OAuth2 setup spend hours convinced
their credentials are wrong when the real problem is a missing
`oauth2.server.enabled = on` line. The HTML body is particularly
confusing because it looks like a full DHIS2 instance is up (and at
`/api/*` it is) — so why is the token endpoint returning an HTML login
page?

**Workaround in this repo:**
`packages/dhis2-core/src/dhis2_core/oauth2_preflight.py` probes the
`.well-known/openid-configuration` endpoint before we try to drive an
authorize/token flow. If the AS isn't up, we fail fast with a clean
error that points at the missing `dhis.conf` key.

**How to know it's fixed:** The repro above returns a JSON body with
`error` field, even when the AS is off — so callers can distinguish
states programmatically.

---

## 4c. DHIS2's embedded JWT keystore is regenerated on every startup; refresh tokens minted before a restart are permanently dead

**Observed on:** DHIS2 `2.42.4` with `oauth2.server.jwt.keystore.generate-if-missing` at its default (on).

**Repro:**

```bash
# 1. Start DHIS2. Drive an authorize-code flow end-to-end:
# 2. Access token + refresh token get persisted by the caller.
# 3. Restart DHIS2 (e.g. `make dhis2-down && make dhis2-up`).
# 4. Try to use the refresh token:
curl -s -u client:secret -X POST http://localhost:8080/oauth2/token/ \
  -d "grant_type=refresh_token&refresh_token=$SAVED_REFRESH"
# -> 400 {"error":"invalid_grant","error_description":"..."}
```

Every cached refresh token — whether it had expired or not — is dead
after a restart. The newly-generated keystore can't decode signatures
produced by the old one, and tracked `oauth2_authorizations` rows in
the DB point at a dead signing key.

**Expected:** The keystore should be persistent by default (either
written to disk alongside `dhis.conf`, or derivable from a seed). Then
issued tokens should survive a graceful restart, which is the whole
point of having refresh tokens in the first place.

**Actual:** On a stack with no explicit keystore config, every restart
silently invalidates every cached token.

**Impact:**
- Local dev: every `make dhis2-down && make dhis2-up` cycle forces
  re-authentication through every browser-based flow. Our
  `examples/cli/02_profiles.sh` now shows `local_oidc: HTTPStatusError:
  400` after any restart for exactly this reason.
- Prod: any DHIS2 rolling restart (host maintenance, patch deploy)
  terminates every OAuth2 session across every client app integrated
  with it. Mobile apps, dashboards, LLMs-via-MCP — all get logged out.

**Workaround in this repo:** No code workaround; we document the
"rerun `dhis2 profile login`" step for dev. A real fix is infrastructure:
explicit keystore via `oauth2.server.jwt.keystore.*` keys, persisted in
`infra/home/keystore.p12` or similar.

**How to know it's fixed:** After the repro above, the refresh-token
call returns 200 with a fresh access token (assuming the refresh token
itself hasn't expired).

---

## 4d. DHIS2 conflates "OAuth2" and "OIDC" across its config keys, docs, and code paths

**Observed on:** DHIS2 `2.42.4`.

DHIS2 exposes an OAuth 2.1 Authorization Server. That's pure OAuth2 — issue access tokens, validate bearer tokens. Separately DHIS2 can *also* act as an OpenID Connect Provider — additional `id_token` JWT, `/userinfo` endpoint, `.well-known/openid-configuration` discovery.

These are different things and DHIS2 mixes them freely:

| Concern | DHIS2 `dhis.conf` key |
| --- | --- |
| Turn on the Authorization Server (OAuth2) | `oauth2.server.enabled` |
| Accept Bearer tokens at `/api/*` (OAuth2) | `oidc.jwt.token.authentication.enabled` |
| Wire the login form (OAuth2) | `oidc.oauth2.login.enabled` |
| Register a generic OIDC provider (either OAuth2 or OIDC role) | `oidc.provider.<name>.*` |

So a pure OAuth2 setup (no OIDC extras) still requires `oidc.*` keys set. The `oidc.*` prefix implies ID-token semantics that are orthogonal. Users reading the config can't tell which parts are OAuth2 and which are OIDC.

**Impact for us:** We're implementing a pure OAuth2 integration — access tokens, PKCE, refresh tokens. We do NOT parse `id_token`, do NOT hit `/userinfo`, do NOT do discovery. The profile's `auth` kind is `"oauth2"` and the CLI lives under `dhis2 profile login/logout/bootstrap` (protocol-neutral verbs). We deliberately did not call the namespace `oidc` — that would mis-describe what the code does.

**Expectation:** DHIS2 config keys should split cleanly — `oauth2.*` for the Authorization Server, `oidc.*` only for the extra OIDC features. Right now you can't opt into OAuth2 without setting 10+ `oidc.*`-prefixed keys, which makes it look like you're configuring OIDC when you're not.

**How to know it's fixed:** DHIS2 docs for "enable the embedded OAuth2 Authorization Server" give a minimal config block using only `oauth2.*` keys.

---

## 4e. DHIS2 Route API `api-token` auth sends `Authorization: ApiToken <value>` — not the standard `Bearer` scheme

**Observed on:** DHIS2 `2.42.4`.

A route configured with `"auth": {"type": "api-token", "token": "..."}` causes DHIS2 to call the upstream URL with `Authorization: ApiToken <token>` — a DHIS2-specific scheme, not the standard OAuth2 `Authorization: Bearer <token>`.

**Repro:**

```bash
# 1. Create a route pointing at httpbin's header-echo endpoint.
curl -s -u admin:district -X POST http://localhost:8080/api/routes \
  -H 'Content-Type: application/json' \
  -d '{"code":"T","name":"t","url":"https://httpbin.org/headers",
       "auth":{"type":"api-token","token":"observed-value"}}'
# -> "uid": "<route-uid>"

# 2. Run it. httpbin echoes the request headers.
curl -s -u admin:district http://localhost:8080/api/routes/<route-uid>/run
# -> {"headers": {"Authorization": "ApiToken observed-value", ...}}
```

The header value is `ApiToken observed-value`, not `Bearer observed-value`.

**Expected:** The OAuth2 `Bearer` scheme (RFC 6750) is the universal format for API tokens over HTTP. `api-token` should send `Authorization: Bearer <token>` so upstream APIs built against the standard work without per-server customisation. If a DHIS2-specific scheme is genuinely required, the config type name should reflect that (e.g. `"type": "dhis2-api-token"`) rather than the generic `api-token`.

**Actual:** `ApiToken <value>`. Breaks integration with any upstream that expects the standard Bearer scheme (most OAuth2 resource servers, GitHub PATs, Slack bot tokens, httpbin.org/bearer, etc.).

**Impact:**
- Common public APIs reject the upstream call with 401 "invalid_token" or "missing Bearer scheme".
- Integrators can't use off-the-shelf Bearer-auth endpoints without wrapping them in a shim that rewrites the Authorization header.
- Cascading into our tooling: `dhis2 route run` then surfaces the 401 as "auth error at GET /api/routes/.../run", suggesting a DHIS2-side auth problem when the failure is actually on the upstream leg.

**Workaround in this repo:** None. Our `examples/cli/08_routes.sh` targets httpbin.org/headers (which echoes whatever DHIS2 sends) instead of httpbin.org/bearer (which rejects the non-standard scheme).

**How to know it's fixed:** The curl repro above shows `"Authorization": "Bearer observed-value"`.

---

## 4f. DHIS2's WebMessageResponse envelope names the created object's identifier `uid`, not `id`

**Observed on:** DHIS2 `2.42.4`. Consistent across `/api/routes`, `/api/oAuth2Clients`, `/api/apiToken`, `/api/organisationUnits`, `/api/dataElements` — anything that returns an `ObjectReportWebMessageResponse`.

**Repro:**

```bash
# POST creates an object. Response wraps it in a WebMessageResponse:
curl -s -u admin:district -X POST http://localhost:8080/api/routes \
  -H 'Content-Type: application/json' \
  -d '{"code":"T","name":"t","url":"https://httpbin.org/get"}'
# {
#   "httpStatus": "Created", "httpStatusCode": 201, "status": "OK",
#   "response": {
#     "uid": "ujvQ0frIFA6",               <-- uid
#     "klass": "org.hisp.dhis.route.Route",
#     "errorReports": [],
#     "responseType": "ObjectReportWebMessageResponse"
#   }
# }

# GET returns the object directly. The identifier is `id`:
curl -s -u admin:district http://localhost:8080/api/routes/ujvQ0frIFA6
# { "id": "ujvQ0frIFA6", "code": "T", "name": "t", ... }
```

**Expected:** Consistent field name for the object identifier. Either always `id` (matches the object's own model, `/api/schemas/<resource>.id`) or always `uid` — but not both depending on which endpoint you hit. Almost every client ends up with parsing branches like `response.get("response", {}).get("uid") or response.get("id")` to handle both.

**Actual:** POST/PUT/DELETE wrap the identifier as `response.response.uid`. GET returns `id` at the top level. JSON Patch (`PATCH`) returns the full object (so `id`). This is reflected in DHIS2's Java classes: `ObjectReport` has a `uid` field, `BaseIdentifiableObject` has an `id` field, and they're serialised as named.

**Impact:**
- Callers that capture the UID after a POST must reach into `response.response.uid`, not `response.id`.
- Copy/paste between "I created this" and "fetch by UID" paths requires renaming the field.
- Generated pydantic models from `/api/schemas` use `id` (correctly — matches the object shape), but the WebMessageResponse envelope isn't schema-driven so callers have no typed model to work with for writes.

**Workaround in this repo:** Several shell + Python callers use `response.get("response", {}).get("uid") or response.get("id") or ""` as a defensive two-field lookup. See `packages/dhis2-core/src/dhis2_core/plugins/dev/sample.py:sample_route_command` for one example. A single WebMessageResponse pydantic model in `dhis2-client` would let us type this once (follow-up).

**How to know it's fixed:** The POST response above shows `"response": {"id": "..."}` — matching the GET shape.

---

## 4g. DHIS2 accepts whitespace-abusive values for `name`, `shortName`, and `code` on metadata create

**Observed on:** DHIS2 `2.42.4`. Confirmed against `TrackedEntityType` and `DataElement`; pattern appears consistent across metadata types.

**Repro:**

```bash
# Leading/trailing spaces + multiple consecutive spaces in name, shortName, code.
curl -s -u admin:district -X POST http://localhost:8080/api/trackedEntityTypes \
  -H 'Content-Type: application/json' \
  -d '{"name":" space  hello     workd","shortName":"  ugly   ","code":"  CODE  WITH   SPACES  "}'
# -> 201 Created, uid=N00MYHinQ3r

# Read it back — values persisted verbatim:
curl -s -u admin:district http://localhost:8080/api/trackedEntityTypes/N00MYHinQ3r?fields=name,shortName,code
# {
#   "name": " space  hello     workd",
#   "shortName": "  ugly   ",
#   "code": "  CODE  WITH   SPACES  "
# }
```

Same behaviour on `DataElement` (`name`, `shortName`, `code`). No trimming, no collapsing of consecutive whitespace, no validation error.

**Expected:** DHIS2 should either trim + collapse whitespace before persisting (what 99% of real-world use cases want), or reject the input with a `validation_error` pointing at the affected field. `name` / `shortName` are user-facing labels that end up in dropdowns, reports, analytics dimension headers — leading spaces break sort order, extra whitespace breaks equality checks, trailing spaces make dashboards look broken. `code` is even worse: `code` is often used as a stable lookup key, and `"  FOO  "` does NOT match `"FOO"` in a filter `code:eq:FOO`.

**Actual:** Values persist byte-for-byte. Downstream callers end up either doing client-side trimming (fragile — you have to know every place where a user-typed name reaches DHIS2) or writing defensive filters like `code:like:%FOO%` that lose the point of an exact-match lookup.

**Impact:**
- Reports and dropdown menus render junk names with obvious formatting problems.
- Metadata-import scripts that copy-paste values from spreadsheets silently introduce whitespace bugs.
- `dhis2 metadata list <resource> --filter "code:eq:FOO"` fails to find objects whose `code` is actually ` FOO ` in the DB.
- No way to audit whitespace-corrupted values after the fact without a full-table scan + regex.

**Workaround in this repo:** None at the CLI/MCP layer — we pass user input through verbatim. Client-side validation in `dhis2-core` could reject whitespace-abusive values before the POST, but that would diverge from DHIS2's actual constraints (it'd reject inputs DHIS2 itself accepts).

**How to know it's fixed:** The first repro POST either 400s with a validation error OR the read-back shows trimmed + collapsed values ("space hello workd", "ugly", "CODE WITH SPACES").

---

## 5. `organisationUnits` POST inside a user's capture scope enforces DESCENDANT, not sibling-of-scope

**Observed on:** DHIS2 `2.42.4`.

**Repro:**

```bash
# Seeded admin has organisationUnits = [4 fylker under NORNorway01].
# NORNorway01 is the country root; it is NOT in admin's capture scope.

# Create an OU directly under NORNorway01 (= sibling of the 4 fylker):
NEW_OU=$(curl -s -u admin:district 'http://localhost:8080/api/system/id' | python3 -c "import sys,json; print(json.load(sys.stdin)['codes'][0])")
curl -s -u admin:district -X POST http://localhost:8080/api/organisationUnits \
  -H 'Content-Type: application/json' \
  -d "{\"id\":\"$NEW_OU\",\"code\":\"EX_SIB\",\"name\":\"Sibling of scope\",\"shortName\":\"Sib\",
       \"openingDate\":\"2025-01-01\",\"parent\":{\"id\":\"NORNorway01\"}}"
# -> 201 Created — that part's fine.

# Now write a data value at the new OU:
curl -s -u admin:district -X POST http://localhost:8080/api/dataValueSets \
  -H 'Content-Type: application/json' \
  -d "{\"dataValues\":[{\"dataElement\":\"DEancVisit1\",\"period\":\"202603\",\"orgUnit\":\"$NEW_OU\",\"value\":\"42\"}]}"
# -> 409 "Organisation unit: <NEW_OU> not in hierarchy of current user: <admin uid>"
```

**Expected:** The error message says "not in hierarchy", but admin IS
assigned to multiple OUs (the 4 fylker). The check is specifically:
"`NEW_OU` must be a DESCENDANT of at least one of the current user's
`organisationUnits`". The wording misleads — it sounds like admin's scope
is empty.

**Actual:** Silently-strict DESCENDANT check. Admin has to be explicitly
granted the new OU (or an ancestor of it) via
`/api/users/<admin>/organisationUnits` before writes are accepted.

**Impact:** Any bootstrap / onboarding workflow that provisions a new
OU structure hits this. The fix is to PATCH the admin user's
`organisationUnits` to include the new ancestor(s) — but that requires
knowing the semantics.

**Workaround in this repo:** `examples/client/09_bootstrap.py` parents new
OUs under `NOROsloProv` (already in admin's scope via the seeded fixture)
so they inherit descendant-of-scope. The "one-liner" PATCH pattern for
when you must create sibling-of-scope OUs is documented inline as a
comment.

**Expected improvement:** DHIS2's error message should distinguish
"admin's scope is empty" from "OU X is outside admin's capture tree" —
the latter case should suggest the PATCH fix in the error body.

**How to know it's fixed:** Error message on the failing POST above
names the ancestor chain admin would need, or the behaviour is documented
clearly in the `OrganisationUnit` API reference page.

---

## 6. Bulk `/api/dataValueSets` push returns 409 even when every row's `ignored`, hiding the per-row conflict detail

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, build revision `eaf4b70`, build time `2026-01-30`).

**Repro (against the seeded e2e fixture, after `make dhis2-seed`):**

```bash
cat > /tmp/dv.json <<'JSON'
{"dataValues": [{"dataElement":"DEancVisit1","period":"202604","orgUnit":"NOROsloProv","value":"77"}]}
JSON

# Period 202604 lands outside `NORMonthDS1`'s open-future-period window.
curl -s -u admin:district -H 'Content-Type: application/json' \
  -o /tmp/resp.json -w '%{http_code}\n' \
  'http://localhost:8080/api/dataValueSets?dryRun=true&importStrategy=CREATE_AND_UPDATE' \
  --data @/tmp/dv.json
# 409

jq '{httpStatusCode, status, message, importCount: .response.importCount, rejectedIndexes: .response.rejectedIndexes, conflicts: .response.conflicts}' /tmp/resp.json
```

**Expected:** Either a 200 with `status=WARNING` and a populated `conflicts[]` block (so clients can branch on the status code alone), or a 4xx whose body the typical HTTP client still surfaces. Current behaviour mixes them — status is `WARNING` (process completed), `importCount` is non-zero-and-fully-ignored, every row rejected — but the HTTP code is 409, which most clients treat as a hard failure and raise.

**Actual:** The response body carries the full import summary (rich `conflicts[]` with `errorCode`, `property`, `indexes`, a human message per row). But the 409 status makes every `httpx`, `requests`, or hand-rolled client raise before the body is inspected — so the caller sees `409 Conflict: please check import summary` without the import summary.

**Impact:** Users running `dhis2 data aggregate push` against valid-looking data used to see a bare "please check import summary" message; the *actual* rejection reason (e.g. `E7641: Period 202604 is after latest open future period 202603 for data element X and data set Y`) was in the body but never reached them.

**Workaround in this repo:** `Dhis2ApiError.body` always carries the JSON body; `Dhis2ApiError.web_message` lazily parses it into a typed `WebMessageResponse` (see `packages/dhis2-client/src/dhis2_client/errors.py`). The CLI's clean-error renderer (`packages/dhis2-core/src/dhis2_core/cli_errors.py::_render_api_error`) extracts `importCount`, `conflicts[]`, and `rejectedIndexes[]` and prints one line per conflict with `errorCode` / `property` / `value`. `dhis2 data aggregate push` against a rejected row now surfaces the actual E7641-level reason.

**Expected improvement:** `/api/dataValueSets` returns 200 when `status=WARNING` (process completed, some rows rejected) and reserves 4xx for process failures. OR: the DHIS2 error-body convention is documented so client libraries know to parse the body on 409 rather than raise.

**How to know it's fixed:** Either the status code changes, or the body-on-4xx convention lands in the API reference — and `dhis2-client`'s `get_raw`/`post_raw` gains the matching parse-on-4xx branch.
