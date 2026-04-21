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
# ... (see examples/client/bootstrap_zero_to_data.py for the full setup). Let:
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

**Workaround in this repo:** `examples/client/bootstrap_zero_to_data.py` executes the
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
  `examples/cli/profile_list_verify.sh` now shows `local_oidc: HTTPStatusError:
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

**Workaround in this repo:** None. Our `examples/cli/route_register_and_run.sh` targets httpbin.org/headers (which echoes whatever DHIS2 sends) instead of httpbin.org/bearer (which rejects the non-standard scheme).

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

**Workaround in this repo:** `examples/client/bootstrap_zero_to_data.py` parents new
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

---

## 7. DHIS2's OpenAPI names the primary key `uid` while the REST API wire format uses `id`

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, build revision `eaf4b70`, build time `2026-01-30`).

**Repro:** inspect `/api/openapi.json` — every metadata resource schema declares `"properties": {..., "uid": {"type": "string", ...}}` but no `id`. Yet `GET /api/organisationUnits/<uid>` returns `{"id": "<uid>", ...}` and `POST /api/organisationUnits` expects `{"id": "<uid>", ...}`:

```bash
# What the OpenAPI spec says
curl -s http://localhost:8080/api/openapi.json \
  | jq '.components.schemas.OrganisationUnit.properties | keys[] | select(. == "id" or . == "uid")'
# "uid"

# What the actual API returns
curl -s -u admin:district 'http://localhost:8080/api/organisationUnits/NORNorway01?fields=:identifiable' \
  | jq 'keys[] | select(. == "id" or . == "uid")'
# "id"

# What a POST with uid= does: DHIS2 ignores it and DELETE-first-then-409 complains about missing id
curl -s -u admin:district -X POST 'http://localhost:8080/api/organisationUnits' \
  -H 'Content-Type: application/json' \
  -d '{"uid":"abc12345678","name":"Test","shortName":"T","openingDate":"2025-01-01","parent":{"id":"NORNorway01"}}' \
  -o /dev/null -w '%{http_code}\n'
# 409
```

**Expected:** the OpenAPI field name matches the wire format — either `id` everywhere (so generated clients construct `Model(id="...")` and the JSON dump uses `id`), or `uid` everywhere.

**Actual:** generator builds `class OrganisationUnit(BaseModel): uid: str | None = None` from the OpenAPI spec. Callers doing `OrganisationUnit(uid=X).model_dump()` get `{"uid": X, ...}`, which DHIS2 rejects at create time with 409.

**Impact:** every generated client across every language has to work around this.

**Workaround in this repo:** the codegen renames `uid` -> `id` at emit time for every top-level resource schema (`packages/dhis2-codegen/src/dhis2_codegen/emit.py::_fields_for`). Generated models now declare `id: str | None` matching the wire format, so callers write `Model(id="...").model_dump()` and get `{"id": "..."}` — what DHIS2 actually accepts. The OpenAPI/schemas-endpoint divergence stays internal to the generator; library users never see `uid` on resource models.

**Expected improvement:** OpenAPI spec aligned with wire format — `id` in both places.

**How to know it's fixed:** `jq '.components.schemas.OrganisationUnit.properties.id'` returns non-null on `/api/openapi.json` for any DHIS2 version.

---

## 8. `/api/schemas` mis-reports the plural wire key for `UserRole.authorities` as "authoritys"

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, build revision `eaf4b70`, build time `2026-01-30`).

**Repro:** fetch the UserRole schema and check the `authorities` property:

```bash
curl -s -u admin:district \
  'http://localhost:8080/api/schemas/userRole?fields=properties[name,fieldName,collection,itemKlass]' \
  | jq '.properties[] | select(.name == "authority" or .name == "authorities" or .fieldName == "authorities")'
# {
#   "name": "authority",
#   "fieldName": "authoritys",
#   "collection": true,
#   "itemKlass": "java.lang.String"
# }
```

Yet the wire format DHIS2 actually returns + accepts is `authorities`:

```bash
curl -s -u admin:district 'http://localhost:8080/api/userRoles?fields=id,authorities&pageSize=1' \
  | jq '.userRoles[0] | keys'
# ["authorities", "id"]
```

**Expected:** `/api/schemas` reports `fieldName: "authorities"` so clients that build wire-name tables from `/api/schemas` get the right key.

**Actual:** `fieldName` is `"authoritys"` (naive `singular + "s"` suffix). The DHIS2 server's own serializer hand-overrides this to `authorities` on read/write, but `/api/schemas` leaks the underlying field name.

**Impact:** any client that derives the JSON key from `/api/schemas.fieldName` (as the Python workspace's `/api/schemas` codegen does) emits `authoritys` as the field name. Callers hit `unknown property` warnings or silent drops when passing `authoritys` to `POST /api/userRoles`, and reads via the generated model miss the field.

**Workaround in this repo:** `infra/scripts/build_e2e_dump.py` imports `UserRole` from `dhis2_client.generated.v42.oas` (the `/api/openapi.json` path, which reports `authorities` correctly) for the user-role seed step. The `/api/schemas`-derived `UserRole` model in `packages/dhis2-client/src/dhis2_client/generated/v42/schemas/user_role.py` still carries the buggy `authoritys` field name. A general fix in the `/api/schemas` emitter would be an allow-list override keyed by `(schema_name, property_name)` — low priority until another similar mis-pluralisation turns up.

**Expected improvement:** `/api/schemas` aligns `fieldName` with the actual wire key. Spotted only on `UserRole.authority` so far; possibly present on other Java-side collections whose plural doesn't follow "add s".

**How to know it's fixed:** `jq '.properties[] | select(.name == "authority") | .fieldName'` on `/api/schemas/userRole` returns `"authorities"`.

---

## 9. DHIS2's strict OIDC property parser rejects entire provider config on typos

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, build revision `eaf4b70`, build time `2026-01-30`).

**Repro:** Set an unknown key under `oidc.provider.dhis2.*` in `dhis.conf`:

```ini
oidc.provider.dhis2.logo_image = http://localhost:8080/logo.png
```

Restart DHIS2 and check the startup log:

```
ERROR GenericOidcProviderConfigParser — OpenID Connect (OIDC) configuration
      for provider: 'dhis2' contains an invalid property: 'logo_image',
      did you mean: 'login_image' ?
ERROR GenericOidcProviderConfigParser — OpenID Connect (OIDC) configuration
      for provider: 'dhis2' contains one or more invalid properties.
      Failed to configure the provider successfully! See previous errors...
```

Then attempt an OAuth2 login against DHIS2's own Spring AS and hit the API with the minted token:

```bash
TOKEN=...  # access_token returned by /oauth2/token
curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/system/info
# 401 {"message":"invalid_token","devMessage":"Invalid issuer"}
```

**Expected:** DHIS2 logs a warning for the typo, skips the unknown property, and registers the provider with the properties that parsed cleanly. The token minted by its own AS should validate on `/api/*` calls.

**Actual:** the entire provider registration fails. `DhisOidcProviderRepository` stays empty for `dhis2`, so the API-side JWT validator doesn't trust `iss = http://localhost:8080` even though DHIS2's own AS just minted the token with that issuer. Every authenticated API call fails with `Invalid issuer`.

**Impact:** a single typo in the `oidc.provider.<id>.*` block silently breaks end-to-end auth without any runtime error after startup — the symptom surfaces much later (401 on every token-authed call) far from the cause (startup config parse). Easy to mis-diagnose as a token-signing or audience problem.

**Workaround in this repo:** `infra/home/dhis.conf` now uses `login_image` / `login_image_padding` (the parser-accepted names, confirmed by GenericOidcProviderConfigParser.java's suggestion). Rebuilding the committed e2e dump picks up the fix. See docs/decisions.md for the original OIDC seed rationale.

**Expected improvement:** either warn-and-continue on unknown properties (so a typo doesn't brick the provider), or surface the full failure louder than a single `ERROR` line during startup (and explicitly on 401 with `Invalid issuer` when the corresponding issuer is a known-but-unregistered-provider mismatch).

**How to know it's fixed:** `logo_image` (or any other unknown key) in `oidc.provider.<id>.*` logs a warning at startup but the provider still registers. `curl -H "Authorization: Bearer <DHIS2-minted token>" /api/system/info` returns 200.

## 10. Login-page system-setting keys are a mix of prefixed and unprefixed

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro (against any v42 instance):**

```bash
# These key names look obvious from `/api/loginConfig` but most don't exist:
for name in applicationTitle applicationIntroduction applicationNotification applicationFooter applicationRightFooter; do
  curl -s -u admin:district -X POST -H 'Content-Type: text/plain' \
    --data "test-$name" "http://localhost:8080/api/systemSettings/$name" \
    -w "  $name -> %{http_code}\n"
done
#   applicationTitle       -> 200
#   applicationIntroduction -> 404  "Setting does not exist"
#   applicationNotification -> 404
#   applicationFooter       -> 404
#   applicationRightFooter  -> 404

# The real keys are mostly `key`-prefixed but `applicationTitle` is not:
curl -s -u admin:district http://localhost:8080/api/systemSettings \
  | python3 -c "import json,sys,re;d=json.load(sys.stdin);\
    [print(k) for k in sorted(d) if re.search('^(key)?(Application|Login|Custom)',k)]"
# applicationTitle
# keyApplicationFooter
# keyApplicationIntro
# keyApplicationNotification
# keyApplicationRightFooter
# keyCustomLoginPageLogo
# keyStyle
# keyUseCustomLogoFront
# ...
```

**Expected:** either all five application-text settings share a naming scheme (all prefixed or none), or `/api/loginConfig` uses the real wire-key names in its response so callers can round-trip read → mutate.

**Actual:** `/api/loginConfig` advertises field names `applicationTitle`, `applicationDescription`, `applicationNotification`, `applicationLeftSideFooter`, `applicationRightSideFooter` — none of which match the writeable system-setting keys (`applicationTitle`, `keyApplicationIntro`, `keyApplicationNotification`, `keyApplicationFooter`, `keyApplicationRightFooter`). A naive "read-modify-write" using the loginConfig response as-is fails with `Setting does not exist` on four of five fields.

**Impact:** any branding / deployment tool that tries to diff login-page state against a preset has to maintain its own translation table from loginConfig field → systemSettings key. Not documented anywhere in the API reference.

**Workaround in this repo:** `dhis2_client.customize.CustomizeAccessor` and `infra/login-customization/preset.json` hardcode the five correct wire-key names. See `docs/architecture/login-customization.md` for the field↔key mapping.

**Expected improvement:** either rename the system-setting keys so `/api/loginConfig` field names match (preferred — it's a greenfield rename in the DHIS2 codebase, no external API contract is broken because system-settings POST and loginConfig GET aren't the same endpoint), or document the translation table prominently next to `/api/loginConfig` and `/api/systemSettings`.

**How to know it's fixed:** `POST /api/systemSettings/applicationIntroduction` with body `"x"` returns 200 — or the DHIS2 docs gain a "login-page settings" page that enumerates every wire-key name that affects `/api/loginConfig`.

---

## 11. `POST /api/staticContent/logo_front` succeeds but DHIS2 keeps serving the built-in default until `keyUseCustomLogoFront=true` is also set

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro (against any v42 instance):**

```bash
# 1. Upload a custom logo — HTTP 204, bytes land on disk:
curl -s -u admin:district -F "file=@my_logo.png;type=image/png" \
  http://localhost:8080/api/staticContent/logo_front -w "upload %{http_code}\n"
# upload 204

# 2. Read it back — gets a 302 to the DHIS2 default, NOT the uploaded bytes:
curl -sL -u admin:district http://localhost:8080/api/staticContent/logo_front.png -o /tmp/got.png \
  -w "final %{url_effective} (%{size_download} bytes)\n"
# final http://localhost:8080/dhis-web-commons/security/logo_front.png (3082 bytes)
# ^ 3082 bytes = DHIS2 built-in, not my_logo.png

# 3. Flip the magic flag and re-fetch — now DHIS2 serves the uploaded bytes:
curl -s -u admin:district -X POST -H 'Content-Type: text/plain' --data 'true' \
  http://localhost:8080/api/systemSettings/keyUseCustomLogoFront
curl -sL -u admin:district http://localhost:8080/api/staticContent/logo_front.png -o /tmp/got2.png \
  -w "final %{url_effective} (%{size_download} bytes)\n"
# final http://localhost:8080/api/staticContent/logo_front.png (<my upload size> bytes)
```

**Expected:** `POST /api/staticContent/logo_front` either (a) stores the file AND activates it (one call, one effect), or (b) returns 4xx / a response body that tells the caller another step is needed. Same for `logo_banner`.

**Actual:** the POST silently stores the file under `DHIS2_HOME/files/document/logo_front` but leaves `keyUseCustomLogoFront` at its default `false`. Subsequent GETs serve the built-in default from the webapp classpath. The caller has no feedback that the upload had no user-visible effect until they look at `/api/loginConfig.useCustomLogoFront` or try a GET.

**Impact:** every first-time caller of the customisation API spends time figuring out why their upload didn't take. The same trap applies to the banner via `keyUseCustomLogoBanner`.

**Workaround in this repo:** `Dhis2Client.customize.upload_logo_front(...)` automatically POSTs `keyUseCustomLogoFront=true` after the staticContent upload (same for banner). Callers never need to know the flag exists. See `packages/dhis2-client/src/dhis2_client/customize.py`.

**Expected improvement:** either auto-activate on successful upload, or return a 201 with a body like `{"httpStatus":"OK","activated":false,"nextStep":"POST /api/systemSettings/keyUseCustomLogoFront=true"}` so the caller knows. Documenting the two-step dance in the API reference would also help.

**How to know it's fixed:** after a single `POST /api/staticContent/logo_front` upload, `GET /api/staticContent/logo_front.png` serves the uploaded bytes (no 302 to `/dhis-web-commons/security/logo_front.png`) AND `/api/loginConfig.useCustomLogoFront` is `true`, without any additional `POST /api/systemSettings/keyUseCustomLogoFront` call.

## 12. DHIS2 login app leaves `html` transparent, so browser zoom > 100% exposes the browser's background below the page

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`, login app `apps/dhis2-login-app` bundle `main-Dmx4sX17.css` / `app-DHjc329F.css`).

**Repro:**

1. Load `http://localhost:8080/dhis-web-login/` in Chrome on a HiDPI display.
2. Zoom to 110% or 125% (`Cmd +` on macOS, `Ctrl +` on Linux/Windows) — or alternatively use a tall window (e.g. 1305px viewport height) where CSS `100vh` resolves to fewer pixels than the actual window area due to toolbar/zoom.
3. Observe the login page: blue fills the top portion, a solid black band spans the bottom portion.

```js
// In DevTools:
getComputedStyle(document.documentElement).backgroundColor
// > "rgba(0, 0, 0, 0)"
getComputedStyle(document.body).backgroundColor
// > "rgb(42, 82, 152)"
getComputedStyle(document.querySelector('.app')).height
// > "900px"        // == CSS 100vh
document.body.offsetHeight
// > 900            // < window.innerHeight when zoomed
```

**Expected:** the `html` element also has `background: #2a5298` (or the `.app` container has `min-height: 100%` plus a background chain that reaches `html`), so the blue fills the actual viewport at any zoom level.

**Actual:** the login-app inline `<style>` tag sets:

```css
body { padding: 0; margin: 0; background: #2a5298; }
.app { display: flex; flex-direction: column; height: 100vh; width: 100vw; }
```

— but never touches `html`. When `.app` is shorter than the browser's visible height, the transparent html shows through as whatever the browser's default is (dark grey/black in dark-theme Chrome, white in light).

**Impact:** on any machine with non-100% zoom or a tall window, the login page looks broken. Particularly visible on 4K/HiDPI monitors where users commonly run at 110–150% zoom.

**Workaround in this repo:** none available through the DHIS2 API. `POST /api/files/style` only affects post-auth pages; the login app is a separate React bundle that doesn't include it. A full `loginPageTemplate` replacement is too heavy for a single CSS rule. Documented as a known limitation in `docs/architecture/customize-plugin.md`.

**Expected improvement:** add `html { background: #2a5298; min-height: 100vh; }` to the login-app's inline styles (or, better, to the bundled CSS). One line fix.

**How to know it's fixed:** load the login page at 125% browser zoom — blue fills the entire viewport with no black band at the bottom.

## 13. `OutlierDetectionAlgorithm` OAS enum reports `MOD_Z_SCORE` but DHIS2 rejects that value at runtime

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# OAS says MOD_Z_SCORE is valid:
grep -A4 '"OutlierDetectionAlgorithm"' packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json
#   "enum": ["Z_SCORE", "MIN_MAX", "MOD_Z_SCORE", "INVALID_NUMERIC"]

# But calling the endpoint with that value returns 400:
curl -s -u admin:district \
  'http://localhost:8080/api/analytics/outlierDetection?ds=NORMonthDS1&ou=NOROsloProv&pe=LAST_12_MONTHS&algorithm=MOD_Z_SCORE' \
  | python3 -m json.tool | head -5
# {"httpStatus":"Bad Request","httpStatusCode":400,"status":"ERROR",
#  "message":"Value 'MOD_Z_SCORE' is not valid for parameter algorithm.
#             Valid values are: [Z_SCORE, MIN_MAX, MODIFIED_Z_SCORE]", ...}

# MODIFIED_Z_SCORE works:
curl -s -u admin:district \
  'http://localhost:8080/api/analytics/outlierDetection?ds=NORMonthDS1&ou=NOROsloProv&pe=LAST_12_MONTHS&algorithm=MODIFIED_Z_SCORE' \
  | python3 -m json.tool | head -3
# { "headers": [...], "rows": [...] }   <- 200 OK
```

**Expected:** OAS enum values match the server's actual accepted set. Either the OAS says `MODIFIED_Z_SCORE` or the server accepts `MOD_Z_SCORE`.

**Actual:** OAS `OutlierDetectionAlgorithm` enum declares `{Z_SCORE, MIN_MAX, MOD_Z_SCORE, INVALID_NUMERIC}`. The server's actual accept-list is `{Z_SCORE, MIN_MAX, MODIFIED_Z_SCORE}`. The OAS name is truncated; the server name isn't. (A second enum `OutlierMethod` in the same OAS file has `MODIFIED_Z_SCORE` — so the symbol exists upstream, but it's wired to the wrong parameter type.)

**Impact:** callers with IDE autocomplete or strict typing reach for `OutlierDetectionAlgorithm.MOD_Z_SCORE`, ship code, then get a 400 at runtime. Users who `grep` DHIS2 docs for "algorithm" values see inconsistent naming. Blocked the first run of `examples/cli/analytics_outlier_tracked_entities.sh`.

**Workaround in this repo:** CLI + examples use the string `"MODIFIED_Z_SCORE"` directly; docstrings + BUGS.md entry call out the mismatch. A typed helper (`OutlierDetectionAlgorithm.MODIFIED_Z_SCORE` alias) isn't added because the enum member genuinely doesn't exist in the OAS emission — would need a post-emission patch step which is worse than the string.

**Expected improvement:** upstream, either rename the OAS enum member `MOD_Z_SCORE` → `MODIFIED_Z_SCORE`, or alias the short name server-side. Either fix unblocks typed callers.

**How to know it's fixed:** `grep MOD_Z_SCORE packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json` returns nothing after the next `dhis2 dev codegen` regeneration against a patched DHIS2.

**Status on v43 (2.43.1-SNAPSHOT, dev-2-43):** NOT fixed — `OutlierDetectionAlgorithm` still declares `{Z_SCORE, MIN_MAX, MOD_Z_SCORE, INVALID_NUMERIC}` on the v43 OAS. The truncated name remains; the workaround is still required.

---

## 14. OAS `Route.auth` is a `oneOf` with no discriminator — and the auth-scheme schemas are missing their Jackson `type` field

**Observed on:** DHIS2 `2.42.4` (`packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json`, DHIS2-generated Swagger spec).

**Repro:**

```bash
# Route.auth is an unconstrained oneOf:
jq '.components.schemas.Route.properties.auth' \
  packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json
# {
#   "oneOf": [
#     { "$ref": "#/components/schemas/HttpBasicAuthScheme" },
#     { "$ref": "#/components/schemas/ApiTokenAuthScheme" },
#     { "$ref": "#/components/schemas/ApiHeadersAuthScheme" },
#     { "$ref": "#/components/schemas/ApiQueryParamsAuthScheme" },
#     { "$ref": "#/components/schemas/OAuth2ClientCredentialsAuthScheme" }
#   ]
# }

# No `discriminator` block on the oneOf. And the individual schemas
# don't carry a `type` field either:
jq '.components.schemas.HttpBasicAuthScheme' \
  packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json
# {
#   "properties": {
#     "password": { "type": "string" },
#     "username": { "type": "string" }
#   },
#   "required": ["password", "username"],
#   "type": "object"
# }
# ^ no "type" property — but on the wire DHIS2 requires {"type": "http-basic", ...}.
```

**Expected:** Either

1. The `oneOf` carries a `discriminator` block:
   ```json
   "discriminator": {
     "propertyName": "type",
     "mapping": {
       "http-basic": "#/components/schemas/HttpBasicAuthScheme",
       "api-token":  "#/components/schemas/ApiTokenAuthScheme",
       "api-headers": "#/components/schemas/ApiHeadersAuthScheme",
       "api-query-params": "#/components/schemas/ApiQueryParamsAuthScheme",
       "oauth2-client-credentials": "#/components/schemas/OAuth2ClientCredentialsAuthScheme"
     }
   }
   ```
   And each referenced schema has `"type": { "type": "string", "enum": ["<tag>"] }` in its required properties.

2. Or, since the Java side uses Jackson's `@JsonTypeInfo(include = As.PROPERTY, property = "type")` + `@JsonSubTypes`, the OAS generator could project that directly into OpenAPI's discriminator syntax — the two are 1:1.

**Actual:** Neither. The `oneOf` is bare and the variant schemas drop the tag field.

**Impact:**

- Code generators (ours included) can't emit a typed tagged-union for `Route.auth`. Pydantic's `Field(discriminator="type")` can't be used because the variants don't declare a `Literal["<tag>"]` type field.
- Clients that construct a Route auth block from Python have no type-safe path to pick the right variant — you're down to dicts or `extra="allow"` carveouts.
- Reads work by accident (`extra="allow"` preserves the incoming `type` field) but writes are brittle: you have to remember to include `{"type": "..."}` manually on every payload.
- Blast radius is bigger than Route — this pattern repeats anywhere DHIS2 uses Jackson polymorphic subclasses (e.g. `AuthScheme` is referenced elsewhere; `AnalyticalObject` has similar shape).

**Current status:** patched locally in codegen. `packages/dhis2-codegen/src/dhis2_codegen/spec_patches.py::_patch_auth_scheme_discriminators` injects the discriminator block on `Route.auth`, `RouteParams.auth`, and `WebhookTarget.auth` before emission, and tags every `*AuthScheme` variant with its `type: Literal["<tag>"]` (plus restores `scopes` on `OAuth2ClientCredentialsAuthScheme`, which upstream also omits). Post-patch, the generated `Route.auth` is `Annotated[HttpBasicAuthScheme | ApiTokenAuthScheme | ... , Field(discriminator="type")] | None` and `RoutePayload.auth: AuthScheme | None` in the route plugin's service layer. The patch is idempotent — it short-circuits if DHIS2 ever lands a proper `discriminator` block upstream.

**Expected upstream fix:** DHIS2's springdoc/swagger generator should project the Jackson `@JsonTypeInfo` annotations into OpenAPI discriminator syntax:

```json
"Route": {
  "properties": {
    "auth": {
      "oneOf": [...],
      "discriminator": {
        "propertyName": "type",
        "mapping": {
          "http-basic": "#/components/schemas/HttpBasicAuthScheme",
          ...
        }
      }
    }
  }
}
```

And every `*AuthScheme` schema should declare a required `type` property with a single-value `enum` of its wire tag.

**How to know it's fixed:** `jq '.components.schemas.Route.properties.auth.discriminator' openapi.json` returns a non-null object after regeneration; every auth-scheme schema has a required `type` property with an `enum` of one value. At that point `spec_patches._patch_auth_scheme_discriminators` becomes a no-op and can be retired.

**Status on v43 (2.43.1-SNAPSHOT, dev-2-43):** NOT fixed — `Route.auth` is still a bare `oneOf` on the v43 OAS, `HttpBasicAuthScheme` / `ApiTokenAuthScheme` / etc. still omit the `type` property. Our codegen spec-patch (`_patch_auth_scheme_discriminators`) fires cleanly on v43 emission too, so downstream consumers don't notice a difference.

---

## 15. OAS emits `JobConfiguration.jobParameters` and `WebMessage.response` as undiscriminated `oneOf`s

**Observed on:** DHIS2 `2.42.4` (same OAS-gap family as #14).

**Repro:**

```bash
# 23 variants, no discriminator:
jq '.components.schemas.JobConfiguration.properties.jobParameters' \
  packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('variants:', len(d.get('oneOf',[]))); print('has discriminator:', 'discriminator' in d)"
# variants: 23
# has discriminator: False

# 17 variants, no discriminator:
jq '.components.schemas.WebMessage.properties.response' \
  packages/dhis2-client/src/dhis2_client/generated/v42/openapi.json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('variants:', len(d.get('oneOf',[]))); print('has discriminator:', 'discriminator' in d)"
# variants: 17
# has discriminator: False
```

**Expected:** Both `oneOf`s carry a `discriminator` block identifying the Jackson type property. DHIS2's `JobParameters` hierarchy uses `@JsonTypeInfo(include = As.PROPERTY, property = "type")` server-side; `WebMessageResponse` has a similar polymorphic shape.

**Actual:** Bare `oneOf` on both. Same root cause as #14 (springdoc not projecting Jackson annotations).

**Impact:** Matches #14 — codegen can't emit typed tagged unions. Wider blast radius than `Route.auth` because these unions have 23 and 17 variants respectively, and the parent schemas are used heavily:

- `JobConfiguration` is the whole scheduler / async-task surface (`/api/jobConfigurations`).
- `WebMessage.response` is the body of every DHIS2 write that returns a detailed report (`ImportSummary`, `PredictionSummary`, `MergeWebResponse`, `ObjectReport`, ...).

**Workaround in this repo:**

- `WebMessage.response` is already flattened to `dict[str, Any]` via an explicit override in `_FIELD_OVERRIDES` (`packages/dhis2-codegen/src/dhis2_codegen/oas_emit.py`); the hand-written `dhis2_client.envelopes.WebMessageResponse` provides typed accessor methods (`.import_count()`, `.conflicts()`, ...) that project the field into useful shapes on demand.
- `JobConfiguration.jobParameters` doesn't have a workaround yet. The maintenance plugin uses `dict[str, Any]` for job-params input; a future `spec_patches.py` entry can tag these the same way #14 handled AuthScheme once the mapping from wire-tag to variant class is confirmed (DHIS2's `JobParametersSubtypes` enum + `@JsonSubTypes` is the ground truth).

**Expected upstream fix:** same as #14 — project Jackson annotations into OpenAPI discriminator syntax.

**How to know it's fixed:** run the same `jq` repro and see a non-null discriminator block; codegen then picks it up with zero repo changes.

**Status on v43 (2.43.1-SNAPSHOT, dev-2-43):** NOT fixed — `JobConfiguration.jobParameters` still emits as a bare `oneOf` (22 variants, dropped from 23 — membership is drifting slightly but discriminator still absent). `WebMessage.response` also unchanged (17 variants, no discriminator).

## 16. `POST /api/documents` rejects multipart uploads with 415, forcing a two-step upload flow

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# 1. Naive multipart POST as you'd do for any file upload endpoint:
echo "hello dhis2" > /tmp/hello.txt
curl -s -u admin:district \
  -F 'file=@/tmp/hello.txt' \
  -F 'name=smoke-test' \
  'http://localhost:8080/api/documents' \
  -w '\n%{http_code}  %{content_type}\n'
# {"httpStatus":"Unsupported Media Type",
#  "message":"Content-Type 'multipart/form-data;boundary=...' is not supported"}
# 415  application/json

# 2. The documented OpenAPI spec only lists `application/json` as acceptable,
#    so binary-upload must go through a fileResource first:
curl -s -u admin:district -F 'file=@/tmp/hello.txt' \
  'http://localhost:8080/api/fileResources?domain=DOCUMENT' \
  -w '\n%{http_code}\n'
# {"response":{"fileResource":{"id":"TacExtJuMmW", ...}}}
# 202

# 3. Then create the document pointing at the fileResource uid:
curl -s -u admin:district -H 'Content-Type: application/json' \
  -d '{"name":"smoke-test","url":"TacExtJuMmW","external":false,"attachment":true}' \
  'http://localhost:8080/api/documents' \
  -w '\n%{http_code}\n'
# {"response":{"uid":"RTkjSgLtdI6", ...}}
# 201
```

**Expected:** `POST /api/documents` either (a) accepts `multipart/form-data`
directly — matching `POST /api/fileResources` and `POST /api/staticContent/{key}`
— or (b) documents the two-step flow prominently in the endpoint's OpenAPI
description and the user-facing docs.

**Actual:** The OpenAPI spec silently lists only `application/json` as an
accepted request content-type; callers reasonably assume multipart works by
analogy to `/api/fileResources` and hit a bare 415 with no hint at the
workflow they need to use instead.

**Impact:** Every caller hand-rolls the two-step. There's no affordance on
the wire for discovering this — a multipart POST looks like the right thing
to try given the rest of DHIS2's file-upload surface, and the error message
doesn't mention fileResources.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/files.py::FilesAccessor.upload_document`
does the two-step automatically — uploads the bytes as a `FileResource` with
`domain=DOCUMENT`, then posts the document JSON with `url=<fileResource.id>`.
Callers see `client.files.upload_document(data, name=...)` and get back a
typed `Document`.

**Expected upstream fix (in order of preference):**

1. Accept multipart on `POST /api/documents` and do the fileResource hop
   server-side — matches the ergonomics of `/api/fileResources` and
   `/api/staticContent/{key}`.
2. If that's not feasible, return a 400 with an `upload via /api/fileResources
   first` hint instead of a bare 415.
3. At minimum, document the two-step in the OpenAPI description on
   `POST /api/documents` so the OAS reader sees the guidance.

**How to know it's fixed:** re-run the naive `curl -F file=...` against
`/api/documents` and see it create a document that `GET /api/documents/{uid}/data`
can then download. No code change needed in this repo if a 2.43+ fix
accepts multipart — `upload_document` can detect multipart support with a
probe later, but the two-step path will keep working indefinitely.

## 17. `POST /api/messageConversations` returns the new UID on the `Location` header, not in the JSON envelope

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# Look at a normal create — e.g. /api/dataElements. The envelope carries the new UID:
curl -s -u admin:district -H 'Content-Type: application/json' \
  -d '{"name":"probe","shortName":"p","aggregationType":"SUM","domainType":"AGGREGATE","valueType":"TEXT","categoryCombo":{"id":"bjDvmb4bfuf"}}' \
  'http://localhost:8080/api/dataElements'
# {"httpStatus":"Created","status":"OK","response":{"responseType":"ObjectReport","uid":"aB3dEf5gH7i", ...}}

# Now do the same against /api/messageConversations:
curl -s -i -u admin:district -H 'Content-Type: application/json' \
  -d '{"subject":"probe","text":"body","users":[{"id":"M5zQapPyTZI"}]}' \
  'http://localhost:8080/api/messageConversations'
# HTTP/1.1 201
# Location: http://localhost:8080/api/messageConversations/lQtpMU8ChLW
# {"httpStatus":"Created","httpStatusCode":201,"status":"OK","message":"Message conversation created"}
#
# NOTE: no `response.uid` in the JSON body. The UID is ONLY on the Location header.
```

**Expected:** `POST /api/messageConversations` returns the same
`WebMessage`-with-`ObjectReport` envelope every other create endpoint returns —
with `response.responseType = "ObjectReport"` and `response.uid` populated to
the new conversation's UID. Matches `/api/dataElements`, `/api/indicators`,
every metadata CRUD endpoint, and the documented `WebMessage` schema in the
OpenAPI spec.

**Actual:** The envelope stops at the status block (`httpStatus`, `status`,
`message`) — no `response` key at all. Discovering the new UID requires
parsing the 201 `Location` header. Callers using only the JSON body see
success-without-a-handle and have to do a follow-up list/filter call to
locate the message they just sent.

**Impact:** Every client that tries to look up the newly-sent conversation
after `send()` (to attach tracking metadata, link into a ticketing system,
or simply confirm the write) hits a dead end unless it inspects HTTP
headers too. Most high-level HTTP clients hide header access behind an
extra `raw_response` call, so this invariably surfaces as a "how do I get
the UID back?" question from every new integrator.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/messaging.py::MessagingAccessor.send`
uses the low-level `_request` path to access response headers, parses the
final path segment of `Location` as the UID, and GETs the conversation
back so the caller receives a typed `MessageConversation` (matches the
ergonomics of `files.upload_document` / `resources.<x>.create`). A
`RuntimeError` fires if DHIS2 returns 201 without a `Location` header —
defensive; haven't seen DHIS2 omit it in practice.

**Expected upstream fix:** project the `ObjectReport` response DHIS2 has
internally (the new conversation IS persisted as an object at that point)
into the `WebMessage.response` field, so the envelope matches the rest of
the create-endpoint family. `/api/messages` has the same shape and
probably the same fix.

**How to know it's fixed:** `response.uid` populated on a 201 from
`POST /api/messageConversations` lets us drop the Location-header parsing
path — `messaging.send` can then mirror `files.upload_document` exactly.

## 18. `POST /api/messageConversations/{uid}` takes `text/plain` body; `send` requires `{id}` refs for attachments

Two wire-shape quirks on DHIS2 v42's messaging surface, related enough to
record together. Both surface on any client hitting `/api/messageConversations*`.

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

### 18a. Reply endpoint stores the request body verbatim as message text

**Repro:**

```bash
# Send a message with DHIS2 admin talking to themselves:
SUBJ_UID=$(curl -s -u admin:district -i -H 'Content-Type: application/json' \
  -d '{"subject":"probe","text":"first","users":[{"id":"M5zQapPyTZI"}]}' \
  'http://localhost:8080/api/messageConversations' \
  | awk '/^[Ll]ocation:/ {print $2}' | tr -d '\r' | awk -F/ '{print $NF}')

# The JSON-object body looks right — it matches every OTHER create endpoint's shape:
curl -s -u admin:district -H 'Content-Type: application/json' \
  -d '{"text":"second"}' \
  "http://localhost:8080/api/messageConversations/$SUBJ_UID"
# 201 Created  -> seems fine

# But what got stored is the raw JSON, not the text:
curl -s -u admin:district \
  "http://localhost:8080/api/messageConversations/$SUBJ_UID?fields=messages[id,text]"
# {"messages":[{"id":"...","text":"first"},{"id":"...","text":"{\"text\":\"second\"}"}]}
#                                                          ^^^ ←  stringified JSON, not "second"

# Plain text body is what DHIS2 actually expects here:
curl -s -u admin:district -H 'Content-Type: text/plain' \
  --data 'third' \
  "http://localhost:8080/api/messageConversations/$SUBJ_UID"
# stored as: {"text":"third"} — correct.
```

**Expected:** `POST /api/messageConversations/{uid}` parses the request
body according to `Content-Type` — JSON for `application/json` (reading
`text` / `attachments` / `internal`), plain text for `text/plain`.
Matches every other POST endpoint on DHIS2.

**Actual:** The handler ignores `Content-Type` and reads the body as a raw
string, storing it verbatim as the new message's `text`. JSON-object
callers end up with `"{\"text\":\"...\"}"` as the literal message.
Callers can't attach fileResources on replies, or set the `internal`
ticket-note flag (two fields documented elsewhere for `Message`).

**Impact:** High-level clients can't round-trip through `Message`
serialization on replies — every reply has to bypass the typed flow and
send raw bytes. Attachments only work at initial `send`.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/messaging.py::MessagingAccessor.reply`
encodes its `text` argument as UTF-8 bytes and sends `Content-Type: text/plain`.
`attachments=` + `internal=` parameters were dropped from the signature
since they silently no-op — documented in the method docstring.

### 18b. `attachments` on `send` needs `{id}` refs, not bare UID strings

**Repro:**

```bash
# Upload a MESSAGE_ATTACHMENT fileResource first — produces some FR uid:
FR_UID=$(curl -s -u admin:district -F 'file=@/tmp/hello.txt' \
  'http://localhost:8080/api/fileResources?domain=MESSAGE_ATTACHMENT' \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["response"]["fileResource"]["id"])')

# Bare UID strings in attachments[] — OAS-documented shape on Message.attachments:
curl -s -u admin:district -H 'Content-Type: application/json' \
  -d '{"subject":"attach","text":"body","users":[{"id":"M5zQapPyTZI"}],"attachments":["'"$FR_UID"'"]}' \
  'http://localhost:8080/api/messageConversations' \
  -w '\n%{http_code}\n'
# 500 Internal Server Error

# Wrap in {id} refs — works:
curl -s -u admin:district -H 'Content-Type: application/json' \
  -d '{"subject":"attach","text":"body","users":[{"id":"M5zQapPyTZI"}],"attachments":[{"id":"'"$FR_UID"'"}]}' \
  'http://localhost:8080/api/messageConversations' \
  -w '\n%{http_code}\n'
# 201 Created
```

**Expected:** DHIS2 accepts `attachments: [String]` per the `Message`
OAS schema (`attachments: array[string]`) — a list of fileResource UIDs.

**Actual:** Bare UIDs produce a 500 with no error body. Only `{"id":
uid}` reference objects work. The OAS schema for `Message.attachments`
is typed as `array[string]` on v42 but the handler requires
`array[ObjectNode]`.

**Workaround in this repo:**
`MessagingAccessor.send` takes `attachments: Sequence[str]` and wraps
each UID as `{"id": uid}` before serialisation. Callers pass plain UID
lists; the accessor handles the wrapping.

### Impact summary

Both quirks silently fail (or fail with opaque 500s) for any
typed-client that follows the OAS spec or the standard DHIS2 "POST JSON
body" convention. `messaging.send` / `messaging.reply` in
`dhis2_client` paper over both; upstream callers who hit DHIS2 directly
will need the same two workarounds.

**Expected upstream fix:**
- Reply endpoint should honour `Content-Type` and parse a JSON body with
  `text` / `attachments` / `internal` keys when the header says JSON —
  matches every other DHIS2 POST.
- Attachment schema for `Message.attachments` should either accept bare
  UIDs (matching the OAS type) or the OAS type should be corrected to
  `array[Reference]`.

**How to know it's fixed:**
- `curl -H 'Content-Type: application/json' -d '{"text":"x"}' .../convUid` → stored text is `x`, not `{"text":"x"}`.
- `curl ... -d '{"attachments":["<fr-uid>"]}' .../messageConversations` → 201, not 500.

## 19. `GET /api/validationResults` silently ignores `fields=*` and `fields=:all`

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# Make sure some persisted results exist (run any VR analysis with persist=true first).
# Default call returns id-only nested refs:
curl -s -u admin:district \
  'http://localhost:8080/api/validationResults?pageSize=1' \
  | jq '.validationResults[0]'
# {
#   "validationRule": { "id": "WQ9mjcYCFJE" },
#   "organisationUnit": { "id": "NORNordland" },
#   "period": { "id": "202501" },
#   ...
# }

# `fields=*` doesn't expand — still id-only:
curl -s -u admin:district \
  'http://localhost:8080/api/validationResults?pageSize=1&fields=*' \
  | jq '.validationResults[0].validationRule'
# { "id": "WQ9mjcYCFJE" }

# Same for `fields=:all`:
curl -s -u admin:district \
  'http://localhost:8080/api/validationResults?pageSize=1&fields=:all' \
  | jq '.validationResults[0].validationRule'
# { "id": "WQ9mjcYCFJE" }

# Explicit nested selection DOES work:
curl -s -u admin:district \
  'http://localhost:8080/api/validationResults?pageSize=1&fields=id,validationRule[id,displayName,importance,operator],organisationUnit[id,displayName],period[id,displayName],leftsideValue,rightsideValue' \
  | jq '.validationResults[0].validationRule'
# {
#   "id": "WQ9mjcYCFJE",
#   "displayName": "ANC 1st >= ANC 4th",
#   "importance": "HIGH",
#   "operator": "greater_than_or_equal_to"
# }
```

**Expected:** `fields=*` / `fields=:all` expand nested refs the same way
they do on every other metadata endpoint — `validationRule` comes back
with at least `id + displayName`, matching how `/api/dataElements?fields=*`
behaves.

**Actual:** The `/api/validationResults` handler treats `fields=*` and
`fields=:all` as no-ops — nested refs stay at `{id}` alone regardless.
Only an explicit field selector like
`validationRule[id,displayName,importance,operator]` pulls the nested
properties. The underlying rule's `operator` + `importance` also aren't
accessible through any preset — you have to name both inside the nested
selector.

**Impact:** CLI / SDK callers listing violations for display can't rely on
the standard preset shorthand; every tool has to hand-roll the full
nested selector or make a second round-trip to `/api/validationRules/{id}`
just to render a usable table.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/validation.py::_DEFAULT_RESULT_FIELDS`
is a hard-coded selector sent on every `list_results` / `get_result`
call. Callers that want the thin (id-only) shape for large sweeps pass
`fields="id,validationRule[id],..."` explicitly. The CLI's `validation
result list` table reads `importance` / `operator` via `model_extra`
since `BaseIdentifiableObject` doesn't type those fields.

**Expected upstream fix:**
- `/api/validationResults` should honour the normal `fields` preset
  expansion. `fields=*` expanding `validationRule` to
  `id + displayName + every primitive property` is the behaviour every
  other metadata endpoint exhibits.
- Or DHIS2 could flatten `importance` + `operator` onto the
  `ValidationResult` response directly (like the `/api/dataAnalysis/validationRules`
  path already does), which would also remove the cross-endpoint
  inconsistency we hit in the flat-vs-nested shape divergence.

**How to know it's fixed:**
- `curl 'http://localhost:8080/api/validationResults?fields=*'` returns
  nested refs with at least `displayName` populated.
- `curl 'http://localhost:8080/api/validationResults?fields=:all'`
  returns nested refs with `displayName + operator + importance`.

## 20. `DELETE /api/options/{uid}` returns 200 OK but leaves the option in place

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# Assume the seeded OptionSet OsVaccType1 with an "HPV" option (uid TnI3wDs1bKL).
curl -s -u admin:district -X DELETE \
  http://localhost:8080/api/options/TnI3wDs1bKL
# {"httpStatus":"OK","httpStatusCode":200,"status":"OK",
#  "response":{"uid":"TnI3wDs1bKL","klass":"org.hisp.dhis.option.Option",
#              "errorReports":[],"responseType":"ObjectReportWebMessageResponse"}}

# …but the option is still there:
curl -s -u admin:district \
  'http://localhost:8080/api/options?filter=code:eq:HPV&fields=id,code'
# {"pager":{...},"options":[{"id":"TnI3wDs1bKL","code":"HPV",...}]}
```

**Expected:** `DELETE /api/options/{uid}` actually removes the option
from the database (same semantics as `DELETE /api/dataElements/{uid}`
etc.). Matches every other per-resource DELETE endpoint on DHIS2.

**Actual:** The endpoint acknowledges the request with a full
`ObjectReportWebMessageResponse` envelope + `status=OK` + empty
`errorReports`, but the option row is untouched. Subsequent GETs still
return it; it also still shows up under the owning OptionSet's
`options` list. There's no 409, no conflict, no warning — the delete
simply doesn't take effect.

**Impact:** Any workflow that wants to shrink an OptionSet must route
deletes through `POST /api/metadata?importStrategy=DELETE` with the
options bundled there. Callers relying on the per-resource DELETE
surface get a silently-broken path.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/option_sets.py::OptionSetsAccessor.upsert_options`
routes removals through `client.metadata.delete_bulk("options", uids)`
(which posts `POST /api/metadata?importStrategy=DELETE`). Tested
end-to-end with a round-trip that adds two options and then rolls
them back — removes do commit via this path.

**Expected upstream fix:**
`DELETE /api/options/{uid}` should actually delete the row, matching
every other per-resource DELETE endpoint. At minimum it should return
`409 Conflict` (or an envelope with a non-empty `errorReports`) if
deletion via this route is intentionally not supported, so callers
can't be fooled by a 200 status.

**How to know it's fixed:**
- `curl -X DELETE .../options/<uid>` → subsequent GET on the same UID
  returns 404 (or the option's absent from the owning set's list).

## 21. Attribute-value filters: path property is the Attribute UID, not `attributeValues.value`

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

**Repro:**

```bash
# Seeded: OptionSet OsVaccType1 with 5 options, each carrying an
# AttributeValue for attribute AttrSnom001 (code SNOMED_CODE).

# Obvious-but-wrong: filter by nested property path. 400.
curl -s -u admin:district -G http://localhost:8080/api/options \
  --data-urlencode 'filter=optionSet.id:eq:OsVaccType1' \
  --data-urlencode 'filter=attributeValues.value:eq:386661006' \
  --data-urlencode 'fields=id,code'
# {"httpStatus":"Bad Request","httpStatusCode":400,"status":"ERROR",
#  "message":"Unknown path property: attributeValues.value","errorCode":"E1003"}

# Actually-works: filter by the attribute's UID used *as the property name*.
curl -s -u admin:district -G http://localhost:8080/api/options \
  --data-urlencode 'filter=optionSet.id:eq:OsVaccType1' \
  --data-urlencode 'filter=AttrSnom001:eq:386661006' \
  --data-urlencode 'fields=id,code'
# {"options":[{"code":"MEASLES","id":"OptVacMes01"}]}

# Plausible-sounding alternatives silently match everything (no filter):
# `attributeValues[AttrSnom001]:eq:386661006` returns all 5 options.
```

**Expected:** `filter=attributeValues.value:eq:X` works the way every
other nested-property filter works — walks into the `AttributeValue`
schema, matches `value` against `X`, filters server-side. Consistent
with `filter=optionSet.id:eq:UID`, `filter=categoryCombo.id:eq:UID`,
etc.

**Actual:** The nested-property-path walk stops at
`attributeValues.value` (E1003). The only server-side filter that
actually matches attribute values is to use the **Attribute's UID** as
the property name — `filter=<attrUid>:eq:<value>`. This is an
undocumented shorthand the DHIS2 query DSL reserves for attribute
filtering; no other DHIS2 filter works this way.

**Impact:** Integration code that wants to reverse-lookup a metadata
object by an external-system code has to (a) know about this shorthand
and (b) first resolve the Attribute's UID from its business code before
it can filter. Raw-URL callers get silent empty results or cryptic
400s; typed accessors have to paper over the surface difference.

**Workaround in this repo:**
`packages/dhis2-client/src/dhis2_client/option_sets.py::OptionSetsAccessor.find_option_by_attribute`
calls `_resolve_attribute_uid(code_or_uid)` first (turns
`SNOMED_CODE` → `AttrSnom001` via `/api/attributes?filter=code:eq:...`)
and then emits the filter as `AttrSnom001:eq:386661006`. The shorthand
is hidden entirely from the caller — who passes the business code as
the API intends.

**Expected upstream fix:**
- Make `filter=attributeValues.value:eq:X` walk the nested property
  the same way every other ref-valued field does. The current "filter
  by the attribute's UID" shorthand can stay as syntactic sugar, but
  the obvious nested-path form should also work.
- Alternatively, at minimum document the UID-as-property-name
  shorthand on `/api/docs` — it's genuinely useful once you know about
  it, but undiscoverable today.

**How to know it's fixed:**
- `curl 'http://localhost:8080/api/options?filter=attributeValues.value:eq:386661006&filter=optionSet.id:eq:OsVaccType1'`
  returns the MEASLES option (and no others) instead of E1003.

## 22. `ProgramRuleVariable.sourceType` is a schema fiction — wire uses `programRuleVariableSourceType` (and `fields=*` omits it)

**Observed on:** DHIS2 `2.42.4` (core image `dhis2/core:42`).

Two related quirks on `/api/programRuleVariables`, both caught while
seeding the e2e dump with realistic program rules.

### 22a. `/api/schemas` lies about the source-type field name

**Repro:**

```bash
# /api/schemas calls the field `sourceType`:
curl -s -u admin:district \
  'http://localhost:8080/api/schemas/programRuleVariable/?fields=properties[name,propertyType,klass]' \
  | jq '.properties[] | select(.name == "sourceType")'
# { "name": "sourceType", "propertyType": "CONSTANT", "klass": "org...ProgramRuleVariableSourceType" }

# …but posting with that name silently drops the value:
curl -s -u admin:district -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name":"V_X","program":{"id":"eke95YJi9VS"},"sourceType":"DATAELEMENT_CURRENT_EVENT","dataElement":{"id":"DEancVisit1"}}' \
  'http://localhost:8080/api/programRuleVariables'
# 201 Created — but the stored row has sourceType == null.

# Wire format that actually sticks: `programRuleVariableSourceType`.
curl -s -u admin:district -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name":"V_Y","program":{"id":"eke95YJi9VS"},"programRuleVariableSourceType":"DATAELEMENT_CURRENT_EVENT","dataElement":{"id":"DEancVisit1"}}' \
  'http://localhost:8080/api/programRuleVariables'
# Row's programRuleVariableSourceType is now DATAELEMENT_CURRENT_EVENT.
```

**Expected:** the field name reported by `/api/schemas` (`sourceType`) is
what the API accepts on POST/PUT — same as every other resource.

**Actual:** `/api/schemas` lies. Callers have to know the wire format
uses the full property name (`programRuleVariableSourceType`). POSTs
with the schema-reported name silently drop the value instead of
erroring, so bad payloads ship cleanly through CI and only break when
the rule engine evaluates nothing.

Symmetric to `ProgramTrackedEntityAttribute.attribute` vs wire
`trackedEntityAttribute` — same category of schema-vs-wire drift,
same workaround required.

### 22b. `fields=*` silently omits `programRuleVariableSourceType`

**Repro:**

```bash
# Fetch with the "give me everything" selector — source type is missing:
curl -s -u admin:district \
  'http://localhost:8080/api/programRuleVariables/PrvAncCnt01?fields=*' \
  | jq 'keys'
# No "programRuleVariableSourceType" in the output.

# Ask explicitly — it's there:
curl -s -u admin:district \
  'http://localhost:8080/api/programRuleVariables/PrvAncCnt01?fields=id,programRuleVariableSourceType' \
  | jq '.programRuleVariableSourceType'
# "DATAELEMENT_CURRENT_EVENT"
```

**Expected:** `fields=*` expands every stored property, same as every
other metadata endpoint.

**Actual:** `programRuleVariableSourceType` is silently filtered out
of `fields=*` responses. Programmatic callers reading the shape don't
know the rule's source type unless they explicitly name the field.

Same shape as BUGS.md #19 (`/api/validationResults` ignoring
`fields=*` on nested refs).

**Impact (both):** SDK generators reading `/api/schemas` emit a wrong
field name that never writes through, and callers using `fields=*`
for debug dumps miss the single most important configuration field on
each variable. Every integration shipping program rules has to know
the non-discoverable wire names.

**Workaround in this repo:**
`infra/scripts/build_e2e_dump.py::create_program_rules` builds every
variable + action via `pydantic.BaseModel.model_validate({...})` with
the wire field names in the dict (`programRuleVariableSourceType`,
`trackedEntityAttribute`) so the generated model's `extra="allow"`
carries them into the POST payload unchanged. The upcoming
`ProgramRulesAccessor` (PR #63) fetches with an explicit fields
selector naming `programRuleVariableSourceType` so the typed model
sees it.

**Expected upstream fix:**
- `/api/schemas/programRuleVariable` reports the field name the API
  reads (`programRuleVariableSourceType`), or the POST handler accepts
  the schema-reported name (`sourceType`) as an alias.
- `fields=*` on program rule variables returns every stored property,
  including the source type.

**How to know it's fixed:**
- POST `{"sourceType": "DATAELEMENT_CURRENT_EVENT", ...}` stores the
  source type (not silently null-ing it).
- `GET /api/programRuleVariables/<uid>?fields=*` returns
  `programRuleVariableSourceType` in the response body.
