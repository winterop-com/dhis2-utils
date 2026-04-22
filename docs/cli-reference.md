# CLI reference

dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2-core).

**Usage**:

```console
$ dhis2 [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-p, --profile TEXT`: DHIS2 profile name (overrides DHIS2_PROFILE env + TOML default).
* `-d, --debug`: Verbose output on stderr — HTTP method/URL/status/elapsed for every request.
* `--help`: Show this message and exit.

**Commands**:

* `analytics`: DHIS2 analytics queries.
* `browser`: Playwright-driven DHIS2 UI automation.
* `data`: DHIS2 data values (aggregate + tracker).
* `dev`: Developer/operator tools.
* `doctor`: Probe a DHIS2 instance for known gotchas +...
* `files`: Manage DHIS2 documents + file resources.
* `maintenance`: DHIS2 maintenance (tasks, cache,...
* `messaging`: DHIS2 internal messaging.
* `metadata`: DHIS2 metadata inspection.
* `profile`: Manage DHIS2 profiles.
* `route`: DHIS2 integration routes.
* `system`: DHIS2 system info.
* `user`: DHIS2 user administration.
* `user-group`: DHIS2 user-group administration.
* `user-role`: DHIS2 user-role administration.

## `dhis2 analytics`

DHIS2 analytics queries.

**Usage**:

```console
$ dhis2 analytics [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `query`: Run an analytics query.
* `outlier-detection`: Run `/api/analytics/outlierDetection` —...
* `events`: Event analytics — line-lists events or...
* `enrollments`: Enrollment analytics — line-lists...
* `tracked-entities`: Tracked-entity analytics — line-list TEs...

### `dhis2 analytics query`

Run an analytics query. Use `--shape` to pick `table`, `raw`, or `dvs`.

**Usage**:

```console
$ dhis2 analytics query [OPTIONS]
```

**Options**:

* `--dimension, --dim TEXT`: Dimension string (repeatable), e.g. dx:UID, pe:LAST_12_MONTHS, ou:UID.  [required]
* `--shape TEXT`: Response shape: `table` (default, aggregated), `raw` (/api/analytics/rawData), `dvs` (/api/analytics/dataValueSet — DataValueSet shape).  [default: table]
* `--filter TEXT`: Filter string (repeatable), same syntax as --dimension.
* `--agg TEXT`: SUM | AVERAGE | COUNT | MIN | MAX | AVERAGE_SUM_ORG_UNIT ...
* `--output-id-scheme TEXT`: UID | NAME | CODE | ID — how UIDs appear in the response
* `--num-den / --no-num-den`: Include indicator numerator/denominator columns.  [default: no-num-den]
* `--display-property TEXT`: NAME | SHORTNAME — which label to render metadata with.
* `--start-date TEXT`
* `--end-date TEXT`
* `--skip-meta`
* `--help`: Show this message and exit.

### `dhis2 analytics outlier-detection`

Run `/api/analytics/outlierDetection` — flag statistical anomalies in data values.

**Usage**:

```console
$ dhis2 analytics outlier-detection [OPTIONS]
```

**Options**:

* `--data-element, --de TEXT`: Data-element UID (repeatable).
* `--data-set, --ds TEXT`: Data-set UID (repeatable) — expanded to its dataElements.
* `--org-unit, --ou TEXT`: Org-unit UID (repeatable).
* `--period, --pe TEXT`: Period identifier (e.g. LAST_12_MONTHS, 202401).
* `--start-date TEXT`: ISO date YYYY-MM-DD.
* `--end-date TEXT`: ISO date YYYY-MM-DD.
* `--algorithm TEXT`: Z_SCORE (default) | MODIFIED_Z_SCORE | MIN_MAX. (Upstream OAS still shows MOD_Z_SCORE but the server rejects that value — see BUGS.md.)
* `--threshold FLOAT`: Standard-deviation cutoff (default 3.0).
* `--max-results INTEGER`: Cap the number of outliers returned (default 500).
* `--order-by TEXT`: ABS_DEV | STANDARD_DEVIATION | Z_SCORE | ...
* `--sort-order TEXT`: ASC | DESC.
* `--help`: Show this message and exit.

### `dhis2 analytics events`

Event analytics — line-lists events or aggregates them.

**Usage**:

```console
$ dhis2 analytics events [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `query`: Run an event analytics query...

#### `dhis2 analytics events query`

Run an event analytics query (`/api/analytics/events/{mode}/{program}`).

**Usage**:

```console
$ dhis2 analytics events query [OPTIONS] PROGRAM
```

**Arguments**:

* `PROGRAM`: Program UID.  [required]

**Options**:

* `--mode TEXT`: `query` (line-listed events) or `aggregate` (grouped counts).  [default: query]
* `--dimension, --dim TEXT`: Dimension string (repeatable), e.g. pe:LAST_12_MONTHS, ou:UID.
* `--filter TEXT`: Filter string (repeatable), same syntax as --dimension.
* `--stage TEXT`: Program stage UID to narrow events.
* `--output-type TEXT`: EVENT | ENROLLMENT | TRACKED_ENTITY_INSTANCE (row shape).
* `--start-date TEXT`
* `--end-date TEXT`
* `--skip-meta`
* `--page INTEGER`
* `--page-size INTEGER`
* `--help`: Show this message and exit.

### `dhis2 analytics enrollments`

Enrollment analytics — line-lists enrollments.

**Usage**:

```console
$ dhis2 analytics enrollments [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `query`: Run an enrollment analytics query...

#### `dhis2 analytics enrollments query`

Run an enrollment analytics query (`/api/analytics/enrollments/query/{program}`).

**Usage**:

```console
$ dhis2 analytics enrollments query [OPTIONS] PROGRAM
```

**Arguments**:

* `PROGRAM`: Program UID.  [required]

**Options**:

* `--dimension, --dim TEXT`: Dimension string (repeatable).
* `--filter TEXT`: Filter string (repeatable).
* `--start-date TEXT`
* `--end-date TEXT`
* `--skip-meta`
* `--page INTEGER`
* `--page-size INTEGER`
* `--help`: Show this message and exit.

### `dhis2 analytics tracked-entities`

Tracked-entity analytics — line-list TEs for a given type.

**Usage**:

```console
$ dhis2 analytics tracked-entities [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `query`: Line-list tracked entities via...

#### `dhis2 analytics tracked-entities query`

Line-list tracked entities via `/api/analytics/trackedEntities/query/{TET_UID}`.

**Usage**:

```console
$ dhis2 analytics tracked-entities query [OPTIONS] TRACKED_ENTITY_TYPE
```

**Arguments**:

* `TRACKED_ENTITY_TYPE`: TrackedEntityType UID.  [required]

**Options**:

* `--dimension, --dim TEXT`: Dimension string (repeatable).
* `--filter TEXT`: Filter string (repeatable).
* `--program TEXT`: Program UID (repeatable) to narrow results.
* `--start-date TEXT`
* `--end-date TEXT`
* `--ou-mode TEXT`: SELECTED | CHILDREN | DESCENDANTS | ACCESSIBLE | ALL (default SELECTED).
* `--display-property TEXT`: NAME | SHORTNAME.
* `--skip-meta`
* `--skip-data`
* `--include-metadata-details`: Include nested objects in the metaData map.
* `--page INTEGER`
* `--page-size INTEGER`
* `--asc TEXT`: Field to sort ascending (repeatable).
* `--desc TEXT`: Field to sort descending (repeatable).
* `--help`: Show this message and exit.

## `dhis2 browser`

Playwright-driven DHIS2 UI automation.

**Usage**:

```console
$ dhis2 browser [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `pat`: Mint a Personal Access Token V2 via...
* `dashboard`: Dashboard capture workflows.
* `viz`: Visualization capture workflows.
* `map`: Map capture workflows.

### `dhis2 browser pat`

Mint a Personal Access Token V2 via Playwright and print the token value to stdout.

DHIS2 only returns the token value once, at creation — store it somewhere
persistent immediately. Subsequent `GET /api/apiToken/{id}` calls return
metadata but not the secret.

**Usage**:

```console
$ dhis2 browser pat [OPTIONS]
```

**Options**:

* `--url TEXT`: Base URL of the DHIS2 instance.  [required]
* `--username TEXT`: Login username.  [required]
* `--password TEXT`: Login password.  [required]
* `--name TEXT`: Friendly display name for the token.
* `--expires-in-days INTEGER`: Token lifetime in days; omit for no expiry.
* `--allowed-ip TEXT`: CIDR/IP allowlist entry; repeat for multiple.
* `--allowed-method TEXT`: HTTP method allowlist; repeat for each method.
* `--allowed-referrer TEXT`: Referer URL allowlist; repeat for each.
* `--headless / --headful`: Run browser headlessly (default: visible, so you can watch the flow).  [default: headful]
* `--help`: Show this message and exit.

### `dhis2 browser dashboard`

Dashboard capture workflows.

**Usage**:

```console
$ dhis2 browser dashboard [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `screenshot`: Capture full-page PNGs of every DHIS2...

#### `dhis2 browser dashboard screenshot`

Capture full-page PNGs of every DHIS2 dashboard (or just the ones named via --only).

Shares a single Playwright context across dashboards — one login, one
dashboard-app load, then hash-only navigation between dashboards. The
capture loop waits for each item&#x27;s plugin iframe to render substantial
content (canvas / svg / leaflet / highcharts / img / long text) with
a plateau detector so one stuck item doesn&#x27;t stall the batch.

**Usage**:

```console
$ dhis2 browser dashboard screenshot [OPTIONS]
```

**Options**:

* `-o, --output-dir PATH`: Directory for the PNG output. Defaults to `./screenshots`. Each run auto-creates an `{instance-slug}/` subdirectory keyed on the profile&#x27;s base URL so multi-stack captures don&#x27;t overwrite.
* `--only TEXT`: Capture only these dashboard UIDs; repeat for multiple.
* `--headless / --headful`: Run browser headlessly (default: yes — automation-friendly).  [default: headless]
* `--banner / --no-banner`: Prepend an info banner (instance / user / timestamp) to each PNG.  [default: banner]
* `--trim / --no-trim`: Crop uniform-colour edges off the bottom + right of each PNG.  [default: trim]
* `--help`: Show this message and exit.

### `dhis2 browser viz`

Visualization capture workflows.

**Usage**:

```console
$ dhis2 browser viz [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `screenshot`: Capture a PNG of each Visualization (or...

#### `dhis2 browser viz screenshot`

Capture a PNG of each Visualization (or just the UIDs named via --only).

Each capture navigates the DHIS2 Data Visualizer app
(`/dhis-web-data-visualizer/#/&lt;uid&gt;`) inside a shared Playwright
context — one login, one app-shell load, hash-only navigation
between vizes. Renders wait for the chart to materialise (SVG /
canvas / pivot table / long text) with a plateau detector so one
stuck viz doesn&#x27;t stall the batch.

DHIS2 has no native `/api/visualizations/{uid}.png` endpoint, so
every PNG goes through Chromium. Install the extra via
`uv add &#x27;dhis2-cli&#x27;` + `playwright install
chromium` first.

**Usage**:

```console
$ dhis2 browser viz screenshot [OPTIONS]
```

**Options**:

* `-o, --output-dir PATH`: Directory for the PNG output. Defaults to `./screenshots`. Each run auto-creates an `{instance-slug}/` subdirectory keyed on the profile&#x27;s base URL so multi-stack captures don&#x27;t overwrite.
* `--only TEXT`: Capture only these Visualization UIDs; repeat for multiple.
* `--headless / --headful`: Run browser headlessly (default: yes — automation-friendly).  [default: headless]
* `--banner / --no-banner`: Prepend an info banner (name / type / instance / user / timestamp) to each PNG.  [default: banner]
* `--trim / --no-trim`: Crop uniform-colour edges off the bottom + right of each PNG.  [default: trim]
* `--help`: Show this message and exit.

### `dhis2 browser map`

Map capture workflows.

**Usage**:

```console
$ dhis2 browser map [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `screenshot`: Capture a PNG of each Map (or the UIDs...

#### `dhis2 browser map screenshot`

Capture a PNG of each Map (or the UIDs named via --only).

Navigates the DHIS2 Maps app (`/dhis-web-maps/#/&lt;uid&gt;`) in a shared
Playwright context — one login, one app-shell load, hash-nav between
maps. Waits for MapLibre canvas + vector overlays to render before
snapping. Requires the `` extra (install with
`uv add &#x27;dhis2-cli&#x27;` + `playwright install chromium`).

**Usage**:

```console
$ dhis2 browser map screenshot [OPTIONS]
```

**Options**:

* `-o, --output-dir PATH`: Directory for the PNG output. Defaults to `./screenshots`. Each run auto-creates an `{instance-slug}/` subdirectory keyed on the profile&#x27;s base URL so multi-stack captures don&#x27;t overwrite.
* `--only TEXT`: Capture only these Map UIDs; repeat for multiple.
* `--headless / --headful`: Run browser headlessly (default: yes — automation-friendly).  [default: headless]
* `--banner / --no-banner`: Prepend an info banner (name / layer count / instance / user / timestamp) to each PNG.  [default: banner]
* `--trim / --no-trim`: Crop uniform-colour edges off the bottom + right of each PNG.  [default: trim]
* `--help`: Show this message and exit.

## `dhis2 data`

DHIS2 data values (aggregate + tracker).

**Usage**:

```console
$ dhis2 data [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `aggregate`: Aggregate data values (dataValueSets).
* `tracker`: Tracker (entities, enrollments, events,...

### `dhis2 data aggregate`

Aggregate data values (dataValueSets).

**Usage**:

```console
$ dhis2 data aggregate [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Fetch a data value set.
* `push`: Bulk push data values from a JSON file.
* `set`: Set a single data value.
* `delete`: Delete a single data value.

#### `dhis2 data aggregate get`

Fetch a data value set.

**Usage**:

```console
$ dhis2 data aggregate get [OPTIONS]
```

**Options**:

* `--data-set TEXT`: DataSet UID.
* `--period TEXT`: Period (e.g. 202401, 2024W12, 2024).
* `--start-date TEXT`: ISO date (YYYY-MM-DD).
* `--end-date TEXT`: ISO date (YYYY-MM-DD).
* `--org-unit TEXT`: OrganisationUnit UID.
* `--children`: Include descendants of org_unit.
* `--data-element-group, --deg TEXT`: DataElementGroup UID (narrows to its member DEs).
* `--limit INTEGER`: Max rows to include in output.
* `--json`: Emit raw DataValueSet JSON.
* `--help`: Show this message and exit.

#### `dhis2 data aggregate push`

Bulk push data values from a JSON file.

**Usage**:

```console
$ dhis2 data aggregate push [OPTIONS] FILE
```

**Arguments**:

* `FILE`: Path to a JSON file containing a dataValues array or envelope.  [required]

**Options**:

* `--data-set TEXT`
* `--period TEXT`
* `--org-unit TEXT`
* `--dry-run`
* `--strategy TEXT`: CREATE | UPDATE | CREATE_AND_UPDATE | DELETE
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 data aggregate set`

Set a single data value.

**Usage**:

```console
$ dhis2 data aggregate set [OPTIONS]
```

**Options**:

* `--data-element, --de TEXT`: DataElement UID.  [required]
* `--period, --pe TEXT`: Period (e.g. 202401).  [required]
* `--org-unit, --ou TEXT`: OrganisationUnit UID.  [required]
* `--value TEXT`: The value to set (as a string).  [required]
* `--coc TEXT`: CategoryOptionCombo UID.
* `--aoc TEXT`: AttributeOptionCombo UID (category-combo attributes).
* `--comment TEXT`
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 data aggregate delete`

Delete a single data value.

**Usage**:

```console
$ dhis2 data aggregate delete [OPTIONS]
```

**Options**:

* `--data-element, --de TEXT`: [required]
* `--period, --pe TEXT`: [required]
* `--org-unit, --ou TEXT`: [required]
* `--coc TEXT`
* `--aoc TEXT`
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 data tracker`

Tracker (entities, enrollments, events, relationships).

**Usage**:

```console
$ dhis2 data tracker [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List tracked entities of the given...
* `list`: List tracked entities of the given...
* `get`: Fetch one tracked entity by UID...
* `type`: List every configured TrackedEntityType on...
* `push`: Bulk import via POST /api/tracker.
* `enrollment`: Enrollments.
* `event`: Events.
* `relationship`: Relationships.

#### `dhis2 data tracker ls`

List tracked entities of the given TrackedEntityType (name or UID).

**Usage**:

```console
$ dhis2 data tracker ls [OPTIONS] TYPE
```

**Arguments**:

* `TYPE`: TrackedEntityType name (case-insensitive) or UID — e.g. &#x27;Person&#x27;, &#x27;Patient&#x27;, or &#x27;tet01234567&#x27;.  [required]

**Options**:

* `--program TEXT`: Optional program UID to further scope the listing.
* `--te-uids TEXT`: Comma-separated tracked-entity UIDs to fetch directly.
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--fields TEXT`
* `--filter TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`: 1-based page number.
* `--updated-after TEXT`: ISO-8601 cutoff — only entities updated after this.
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 data tracker list`

List tracked entities of the given TrackedEntityType (name or UID).

**Usage**:

```console
$ dhis2 data tracker list [OPTIONS] TYPE
```

**Arguments**:

* `TYPE`: TrackedEntityType name (case-insensitive) or UID — e.g. &#x27;Person&#x27;, &#x27;Patient&#x27;, or &#x27;tet01234567&#x27;.  [required]

**Options**:

* `--program TEXT`: Optional program UID to further scope the listing.
* `--te-uids TEXT`: Comma-separated tracked-entity UIDs to fetch directly.
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--fields TEXT`
* `--filter TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`: 1-based page number.
* `--updated-after TEXT`: ISO-8601 cutoff — only entities updated after this.
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 data tracker get`

Fetch one tracked entity by UID (TrackedEntityType inferred from the entity).

**Usage**:

```console
$ dhis2 data tracker get [OPTIONS] UID
```

**Arguments**:

* `UID`: Tracked entity UID.  [required]

**Options**:

* `--program TEXT`
* `--fields TEXT`
* `--json`: Emit the raw entity payload.
* `--help`: Show this message and exit.

#### `dhis2 data tracker type`

List every configured TrackedEntityType on the connected instance (name + UID).

The `list` and `get` commands accept either a name or a UID in their `&lt;type&gt;`
positional — run this first to see what&#x27;s configured.

**Usage**:

```console
$ dhis2 data tracker type [OPTIONS]
```

**Options**:

* `--json`: Emit the raw list.
* `--help`: Show this message and exit.

#### `dhis2 data tracker push`

Bulk import via POST /api/tracker.

**Usage**:

```console
$ dhis2 data tracker push [OPTIONS] FILE
```

**Arguments**:

* `FILE`: JSON file containing the tracker bundle.  [required]

**Options**:

* `--strategy TEXT`: CREATE | UPDATE | CREATE_AND_UPDATE | DELETE
* `--atomic TEXT`: ALL | OBJECT
* `--dry-run`
* `--async`
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 data tracker enrollment`

Enrollments.

**Usage**:

```console
$ dhis2 data tracker enrollment [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List enrollments (tracker programs only).
* `list`: List enrollments (tracker programs only).

##### `dhis2 data tracker enrollment ls`

List enrollments (tracker programs only).

**Usage**:

```console
$ dhis2 data tracker enrollment ls [OPTIONS]
```

**Options**:

* `--program TEXT`
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--te TEXT`
* `--status TEXT`: ACTIVE | COMPLETED | CANCELLED
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`
* `--updated-after TEXT`
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

##### `dhis2 data tracker enrollment list`

List enrollments (tracker programs only).

**Usage**:

```console
$ dhis2 data tracker enrollment list [OPTIONS]
```

**Options**:

* `--program TEXT`
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--te TEXT`
* `--status TEXT`: ACTIVE | COMPLETED | CANCELLED
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`
* `--updated-after TEXT`
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 data tracker event`

Events.

**Usage**:

```console
$ dhis2 data tracker event [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List events (works with both event and...
* `list`: List events (works with both event and...

##### `dhis2 data tracker event ls`

List events (works with both event and tracker programs).

**Usage**:

```console
$ dhis2 data tracker event ls [OPTIONS]
```

**Options**:

* `--program TEXT`
* `--program-stage TEXT`
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--te TEXT`
* `--enrollment TEXT`
* `--status TEXT`
* `--after TEXT`
* `--before TEXT`
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

##### `dhis2 data tracker event list`

List events (works with both event and tracker programs).

**Usage**:

```console
$ dhis2 data tracker event list [OPTIONS]
```

**Options**:

* `--program TEXT`
* `--program-stage TEXT`
* `--org-unit TEXT`
* `--ou-mode TEXT`: [default: DESCENDANTS]
* `--te TEXT`
* `--enrollment TEXT`
* `--status TEXT`
* `--after TEXT`
* `--before TEXT`
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--page INTEGER`
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 data tracker relationship`

Relationships.

**Usage**:

```console
$ dhis2 data tracker relationship [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List relationships (one of...
* `list`: List relationships (one of...

##### `dhis2 data tracker relationship ls`

List relationships (one of --te/--enrollment/--event required).

**Usage**:

```console
$ dhis2 data tracker relationship ls [OPTIONS]
```

**Options**:

* `--te TEXT`
* `--enrollment TEXT`
* `--event TEXT`
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

##### `dhis2 data tracker relationship list`

List relationships (one of --te/--enrollment/--event required).

**Usage**:

```console
$ dhis2 data tracker relationship list [OPTIONS]
```

**Options**:

* `--te TEXT`
* `--enrollment TEXT`
* `--event TEXT`
* `--fields TEXT`
* `--page-size INTEGER`: [default: 50]
* `--json`: Emit the raw list instead of a table.
* `--help`: Show this message and exit.

## `dhis2 dev`

Developer/operator tools.

**Usage**:

```console
$ dhis2 dev [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `codegen`: Generate version-aware DHIS2 client code...
* `uid`: Generate 11-char DHIS2 UIDs.
* `pat`: Personal Access Tokens — provision PATs on...
* `oauth2`: Manage DHIS2 OAuth2 clients on the server...
* `sample`: Inject known-good fixtures to verify the...
* `customize`: Brand + theme a DHIS2 instance (logos,...

### `dhis2 dev codegen`

Generate version-aware DHIS2 client code from /api/schemas.

**Usage**:

```console
$ dhis2 dev codegen [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate the client for the DHIS2 version...
* `rebuild`: Regenerate the client from saved...
* `oas-rebuild`: Emit OpenAPI-derived pydantic models into...

#### `dhis2 dev codegen generate`

Generate the client for the DHIS2 version reported by `--url`.

**Usage**:

```console
$ dhis2 dev codegen generate [OPTIONS]
```

**Options**:

* `--url TEXT`: Base URL of the DHIS2 instance.  [required]
* `--username TEXT`: Basic-auth username.
* `--password TEXT`: Basic-auth password.
* `--pat TEXT`: Personal Access Token.
* `--output-root PATH`: Directory containing versioned subfolders; defaults to dhis2-client&#x27;s generated/ folder.
* `--help`: Show this message and exit.

#### `dhis2 dev codegen rebuild`

Regenerate the client from saved schemas_manifest.json files (no network).

Useful after touching emit.py / templates when you want every committed
version refreshed without spinning up a live DHIS2 for each. If `--manifest`
is omitted, walks the output root and rebuilds each version whose
schemas_manifest.json is checked in.

**Usage**:

```console
$ dhis2 dev codegen rebuild [OPTIONS]
```

**Options**:

* `--manifest PATH`: Path to a committed schemas_manifest.json. Defaults to every version under the generated root.
* `--output-root PATH`: Directory of versioned subfolders; defaults to dhis2-client generated/.
* `--help`: Show this message and exit.

#### `dhis2 dev codegen oas-rebuild`

Emit OpenAPI-derived pydantic models into `generated/v{N}/oas/`.

Reads the committed `openapi.json` + `schemas_manifest.json` from each
version directory (no network). Output lands alongside the `/api/schemas`
emitter&#x27;s output under `schemas/`.

**Usage**:

```console
$ dhis2 dev codegen oas-rebuild [OPTIONS]
```

**Options**:

* `--version TEXT`: Version key (e.g. v42). Defaults to every committed version.
* `--output-root PATH`: Directory of versioned subfolders; defaults to dhis2-client generated/.
* `--help`: Show this message and exit.

### `dhis2 dev uid`

Generate 11-char DHIS2 UIDs.

**Usage**:

```console
$ dhis2 dev uid [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-n, --count INTEGER RANGE`: How many UIDs to generate.  [default: 1; 1&lt;=x&lt;=10000]
* `--help`: Show this message and exit.

### `dhis2 dev pat`

Personal Access Tokens — provision PATs on DHIS2.

**Usage**:

```console
$ dhis2 dev pat [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a DHIS2 Personal Access Token via...

#### `dhis2 dev pat create`

Create a DHIS2 Personal Access Token via POST /api/apiToken.

Admin creds come from env or prompt (never argv). The PAT value is only
returned once by DHIS2 — capture it here and pipe into a profile:

    export DHIS2_PAT=$(dhis2 dev pat create --url $URL -q)
    dhis2 profile add local --url $URL --auth pat

Or use `dhis2 profile bootstrap --auth pat` for a one-shot setup.

**Usage**:

```console
$ dhis2 dev pat create [OPTIONS]
```

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`
* `--description TEXT`
* `--expires-in-days INTEGER`
* `--allowed-ip TEXT`: IP allowlist entry; repeat for multiple.
* `--allowed-method TEXT`: HTTP method allowlist; repeat for each method.
* `--allowed-referrer TEXT`: Referer allowlist entry; repeat for multiple.
* `-q, --quiet`: Print only the PAT value, suitable for $(command substitution).
* `--help`: Show this message and exit.

### `dhis2 dev oauth2`

Manage DHIS2 OAuth2 clients on the server (admin ops).

**Usage**:

```console
$ dhis2 dev oauth2 [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `client`: OAuth2 client registrations at...

#### `dhis2 dev oauth2 client`

OAuth2 client registrations at /api/oAuth2Clients.

**Usage**:

```console
$ dhis2 dev oauth2 client [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `register`: Register an OAuth2 client on DHIS2 via...

##### `dhis2 dev oauth2 client register`

Register an OAuth2 client on DHIS2 via POST /api/oAuth2Clients.

Secrets (admin credentials, client_secret) come from env or interactive
prompt — never argv.

Prints `client_id` + metadata UID so they can be piped into
`dhis2 profile add --auth oauth2 ...`. For a one-shot bootstrap (register
+ save profile + log in) use `dhis2 profile bootstrap` instead.

**Usage**:

```console
$ dhis2 dev oauth2 client register [OPTIONS]
```

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`
* `--client-id TEXT`: [default: dhis2-utils-local]
* `--redirect-uri TEXT`: [default: http://localhost:8765]
* `--scope TEXT`: [default: ALL]
* `--name TEXT`
* `--help`: Show this message and exit.

### `dhis2 dev sample`

Inject known-good fixtures to verify the stack end-to-end (route, data, pat, oauth2-client).

**Usage**:

```console
$ dhis2 dev sample [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `route`: Create a sample route, run it, and (unless...
* `pat`: Create a sample PAT, use it to call...
* `data-value`: Write a sample data value, read it back,...
* `oauth2-client`: Create a sample OAuth2 client on DHIS2,...
* `all`: Run every sample in sequence — route,...

#### `dhis2 dev sample route`

Create a sample route, run it, and (unless --keep) delete it.

Verifies the full /api/routes lifecycle end-to-end: create -&gt; run (proxy
to target URL) -&gt; delete.

**Usage**:

```console
$ dhis2 dev sample route [OPTIONS]
```

**Options**:

* `--url TEXT`: URL the sample route will proxy to.  [default: https://httpbin.org/get]
* `--code TEXT`: [default: SMOKE_ROUTE]
* `--keep`: Don&#x27;t delete the sample route afterwards.
* `--help`: Show this message and exit.

#### `dhis2 dev sample pat`

Create a sample PAT, use it to call /api/me, then (unless --keep) delete it.

**Usage**:

```console
$ dhis2 dev sample pat [OPTIONS]
```

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`
* `--keep`: Don&#x27;t delete the sample PAT afterwards.
* `--help`: Show this message and exit.

#### `dhis2 dev sample data-value`

Write a sample data value, read it back, and (unless --keep) delete it.

Uses the seeded BfMAe6Itzgt (Child Health) fixture by default — override with --de/--ou/--pe
for other scopes.

**Usage**:

```console
$ dhis2 dev sample data-value [OPTIONS]
```

**Options**:

* `--de TEXT`: DataElement UID.  [default: DEancVisit1]
* `--ou TEXT`: OrganisationUnit UID.  [default: NOROsloProv]
* `--pe TEXT`: Period (e.g. 202603).  [default: 202603]
* `--value TEXT`: [default: 42]
* `--keep`: Don&#x27;t delete the sample data value afterwards.
* `--help`: Show this message and exit.

#### `dhis2 dev sample oauth2-client`

Create a sample OAuth2 client on DHIS2, verify it persisted, then (unless --keep) delete it.

Lifecycle: POST /api/oAuth2Clients -&gt; GET /api/oAuth2Clients/{uid}
-&gt; DELETE /api/oAuth2Clients/{uid}. The admin user is the owner DHIS2
records on the client; no user-impersonation happens.

**Usage**:

```console
$ dhis2 dev sample oauth2-client [OPTIONS]
```

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`
* `--client-id TEXT`: OAuth2 client_id; default = smoke-&lt;epoch&gt;.
* `--keep`: Don&#x27;t delete the sample OAuth2 client afterwards.
* `--help`: Show this message and exit.

#### `dhis2 dev sample all`

Run every sample in sequence — route, data-value, pat, oauth2-client.

**Usage**:

```console
$ dhis2 dev sample all [OPTIONS]
```

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`
* `--keep`: Don&#x27;t delete the fixtures afterwards.
* `--help`: Show this message and exit.

### `dhis2 dev customize`

Brand + theme a DHIS2 instance (logos, copy, CSS).

**Usage**:

```console
$ dhis2 dev customize [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `logo-front`: Upload the login-page splash / upper-right...
* `logo-banner`: Upload the top-menu banner logo (appears...
* `style`: Upload a CSS stylesheet that DHIS2 serves...
* `set`: Set a single system setting.
* `settings`: Bulk-set system settings from a JSON file.
* `apply`: Apply a committed preset directory in one...
* `show`: Show DHIS2&#x27;s current `/api/loginConfig`...

#### `dhis2 dev customize logo-front`

Upload the login-page splash / upper-right logo.

**Usage**:

```console
$ dhis2 dev customize logo-front [OPTIONS] FILE
```

**Arguments**:

* `FILE`: PNG/JPG/SVG to upload as the login splash logo.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize logo-banner`

Upload the top-menu banner logo (appears on every authenticated page).

**Usage**:

```console
$ dhis2 dev customize logo-banner [OPTIONS] FILE
```

**Arguments**:

* `FILE`: PNG/JPG/SVG to upload as the top-menu banner.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize style`

Upload a CSS stylesheet that DHIS2 serves on every authenticated page.

NOTE: DHIS2&#x27;s standalone login app (`/dhis-web-login/`) does NOT include this
stylesheet. Post-auth pages do.

**Usage**:

```console
$ dhis2 dev customize style [OPTIONS] FILE
```

**Arguments**:

* `FILE`: CSS file to upload as `/api/files/style`.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize set`

Set a single system setting.

**Usage**:

```console
$ dhis2 dev customize set [OPTIONS] KEY VALUE
```

**Arguments**:

* `KEY`: System setting key (e.g. applicationTitle, keyApplicationFooter).  [required]
* `VALUE`: New value.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize settings`

Bulk-set system settings from a JSON file.

**Usage**:

```console
$ dhis2 dev customize settings [OPTIONS] FILE
```

**Arguments**:

* `FILE`: JSON file containing a {key: value} object.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize apply`

Apply a committed preset directory in one call (skips files that don&#x27;t exist).

**Usage**:

```console
$ dhis2 dev customize apply [OPTIONS] DIRECTORY
```

**Arguments**:

* `DIRECTORY`: Directory containing optional logo_front.png, logo_banner.png, style.css, preset.json.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 dev customize show`

Show DHIS2&#x27;s current `/api/loginConfig` snapshot (what the login app sees).

**Usage**:

```console
$ dhis2 dev customize show [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON instead of a readable dump.
* `--help`: Show this message and exit.

## `dhis2 doctor`

Probe a DHIS2 instance for known gotchas + requirements.

**Usage**:

```console
$ dhis2 doctor [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--all`: Run every category (metadata + integrity + bugs).
* `--json`: Emit the report as JSON instead of a table.
* `--help`: Show this message and exit.

**Commands**:

* `metadata`: Run workspace metadata-health probes only...
* `integrity`: Run DHIS2&#x27;s own...
* `bugs`: Run BUGS.md workaround drift detection...

### `dhis2 doctor metadata`

Run workspace metadata-health probes only (data sets without DEs, programs without stages, ...).

**Usage**:

```console
$ dhis2 doctor metadata [OPTIONS]
```

**Options**:

* `--json`: Emit the report as JSON.
* `--help`: Show this message and exit.

### `dhis2 doctor integrity`

Run DHIS2&#x27;s own `/api/dataIntegrity/summary` and surface each check as a probe.

**Usage**:

```console
$ dhis2 doctor integrity [OPTIONS]
```

**Options**:

* `--json`: Emit the report as JSON.
* `--help`: Show this message and exit.

### `dhis2 doctor bugs`

Run BUGS.md workaround drift detection (workspace maintenance, not operator-facing).

**Usage**:

```console
$ dhis2 doctor bugs [OPTIONS]
```

**Options**:

* `--json`: Emit the report as JSON.
* `--help`: Show this message and exit.

## `dhis2 files`

Manage DHIS2 documents + file resources.

**Usage**:

```console
$ dhis2 files [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `documents`: Documents (/api/documents).
* `resources`: File resources (/api/fileResources).

### `dhis2 files documents`

Documents (/api/documents).

**Usage**:

```console
$ dhis2 files documents [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List documents — external URL links and...
* `list`: List documents — external URL links and...
* `get`: Show metadata for one document.
* `upload`: Upload a binary document — prints the new...
* `upload-url`: Create an EXTERNAL_URL document — no bytes...
* `download`: Download the binary payload to `destination`.
* `delete`: Delete one document.

#### `dhis2 files documents ls`

List documents — external URL links and UPLOAD_FILE blobs.

For UPLOAD_FILE docs the backing blob lives in `/api/fileResources/{uid}`
where `{uid}` is `Document.url` (DHIS2 reuses the `url` field as the FR
pointer). Pass `--details` to pull each fileResource&#x27;s `contentType`,
`contentLength`, and `storageStatus` inline.

**Usage**:

```console
$ dhis2 files documents ls [OPTIONS]
```

**Options**:

* `--filter TEXT`: DHIS2 filter, e.g. `name:like:Annual`.
* `--page INTEGER`: 1-indexed page number.
* `--page-size INTEGER`: Rows per page (default 50).
* `--details`: For each UPLOAD_FILE, also fetch the backing fileResource&#x27;s contentType / size / storageStatus (one extra request per row).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 files documents list`

List documents — external URL links and UPLOAD_FILE blobs.

For UPLOAD_FILE docs the backing blob lives in `/api/fileResources/{uid}`
where `{uid}` is `Document.url` (DHIS2 reuses the `url` field as the FR
pointer). Pass `--details` to pull each fileResource&#x27;s `contentType`,
`contentLength`, and `storageStatus` inline.

**Usage**:

```console
$ dhis2 files documents list [OPTIONS]
```

**Options**:

* `--filter TEXT`: DHIS2 filter, e.g. `name:like:Annual`.
* `--page INTEGER`: 1-indexed page number.
* `--page-size INTEGER`: Rows per page (default 50).
* `--details`: For each UPLOAD_FILE, also fetch the backing fileResource&#x27;s contentType / size / storageStatus (one extra request per row).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 files documents get`

Show metadata for one document.

**Usage**:

```console
$ dhis2 files documents get [OPTIONS] UID
```

**Arguments**:

* `UID`: Document UID.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 files documents upload`

Upload a binary document — prints the new UID.

**Usage**:

```console
$ dhis2 files documents upload [OPTIONS] FILE
```

**Arguments**:

* `FILE`: File to upload.  [required]

**Options**:

* `--name TEXT`: Document name (defaults to filename).
* `--help`: Show this message and exit.

#### `dhis2 files documents upload-url`

Create an EXTERNAL_URL document — no bytes uploaded; DHIS2 links out to `url`.

**Usage**:

```console
$ dhis2 files documents upload-url [OPTIONS] NAME URL
```

**Arguments**:

* `NAME`: Document display name.  [required]
* `URL`: External URL DHIS2 will link to.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 files documents download`

Download the binary payload to `destination`.

**Usage**:

```console
$ dhis2 files documents download [OPTIONS] UID DESTINATION
```

**Arguments**:

* `UID`: Document UID.  [required]
* `DESTINATION`: Output file path.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 files documents delete`

Delete one document.

**Usage**:

```console
$ dhis2 files documents delete [OPTIONS] UID
```

**Arguments**:

* `UID`: Document UID.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 files resources`

File resources (/api/fileResources).

**Usage**:

```console
$ dhis2 files resources [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `upload`: Upload a file resource; prints the new UID...
* `get`: Show metadata for one file resource.
* `download`: Download the file-resource payload to...

#### `dhis2 files resources upload`

Upload a file resource; prints the new UID (reference it from the owning metadata object).

**Usage**:

```console
$ dhis2 files resources upload [OPTIONS] FILE
```

**Arguments**:

* `FILE`: File to upload as a fileResource.  [required]

**Options**:

* `--domain [data_value|push_analysis|document|message_attachment|user_avatar|org_unit|icon|job_data]`: FileResource domain (DATA_VALUE, ICON, MESSAGE_ATTACHMENT, ...).  [default: DATA_VALUE]
* `--help`: Show this message and exit.

#### `dhis2 files resources get`

Show metadata for one file resource.

**Usage**:

```console
$ dhis2 files resources get [OPTIONS] UID
```

**Arguments**:

* `UID`: FileResource UID.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 files resources download`

Download the file-resource payload to `destination`.

**Usage**:

```console
$ dhis2 files resources download [OPTIONS] UID DESTINATION
```

**Arguments**:

* `UID`: FileResource UID.  [required]
* `DESTINATION`: Output file path.  [required]

**Options**:

* `--help`: Show this message and exit.

## `dhis2 maintenance`

DHIS2 maintenance (tasks, cache, integrity, cleanup, refresh).

**Usage**:

```console
$ dhis2 maintenance [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cache`: Clear every server-side cache (Hibernate +...
* `task`: Background-task polling (all long-running...
* `cleanup`: Hard-remove soft-deleted rows (unblocks...
* `dataintegrity`: DHIS2 data-integrity checks.
* `refresh`: Regenerate analytics / resource /...
* `validation`: Run validation rules + inspect violations...
* `predictors`: Run predictor expressions (CRUD on...

### `dhis2 maintenance cache`

Clear every server-side cache (Hibernate + app caches).

**Usage**:

```console
$ dhis2 maintenance cache [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `dhis2 maintenance task`

Background-task polling (all long-running DHIS2 ops).

**Usage**:

```console
$ dhis2 maintenance task [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `types`: List every background-job type DHIS2...
* `ls`: List every task UID recorded for a given...
* `list`: List every task UID recorded for a given...
* `status`: Print every notification emitted by a...
* `watch`: Poll a task until it reports...

#### `dhis2 maintenance task types`

List every background-job type DHIS2 tracks (ANALYTICS_TABLE, DATA_INTEGRITY, ...).

**Usage**:

```console
$ dhis2 maintenance task types [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance task ls`

List every task UID recorded for a given job type.

**Usage**:

```console
$ dhis2 maintenance task ls [OPTIONS] TASK_TYPE
```

**Arguments**:

* `TASK_TYPE`: Task type, e.g. ANALYTICS_TABLE.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance task list`

List every task UID recorded for a given job type.

**Usage**:

```console
$ dhis2 maintenance task list [OPTIONS] TASK_TYPE
```

**Arguments**:

* `TASK_TYPE`: Task type, e.g. ANALYTICS_TABLE.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance task status`

Print every notification emitted by a task, oldest first.

**Usage**:

```console
$ dhis2 maintenance task status [OPTIONS] TASK_TYPE TASK_UID
```

**Arguments**:

* `TASK_TYPE`: Task type, e.g. ANALYTICS_TABLE.  [required]
* `TASK_UID`: Task UID returned by the async POST.  [required]

**Options**:

* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 maintenance task watch`

Poll a task until it reports `completed=true`, streaming each new notification.

**Usage**:

```console
$ dhis2 maintenance task watch [OPTIONS] TASK_TYPE TASK_UID
```

**Arguments**:

* `TASK_TYPE`: Task type, e.g. DATA_INTEGRITY.  [required]
* `TASK_UID`: Task UID returned by the async POST.  [required]

**Options**:

* `--interval FLOAT`: Poll interval in seconds.  [default: 2.0]
* `--timeout FLOAT`: Abort after N seconds (default 600).  [default: 600.0]
* `--help`: Show this message and exit.

### `dhis2 maintenance cleanup`

Hard-remove soft-deleted rows (unblocks metadata deletion).

**Usage**:

```console
$ dhis2 maintenance cleanup [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `data-values`: Hard-remove soft-deleted data values from...
* `events`: Hard-remove soft-deleted tracker events.
* `enrollments`: Hard-remove soft-deleted tracker enrollments.
* `tracked-entities`: Hard-remove soft-deleted tracked entities.

#### `dhis2 maintenance cleanup data-values`

Hard-remove soft-deleted data values from `/api/dataValueSets` imports.

**Usage**:

```console
$ dhis2 maintenance cleanup data-values [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance cleanup events`

Hard-remove soft-deleted tracker events.

**Usage**:

```console
$ dhis2 maintenance cleanup events [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance cleanup enrollments`

Hard-remove soft-deleted tracker enrollments.

**Usage**:

```console
$ dhis2 maintenance cleanup enrollments [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance cleanup tracked-entities`

Hard-remove soft-deleted tracked entities.

**Usage**:

```console
$ dhis2 maintenance cleanup tracked-entities [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `dhis2 maintenance dataintegrity`

DHIS2 data-integrity checks.

**Usage**:

```console
$ dhis2 maintenance dataintegrity [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every built-in data-integrity check...
* `list`: List every built-in data-integrity check...
* `run`: Kick off a data-integrity run; with...
* `result`: Read the stored result of a completed...

#### `dhis2 maintenance dataintegrity ls`

List every built-in data-integrity check (name, section, severity).

**Usage**:

```console
$ dhis2 maintenance dataintegrity ls [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 maintenance dataintegrity list`

List every built-in data-integrity check (name, section, severity).

**Usage**:

```console
$ dhis2 maintenance dataintegrity list [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 maintenance dataintegrity run`

Kick off a data-integrity run; with --watch, stream progress to completion.

**Usage**:

```console
$ dhis2 maintenance dataintegrity run [OPTIONS] [CHECK]...
```

**Arguments**:

* `[CHECK]...`: Check name(s); omit to run every check.

**Options**:

* `--details`: Hit /details (populates issues[]) instead of /summary.
* `--slow`: Include the ~19 `isSlow` checks DHIS2 skips by default. Resolves the full check list via /api/dataIntegrity and passes every name explicitly — DHIS2 only runs a slow check when it&#x27;s named in the `checks` filter.
* `-w, --watch`: After kicking off the job, poll /api/system/tasks until it reports completed=true.
* `--interval FLOAT`: Poll interval in seconds when --watch is set.  [default: 2.0]
* `--timeout FLOAT`: Abort polling after N seconds (default 600).  [default: 600.0]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 maintenance dataintegrity result`

Read the stored result of a completed data-integrity run (summary or details mode).

**Usage**:

```console
$ dhis2 maintenance dataintegrity result [OPTIONS] [CHECK]...
```

**Arguments**:

* `[CHECK]...`: Check name(s) to read; omit for all.

**Options**:

* `--details`: Hit /details (issues[]) instead of /summary (count only).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 maintenance refresh`

Regenerate analytics / resource / monitoring backing tables.

**Usage**:

```console
$ dhis2 maintenance refresh [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `analytics`: Regenerate the full analytics star schema...
* `resource-tables`: Regenerate resource tables only...
* `monitoring`: Regenerate monitoring tables...

#### `dhis2 maintenance refresh analytics`

Regenerate the full analytics star schema (`/api/resourceTables/analytics`, job=`ANALYTICS_TABLE`).

Primary workflow after pushing new data values: DHIS2&#x27;s analytics queries
read from these tables, so they must be rebuilt for fresh data to show up.
Also refreshes resource tables unless `--skip-resource-tables` is set.

**Usage**:

```console
$ dhis2 maintenance refresh analytics [OPTIONS]
```

**Options**:

* `--last-years INTEGER`
* `--skip-resource-tables`
* `-w, --watch`: After kicking off the job, poll /api/system/tasks until it reports completed=true.
* `--interval FLOAT`: Poll interval in seconds when --watch is set.  [default: 2.0]
* `--timeout FLOAT`: Abort polling after N seconds (default 600).  [default: 600.0]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 maintenance refresh resource-tables`

Regenerate resource tables only (`/api/resourceTables`, job=`RESOURCE_TABLE`).

Rebuilds the supporting OU / category hierarchy tables without touching
the analytics star schema. Use when OU / category metadata changed but
no new data values landed — faster than a full `refresh analytics` run.

**Usage**:

```console
$ dhis2 maintenance refresh resource-tables [OPTIONS]
```

**Options**:

* `-w, --watch`: After kicking off the job, poll /api/system/tasks until it reports completed=true.
* `--interval FLOAT`: Poll interval in seconds when --watch is set.  [default: 2.0]
* `--timeout FLOAT`: Abort polling after N seconds (default 600).  [default: 600.0]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

#### `dhis2 maintenance refresh monitoring`

Regenerate monitoring tables (`/api/resourceTables/monitoring`, job=`MONITORING`).

Rebuilds the tables backing DHIS2&#x27;s data-quality / validation-rule
monitoring. Independent of the analytics + resource tables.

**Usage**:

```console
$ dhis2 maintenance refresh monitoring [OPTIONS]
```

**Options**:

* `-w, --watch`: After kicking off the job, poll /api/system/tasks until it reports completed=true.
* `--interval FLOAT`: Poll interval in seconds when --watch is set.  [default: 2.0]
* `--timeout FLOAT`: Abort polling after N seconds (default 600).  [default: 600.0]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 maintenance validation`

Run validation rules + inspect violations (CRUD on rules: `dhis2 metadata list validationRules`).

**Usage**:

```console
$ dhis2 maintenance validation [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run`: Run a validation-rule analysis + render...
* `send-notifications`: Fire configured notification templates for...
* `validate-expression`: Parse-check an expression + render a human...
* `result`: List / get / delete persisted validation...

#### `dhis2 maintenance validation run`

Run a validation-rule analysis + render the violations.

**Usage**:

```console
$ dhis2 maintenance validation run [OPTIONS] ORG_UNIT
```

**Arguments**:

* `ORG_UNIT`: Org-unit UID to evaluate rules under (DHIS2 walks the sub-tree).  [required]

**Options**:

* `--start-date TEXT`: Period start, YYYY-MM-DD.  [required]
* `--end-date TEXT`: Period end, YYYY-MM-DD.  [required]
* `--group TEXT`: ValidationRuleGroup UID to narrow the rules evaluated.
* `--max-results INTEGER`: Cap on violations returned (DHIS2 default ~500).
* `--notification`: Fire configured notification templates for each triggered rule.
* `--persist`: Write violations into `/api/validationResults` (otherwise ephemeral).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

#### `dhis2 maintenance validation send-notifications`

Fire configured notification templates for every current validation violation.

**Usage**:

```console
$ dhis2 maintenance validation send-notifications [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 maintenance validation validate-expression`

Parse-check an expression + render a human description.

**Usage**:

```console
$ dhis2 maintenance validation validate-expression [OPTIONS] EXPRESSION
```

**Arguments**:

* `EXPRESSION`: DHIS2 expression to parse-check.  [required]

**Options**:

* `--context TEXT`: Expression parser context: one of generic, validation-rule, indicator, predictor, program-indicator.  [default: generic]
* `--help`: Show this message and exit.

#### `dhis2 maintenance validation result`

List / get / delete persisted validation results.

**Usage**:

```console
$ dhis2 maintenance validation result [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List persisted validation results.
* `list`: List persisted validation results.
* `get`: Show one persisted validation result by id.
* `delete`: Bulk-delete validation results by filter.

##### `dhis2 maintenance validation result ls`

List persisted validation results.

**Usage**:

```console
$ dhis2 maintenance validation result ls [OPTIONS]
```

**Options**:

* `--ou TEXT`: Org-unit UID filter.
* `--pe TEXT`: Period filter (e.g. 202501).
* `--vr TEXT`: Validation-rule UID filter.
* `--page INTEGER`
* `--page-size INTEGER`
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

##### `dhis2 maintenance validation result list`

List persisted validation results.

**Usage**:

```console
$ dhis2 maintenance validation result list [OPTIONS]
```

**Options**:

* `--ou TEXT`: Org-unit UID filter.
* `--pe TEXT`: Period filter (e.g. 202501).
* `--vr TEXT`: Validation-rule UID filter.
* `--page INTEGER`
* `--page-size INTEGER`
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

##### `dhis2 maintenance validation result get`

Show one persisted validation result by id.

**Usage**:

```console
$ dhis2 maintenance validation result get [OPTIONS] RESULT_ID
```

**Arguments**:

* `RESULT_ID`: Numeric validation-result id.  [required]

**Options**:

* `--help`: Show this message and exit.

##### `dhis2 maintenance validation result delete`

Bulk-delete validation results by filter. At least one filter is required.

**Usage**:

```console
$ dhis2 maintenance validation result delete [OPTIONS]
```

**Options**:

* `--ou TEXT`: Org-unit UID filter. Repeatable.
* `--pe TEXT`: Period filter. Repeatable.
* `--vr TEXT`: Validation-rule UID filter. Repeatable.
* `--help`: Show this message and exit.

### `dhis2 maintenance predictors`

Run predictor expressions (CRUD on predictors: `dhis2 metadata list predictors`).

**Usage**:

```console
$ dhis2 maintenance predictors [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `run`: Run predictor expressions + emit data...

#### `dhis2 maintenance predictors run`

Run predictor expressions + emit data values for the given date range.

**Usage**:

```console
$ dhis2 maintenance predictors run [OPTIONS]
```

**Options**:

* `--start-date TEXT`: Period start, YYYY-MM-DD.  [required]
* `--end-date TEXT`: Period end, YYYY-MM-DD.  [required]
* `--predictor TEXT`: Run one predictor by UID. Mutually exclusive with --group.
* `--group TEXT`: Run all predictors in a PredictorGroup by UID.
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

## `dhis2 messaging`

DHIS2 internal messaging.

**Usage**:

```console
$ dhis2 messaging [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List conversations the authenticated user...
* `list`: List conversations the authenticated user...
* `get`: Show one conversation&#x27;s metadata + message...
* `send`: Create a new conversation with an initial...
* `reply`: Reply to an existing conversation with a...
* `mark-read`: Mark one or more conversations as read.
* `mark-unread`: Mark one or more conversations as unread.
* `delete`: Delete a conversation (soft-delete for the...
* `set-priority`: Set a conversation&#x27;s ticket-workflow...
* `set-status`: Set a conversation&#x27;s ticket-workflow status.
* `assign`: Assign a conversation to a user (ticket...
* `unassign`: Remove the assignee from a conversation.

### `dhis2 messaging ls`

List conversations the authenticated user is part of.

**Usage**:

```console
$ dhis2 messaging ls [OPTIONS]
```

**Options**:

* `--filter TEXT`: DHIS2 filter. Example: `read:eq:false` for unread only.
* `--page INTEGER`: 1-indexed page number.
* `--page-size INTEGER`: Rows per page (default 50).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 messaging list`

List conversations the authenticated user is part of.

**Usage**:

```console
$ dhis2 messaging list [OPTIONS]
```

**Options**:

* `--filter TEXT`: DHIS2 filter. Example: `read:eq:false` for unread only.
* `--page INTEGER`: 1-indexed page number.
* `--page-size INTEGER`: Rows per page (default 50).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 messaging get`

Show one conversation&#x27;s metadata + message thread.

**Usage**:

```console
$ dhis2 messaging get [OPTIONS] UID
```

**Arguments**:

* `UID`: Conversation UID.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging send`

Create a new conversation with an initial message.

**Usage**:

```console
$ dhis2 messaging send [OPTIONS] SUBJECT TEXT
```

**Arguments**:

* `SUBJECT`: Subject line.  [required]
* `TEXT`: Message body.  [required]

**Options**:

* `-u, --user TEXT`: User UID recipient. Repeatable.
* `-g, --user-group TEXT`: User-group UID recipient. Repeatable.
* `-o, --org-unit TEXT`: Organisation-unit UID recipient. Repeatable.
* `-a, --attachment TEXT`: FileResource UID to attach (upload via `dhis2 files resources upload --domain MESSAGE_ATTACHMENT` first). Repeatable.
* `--help`: Show this message and exit.

### `dhis2 messaging reply`

Reply to an existing conversation with a plain-text message.

DHIS2&#x27;s reply endpoint takes text/plain only on v42 — attachments +
internal-note flag only work on the initial `send` call.

**Usage**:

```console
$ dhis2 messaging reply [OPTIONS] UID TEXT
```

**Arguments**:

* `UID`: Conversation UID.  [required]
* `TEXT`: Reply body (plain text).  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging mark-read`

Mark one or more conversations as read.

**Usage**:

```console
$ dhis2 messaging mark-read [OPTIONS] UID...
```

**Arguments**:

* `UID...`: Conversation UID(s). One or more.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging mark-unread`

Mark one or more conversations as unread.

**Usage**:

```console
$ dhis2 messaging mark-unread [OPTIONS] UID...
```

**Arguments**:

* `UID...`: Conversation UID(s). One or more.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging delete`

Delete a conversation (soft-delete for the calling user; other participants keep it).

**Usage**:

```console
$ dhis2 messaging delete [OPTIONS] UID
```

**Arguments**:

* `UID`: Conversation UID.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging set-priority`

Set a conversation&#x27;s ticket-workflow priority.

Values: NONE / LOW / MEDIUM / HIGH. Applies to any messageType — most
meaningful on TICKET conversations, stored on PRIVATE threads too.

**Usage**:

```console
$ dhis2 messaging set-priority [OPTIONS] UID PRIORITY
```

**Arguments**:

* `UID`: Conversation UID.  [required]
* `PRIORITY`: Priority — NONE / LOW / MEDIUM / HIGH.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging set-status`

Set a conversation&#x27;s ticket-workflow status.

Values: NONE / OPEN / PENDING / INVALID / SOLVED. Not wired into the
initial `send` — DHIS2&#x27;s API requires a separate POST on the
`/status` sub-resource.

**Usage**:

```console
$ dhis2 messaging set-status [OPTIONS] UID STATUS
```

**Arguments**:

* `UID`: Conversation UID.  [required]
* `STATUS`: Status — NONE / OPEN / PENDING / INVALID / SOLVED.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging assign`

Assign a conversation to a user (ticket workflows).

**Usage**:

```console
$ dhis2 messaging assign [OPTIONS] UID USER
```

**Arguments**:

* `UID`: Conversation UID.  [required]
* `USER`: User UID to assign the conversation to.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 messaging unassign`

Remove the assignee from a conversation.

**Usage**:

```console
$ dhis2 messaging unassign [OPTIONS] UID
```

**Arguments**:

* `UID`: Conversation UID.  [required]

**Options**:

* `--help`: Show this message and exit.

## `dhis2 metadata`

DHIS2 metadata inspection.

**Usage**:

```console
$ dhis2 metadata [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List instances of a metadata resource.
* `list`: List instances of a metadata resource.
* `get`: Fetch one metadata object by UID.
* `export`: Download a metadata bundle from `GET...
* `import`: Upload a metadata bundle via `POST...
* `patch`: Apply an RFC 6902 JSON Patch to a metadata...
* `diff`: Compare two metadata bundles (or one...
* `diff-profiles`: Diff a metadata slice between two...
* `type`: Metadata resource types (the catalog).
* `options`: OptionSet workflows (show / find / sync).
* `attribute`: Cross-resource AttributeValue workflows...
* `program-rule`: Program rule workflows (show / vars-for /...
* `sql-view`: SQL view workflows (list / show / execute...
* `viz`: Visualization authoring (list / show /...
* `dashboard`: Dashboard composition (list / show /...
* `map`: Map authoring (list / show / create /...

### `dhis2 metadata ls`

List instances of a metadata resource.

**Usage**:

```console
$ dhis2 metadata ls [OPTIONS] RESOURCE
```

**Arguments**:

* `RESOURCE`: Resource type, e.g. dataElements, indicators  [required]

**Options**:

* `--fields TEXT`: DHIS2 field selector: plain (&#x27;id,name&#x27;), presets (&#x27;:identifiable&#x27;, &#x27;:nameable&#x27;, &#x27;:owner&#x27;, &#x27;:all&#x27;), nested (&#x27;children&#x27;), or exclusions (&#x27;:all,!lastUpdated&#x27;).  [default: id,name]
* `--filter TEXT`: Filter in `property:operator:value` form. Repeatable — AND&#x27;d by default, use --root-junction OR to switch.
* `--root-junction TEXT`: Combine repeated --filter as AND (default) or OR.  [default: AND]
* `--order TEXT`: Sort clause like &#x27;name:asc&#x27; or &#x27;created:desc&#x27;. Repeatable (later clauses tie-break).
* `--page INTEGER`: Server-side page number (1-based). Ignored when --all is set.
* `--page-size INTEGER`: Server-side page size (default 50). Ignored when --all is set.
* `--all`: Stream every page server-side (ignores --page/--page-size). Useful for dumping a full catalog.
* `--translate / --no-translate`: Return server-side translations for i18n fields.
* `--locale TEXT`: Locale for --translate, e.g. &#x27;fr&#x27;.
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 metadata list`

List instances of a metadata resource.

**Usage**:

```console
$ dhis2 metadata list [OPTIONS] RESOURCE
```

**Arguments**:

* `RESOURCE`: Resource type, e.g. dataElements, indicators  [required]

**Options**:

* `--fields TEXT`: DHIS2 field selector: plain (&#x27;id,name&#x27;), presets (&#x27;:identifiable&#x27;, &#x27;:nameable&#x27;, &#x27;:owner&#x27;, &#x27;:all&#x27;), nested (&#x27;children&#x27;), or exclusions (&#x27;:all,!lastUpdated&#x27;).  [default: id,name]
* `--filter TEXT`: Filter in `property:operator:value` form. Repeatable — AND&#x27;d by default, use --root-junction OR to switch.
* `--root-junction TEXT`: Combine repeated --filter as AND (default) or OR.  [default: AND]
* `--order TEXT`: Sort clause like &#x27;name:asc&#x27; or &#x27;created:desc&#x27;. Repeatable (later clauses tie-break).
* `--page INTEGER`: Server-side page number (1-based). Ignored when --all is set.
* `--page-size INTEGER`: Server-side page size (default 50). Ignored when --all is set.
* `--all`: Stream every page server-side (ignores --page/--page-size). Useful for dumping a full catalog.
* `--translate / --no-translate`: Return server-side translations for i18n fields.
* `--locale TEXT`: Locale for --translate, e.g. &#x27;fr&#x27;.
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 metadata get`

Fetch one metadata object by UID.

Prints a concise Rich summary by default (id, name, code, common metadata +
notable extras). Use `--json` for the full payload when debugging or
piping into jq. Pass `--fields` to narrow what DHIS2 returns.

**Usage**:

```console
$ dhis2 metadata get [OPTIONS] RESOURCE UID
```

**Arguments**:

* `RESOURCE`: Resource type, e.g. dataElements  [required]
* `UID`: Object UID  [required]

**Options**:

* `--fields TEXT`: DHIS2 fields selector.
* `--json`: Emit the full JSON payload instead of a summary.
* `--help`: Show this message and exit.

### `dhis2 metadata export`

Download a metadata bundle from `GET /api/metadata`.

Prints a per-resource count summary to stderr so stdout stays pipe-friendly
when `--output` is omitted. With `--check-references` (default), walks the
exported bundle and warns on any reference to a UID not in the bundle —
so a filtered `--resource dataElements` export doesn&#x27;t silently produce a
bundle that won&#x27;t round-trip because categoryCombos / optionSets / ...
are missing.

**Usage**:

```console
$ dhis2 metadata export [OPTIONS]
```

**Options**:

* `--resource TEXT`: Resource type to include (repeatable). Omit for every type DHIS2 exports by default.
* `--fields TEXT`: DHIS2 field selector. Defaults to &#x27;:owner&#x27; for a lossless round-trip import.  [default: :owner]
* `--filter TEXT`: Per-resource filter in the form `RESOURCE:property:operator:value`. Repeatable. Example: `--filter dataElements:name:like:ANC`. Same DSL as `dhis2 metadata list --filter`, prefixed with the resource name.
* `--resource-fields TEXT`: Per-resource field selector in the form `RESOURCE:SELECTOR`. Repeatable. Overrides the global `--fields` for the named resource. Example: `--resource-fields dataElements::identifiable`.
* `--skip-sharing`: Exclude sharing blocks from exported objects.
* `--skip-translation`: Exclude translation blocks.
* `--skip-validation`: Skip validation during export (matches DHIS2&#x27;s server-side option).
* `--check-references / --no-check-references`: After export, walk the bundle and warn on references to UIDs not in the bundle (e.g. a dataElement&#x27;s categoryCombo missing from a filtered export). On by default.  [default: check-references]
* `-o, --output PATH`: Write the bundle to this file (JSON). Omit to print to stdout.
* `--pretty / --no-pretty`: Indent JSON output (default: pretty).  [default: pretty]
* `--help`: Show this message and exit.

### `dhis2 metadata import`

Upload a metadata bundle via `POST /api/metadata` and print the import report.

**Usage**:

```console
$ dhis2 metadata import [OPTIONS] FILE
```

**Arguments**:

* `FILE`: Path to the metadata bundle JSON.  [required]

**Options**:

* `--strategy TEXT`: CREATE | UPDATE | CREATE_AND_UPDATE | DELETE (default CREATE_AND_UPDATE).  [default: CREATE_AND_UPDATE]
* `--atomic-mode TEXT`: ALL (rollback on any failure) or NONE (commit surviving objects).  [default: ALL]
* `--dry-run`: Validate + preheat without committing. Output is the import report DHIS2 would have produced.
* `--identifier TEXT`: UID | CODE | AUTO (default UID).  [default: UID]
* `--skip-sharing`
* `--skip-translation`
* `--skip-validation`
* `--merge-mode TEXT`: REPLACE (overwrite) or MERGE (patch) existing objects.
* `--preheat-mode TEXT`: REFERENCE (default), ALL, or NONE.
* `--flush-mode TEXT`: AUTO (default) or OBJECT.
* `--json`: Emit raw WebMessageResponse JSON.
* `--help`: Show this message and exit.

### `dhis2 metadata patch`

Apply an RFC 6902 JSON Patch to a metadata object (`PATCH /api/&lt;resource&gt;/{uid}`).

Two input modes:

- `--file patch.json` — full patch array on disk, one op per entry:
  `[{&quot;op&quot;: &quot;replace&quot;, &quot;path&quot;: &quot;/name&quot;, &quot;value&quot;: &quot;New&quot;}, ...]`
- `--set path=value` / `--remove path` (each repeatable) — inline shorthand
  for the common replace/remove cases. Values parse as JSON when possible
  (so `--set /valueType=INTEGER` sends a string, `--set /disabled=true`
  sends a boolean).

**Usage**:

```console
$ dhis2 metadata patch [OPTIONS] RESOURCE UID
```

**Arguments**:

* `RESOURCE`: Resource type, e.g. dataElements, indicators.  [required]
* `UID`: UID of the object to patch.  [required]

**Options**:

* `--file PATH`: JSON file with a RFC 6902 patch array. Mutually exclusive with --set/--remove.
* `--set TEXT`: Inline `replace` op as `path=value`. Repeatable. Values are JSON-decoded when they parse as JSON (`{&quot;a&quot;:1}`, `true`, `42`) and treated as strings otherwise.
* `--remove TEXT`: Inline `remove` op as `path`. Repeatable.
* `--json`: Emit raw WebMessageResponse JSON.
* `--help`: Show this message and exit.

### `dhis2 metadata diff`

Compare two metadata bundles (or one bundle against the live instance).

Per-resource counts of create/update/delete. Objects that differ only on
DHIS2&#x27;s per-instance noise (lastUpdated, createdBy, etc.) are treated as
unchanged by default — `--ignore` extends that list.

**Usage**:

```console
$ dhis2 metadata diff [OPTIONS] LEFT [RIGHT]
```

**Arguments**:

* `LEFT`: Left-hand bundle — the &#x27;source of truth&#x27; you&#x27;re comparing against.  [required]
* `[RIGHT]`: Right-hand bundle. Omit with `--live` to diff against the connected DHIS2 instance.

**Options**:

* `--live`: Use the connected DHIS2 instance as the right-hand side. Exports only the resource types present in the left bundle (no full-catalog fetch). Incompatible with a positional right arg.
* `--show-uids`: List up to 5 offending UIDs per per-resource row.
* `--ignore TEXT`: Fields to skip when deciding if an object changed. Repeatable. Defaults cover DHIS2&#x27;s per-instance noise (lastUpdated, createdBy, access, ...); pass `--ignore sharing` etc. to extend.
* `--json`: Emit the typed MetadataDiff as JSON.
* `--help`: Show this message and exit.

### `dhis2 metadata diff-profiles`

Diff a metadata slice between two registered profiles (staging vs prod drift).

Runs both exports in parallel, narrows to `--resource` types, optionally
filters each resource (`--filter resource:prop:op:val`), then structurally
diffs the two bundles ignoring DHIS2&#x27;s per-instance noise
(timestamps, createdBy, access strings, …).

A whole-instance diff is almost never useful — staging and prod diverge on
user accounts, org-unit assignments, and incidental settings by design. Pick
a narrow resource slice (`-r dataElements -r indicators`), filter further
with `--filter`, and extend `--ignore` for anything else that&#x27;s expected to
differ.

Exit code is `0` by default regardless of drift (so operators running this
interactively aren&#x27;t tripped by per-command-exit conventions). Pass
`--exit-on-drift` for the CI shape.

**Usage**:

```console
$ dhis2 metadata diff-profiles [OPTIONS] PROFILE_A PROFILE_B
```

**Arguments**:

* `PROFILE_A`: Name of the &#x27;left&#x27; profile (source of truth).  [required]
* `PROFILE_B`: Name of the &#x27;right&#x27; profile (candidate).  [required]

**Options**:

* `-r, --resource TEXT`: Resource type to compare (e.g. dataElements, indicators). Repeatable. Required — whole-instance diffs are almost always noise.
* `--filter TEXT`: Per-resource filter in `resource:property:operator:value` form. Repeatable. Example: `--filter dataElements:name:like:ANC` only compares data elements whose name contains &#x27;ANC&#x27;. Same DHIS2 filter DSL as `dhis2 metadata list --filter`.
* `--fields TEXT`: DHIS2 field selector applied on both profiles. Defaults to &#x27;:owner&#x27; — the selector DHIS2 itself uses for cross-instance imports (preserves every field needed for a faithful round-trip).  [default: :owner]
* `--ignore TEXT`: Additional fields to skip when deciding if an object changed. Repeatable. Defaults already cover DHIS2&#x27;s per-instance noise (lastUpdated, createdBy, access, ...). Common extensions for drift checks: `--ignore sharing --ignore translations`.
* `--show-uids`: List up to 5 offending UIDs per per-resource row.
* `--exit-on-drift`: Exit 1 when any object differs. CI-friendly (default is always exit 0).
* `--json`: Emit the typed MetadataDiff as JSON (bypasses the table).
* `--help`: Show this message and exit.

### `dhis2 metadata type`

Metadata resource types (the catalog).

**Usage**:

```console
$ dhis2 metadata type [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List the metadata resource types exposed...
* `list`: List the metadata resource types exposed...

#### `dhis2 metadata type ls`

List the metadata resource types exposed by the connected DHIS2 instance.

**Usage**:

```console
$ dhis2 metadata type ls [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 metadata type list`

List the metadata resource types exposed by the connected DHIS2 instance.

**Usage**:

```console
$ dhis2 metadata type list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `dhis2 metadata options`

OptionSet workflows (show / find / sync).

**Usage**:

```console
$ dhis2 metadata options [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `show`: Show one OptionSet with its options...
* `find`: Locate a single option inside a set by...
* `sync`: Idempotently sync an OptionSet to match a...
* `attribute`: External-system code mapping on Options...

#### `dhis2 metadata options show`

Show one OptionSet with its options resolved inline.

**Usage**:

```console
$ dhis2 metadata options show [OPTIONS] UID_OR_CODE
```

**Arguments**:

* `UID_OR_CODE`: OptionSet UID (11 chars) or business code.  [required]

**Options**:

* `--json`: Emit the raw OptionSet JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata options find`

Locate a single option inside a set by code or name; exit 1 if no match.

**Usage**:

```console
$ dhis2 metadata options find [OPTIONS]
```

**Options**:

* `--set TEXT`: OptionSet UID or business code.  [required]
* `--code TEXT`: Business code of the option to locate.
* `--name TEXT`: Display name of the option (exact match).
* `--json`: Emit the raw Option JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata options sync`

Idempotently sync an OptionSet to match a JSON spec file.

The spec is a JSON array of `{code, name, sort_order?}` objects. Codes
not currently in the set get **added**; codes present but with changed
names or sort order get **updated**; exact matches are **skipped**.
Pass `--remove-missing` to also drop options whose code isn&#x27;t in the
spec. `--dry-run` previews the diff without writing.

**Usage**:

```console
$ dhis2 metadata options sync [OPTIONS] SET_REF SPEC_FILE
```

**Arguments**:

* `SET_REF`: OptionSet UID or business code.  [required]
* `SPEC_FILE`: JSON file — list of `{code, name, sort_order?}` objects.  [required]

**Options**:

* `--remove-missing`: Also delete options whose code isn&#x27;t in the spec. Off by default — safer for partial refreshes.
* `--dry-run`: Compute the diff without writing anything.
* `--json`: Emit the UpsertReport as JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata options attribute`

External-system code mapping on Options via Attribute values.

**Usage**:

```console
$ dhis2 metadata options attribute [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Read one attribute value off an Option;...
* `set`: Set / replace an attribute value on an...
* `find`: Reverse lookup — find the Option whose...

##### `dhis2 metadata options attribute get`

Read one attribute value off an Option; exit 1 if unset.

**Usage**:

```console
$ dhis2 metadata options attribute get [OPTIONS] OPTION_UID ATTRIBUTE
```

**Arguments**:

* `OPTION_UID`: Option UID (11 chars).  [required]
* `ATTRIBUTE`: Attribute UID or business code (e.g. &#x27;SNOMED_CODE&#x27;).  [required]

**Options**:

* `--help`: Show this message and exit.

##### `dhis2 metadata options attribute set`

Set / replace an attribute value on an Option.

Reads the full Option, merges the new value (replaces any prior value
for the same attribute UID), PUTs the payload back. DHIS2&#x27;s
attribute-value list is identity-keyed by attribute UID, so this is
idempotent — calling twice with the same value is a no-op.

**Usage**:

```console
$ dhis2 metadata options attribute set [OPTIONS] OPTION_UID ATTRIBUTE VALUE
```

**Arguments**:

* `OPTION_UID`: Option UID (11 chars).  [required]
* `ATTRIBUTE`: Attribute UID or business code (e.g. &#x27;SNOMED_CODE&#x27;).  [required]
* `VALUE`: New attribute value.  [required]

**Options**:

* `--help`: Show this message and exit.

##### `dhis2 metadata options attribute find`

Reverse lookup — find the Option whose attribute matches a value.

The killer integration helper: external systems know a SNOMED / ICD /
LOINC code; this command returns the DHIS2 Option it maps to. Exits 1
on miss with a stderr hint.

**Usage**:

```console
$ dhis2 metadata options attribute find [OPTIONS]
```

**Options**:

* `--set TEXT`: OptionSet UID or business code.  [required]
* `--attribute TEXT`: Attribute UID or business code (e.g. &#x27;SNOMED_CODE&#x27;).  [required]
* `--value TEXT`: Attribute value to match exactly.  [required]
* `--json`: Emit the raw Option JSON.
* `--help`: Show this message and exit.

### `dhis2 metadata attribute`

Cross-resource AttributeValue workflows (get / set / delete / find).

**Usage**:

```console
$ dhis2 metadata attribute [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `get`: Read one attribute value off any resource;...
* `set`: Set / replace one attribute value on any...
* `delete`: Remove one attribute value from any...
* `find`: Reverse lookup across any resource — list...

#### `dhis2 metadata attribute get`

Read one attribute value off any resource; exit 1 if unset.

**Usage**:

```console
$ dhis2 metadata attribute get [OPTIONS] RESOURCE RESOURCE_UID ATTRIBUTE
```

**Arguments**:

* `RESOURCE`: Plural DHIS2 resource name (e.g. `dataElements`, `options`, `organisationUnits`).  [required]
* `RESOURCE_UID`: UID of the resource instance.  [required]
* `ATTRIBUTE`: Attribute UID or business code (e.g. `ICD10_CODE`).  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 metadata attribute set`

Set / replace one attribute value on any resource (read-merge-write).

**Usage**:

```console
$ dhis2 metadata attribute set [OPTIONS] RESOURCE RESOURCE_UID ATTRIBUTE VALUE
```

**Arguments**:

* `RESOURCE`: Plural DHIS2 resource name.  [required]
* `RESOURCE_UID`: UID of the resource instance.  [required]
* `ATTRIBUTE`: Attribute UID or business code.  [required]
* `VALUE`: New attribute value.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 metadata attribute delete`

Remove one attribute value from any resource; exit 0 regardless of whether it existed.

**Usage**:

```console
$ dhis2 metadata attribute delete [OPTIONS] RESOURCE RESOURCE_UID ATTRIBUTE
```

**Arguments**:

* `RESOURCE`: Plural DHIS2 resource name.  [required]
* `RESOURCE_UID`: UID of the resource instance.  [required]
* `ATTRIBUTE`: Attribute UID or business code.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 metadata attribute find`

Reverse lookup across any resource — list every UID whose attribute value matches.

Returns UIDs only (one per line) to keep the helper generic across
resource types. Pipe into `dhis2 metadata get &lt;resource&gt; &lt;uid&gt;` or
`dhis2 metadata list &lt;resource&gt; --filter id:in:[...]` for typed
follow-ups.

**Usage**:

```console
$ dhis2 metadata attribute find [OPTIONS] RESOURCE ATTRIBUTE VALUE
```

**Arguments**:

* `RESOURCE`: Plural DHIS2 resource name.  [required]
* `ATTRIBUTE`: Attribute UID or business code.  [required]
* `VALUE`: Attribute value to match exactly.  [required]

**Options**:

* `--filter TEXT`: Extra DHIS2 filter constraints to narrow the search (e.g. `domainType:eq:AGGREGATE`). Repeatable.
* `--help`: Show this message and exit.

### `dhis2 metadata program-rule`

Program rule workflows (show / vars-for / validate / where-de-is-used).

**Usage**:

```console
$ dhis2 metadata program-rule [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every ProgramRule (optionally scoped...
* `list`: List every ProgramRule (optionally scoped...
* `show`: Show one ProgramRule with its condition,...
* `vars-for`: List every `ProgramRuleVariable` in scope...
* `validate-expression`: Parse-check a program-rule condition...
* `where-de-is-used`: Impact analysis — list every rule whose...

#### `dhis2 metadata program-rule ls`

List every ProgramRule (optionally scoped to one program), sorted by priority.

**Usage**:

```console
$ dhis2 metadata program-rule ls [OPTIONS]
```

**Options**:

* `--program TEXT`: Program UID; omit to list every rule on the instance.
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata program-rule list`

List every ProgramRule (optionally scoped to one program), sorted by priority.

**Usage**:

```console
$ dhis2 metadata program-rule list [OPTIONS]
```

**Options**:

* `--program TEXT`: Program UID; omit to list every rule on the instance.
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata program-rule show`

Show one ProgramRule with its condition, priority, and every action.

**Usage**:

```console
$ dhis2 metadata program-rule show [OPTIONS] RULE_UID
```

**Arguments**:

* `RULE_UID`: ProgramRule UID.  [required]

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata program-rule vars-for`

List every `ProgramRuleVariable` in scope for a program, sorted by name.

**Usage**:

```console
$ dhis2 metadata program-rule vars-for [OPTIONS] PROGRAM_UID
```

**Arguments**:

* `PROGRAM_UID`: Program UID.  [required]

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata program-rule validate-expression`

Parse-check a program-rule condition expression.

DHIS2 doesn&#x27;t expose a dedicated program-rule expression validator —
the closest is the program-indicator parser (used by default here),
which enforces stricter `#{stage.de}` syntax than program rules
accept. For the common `#{variableName}` shorthand program rules
use, the PI validator flags &quot;Invalid Program Stage / DataElement
syntax&quot; — not a real error, just the parser mismatch. Trust a clean
OK as definitely valid; read the specific message on ERROR to
distinguish parser mismatches from real syntax problems.

**Usage**:

```console
$ dhis2 metadata program-rule validate-expression [OPTIONS] EXPRESSION
```

**Arguments**:

* `EXPRESSION`: Program-rule condition expression.  [required]

**Options**:

* `--context TEXT`: Which DHIS2 expression parser to use: program-indicator (default), validation-rule, indicator, predictor, or generic.  [default: program-indicator]
* `--help`: Show this message and exit.

#### `dhis2 metadata program-rule where-de-is-used`

Impact analysis — list every rule whose actions reference this DataElement.

Useful before renaming / removing a DE: catches rules that&#x27;d stop
firing once the reference breaks. Exit 1 if nothing matches (safe
shorthand for `grep -q` pipelines).

**Usage**:

```console
$ dhis2 metadata program-rule where-de-is-used [OPTIONS] DATA_ELEMENT_UID
```

**Arguments**:

* `DATA_ELEMENT_UID`: DataElement UID.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 metadata sql-view`

SQL view workflows (list / show / execute / refresh / adhoc).

**Usage**:

```console
$ dhis2 metadata sql-view [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every SqlView on the instance, sorted...
* `list`: List every SqlView on the instance, sorted...
* `show`: Show one SqlView&#x27;s metadata + its stored...
* `execute`: Run a SqlView and render its rows as a...
* `refresh`: Refresh a MATERIALIZED_VIEW or lazily...
* `adhoc`: Register a throwaway SqlView from a .sql...

#### `dhis2 metadata sql-view ls`

List every SqlView on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata sql-view ls [OPTIONS]
```

**Options**:

* `--type TEXT`: Filter by SqlViewType: VIEW, MATERIALIZED_VIEW, or QUERY.
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata sql-view list`

List every SqlView on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata sql-view list [OPTIONS]
```

**Options**:

* `--type TEXT`: Filter by SqlViewType: VIEW, MATERIALIZED_VIEW, or QUERY.
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata sql-view show`

Show one SqlView&#x27;s metadata + its stored SQL body.

**Usage**:

```console
$ dhis2 metadata sql-view show [OPTIONS] VIEW_UID
```

**Arguments**:

* `VIEW_UID`: SqlView UID.  [required]

**Options**:

* `--json`: Emit raw JSON (includes full sqlQuery).
* `--help`: Show this message and exit.

#### `dhis2 metadata sql-view execute`

Run a SqlView and render its rows as a table, JSON array, or CSV.

**Usage**:

```console
$ dhis2 metadata sql-view execute [OPTIONS] VIEW_UID
```

**Arguments**:

* `VIEW_UID`: SqlView UID.  [required]

**Options**:

* `--var TEXT`: `${name}` substitution for QUERY views, in `name:value` form. Repeatable. DHIS2 strips non-alphanumeric characters from values server-side — wildcards belong in the SQL.
* `--criteria TEXT`: Column filter for VIEW / MATERIALIZED_VIEW results, in `column:value` form. Repeatable.
* `--format TEXT`: Output format: table (default), json, or csv.  [default: table]
* `--help`: Show this message and exit.

#### `dhis2 metadata sql-view refresh`

Refresh a MATERIALIZED_VIEW or lazily create a VIEW&#x27;s DB object.

`POST /api/sqlViews/{uid}/execute` is idempotent for VIEW types — the
first call creates the Postgres view; subsequent calls are no-ops.
MATERIALIZED_VIEW types re-run the underlying SQL each call.

**Usage**:

```console
$ dhis2 metadata sql-view refresh [OPTIONS] VIEW_UID
```

**Arguments**:

* `VIEW_UID`: SqlView UID.  [required]

**Options**:

* `--help`: Show this message and exit.

#### `dhis2 metadata sql-view adhoc`

Register a throwaway SqlView from a .sql file, execute once, delete it on the way out.

Designed for iterating on SQL without leaving test metadata behind.
Subject to DHIS2&#x27;s SQL allowlist — for fully free-form queries, see
the Postgres injector example.

**Usage**:

```console
$ dhis2 metadata sql-view adhoc [OPTIONS] NAME SQL_PATH
```

**Arguments**:

* `NAME`: Display name for the throwaway view.  [required]
* `SQL_PATH`: .sql file containing the query body.  [required]

**Options**:

* `--type TEXT`: SqlViewType — QUERY (default), VIEW, or MATERIALIZED_VIEW.  [default: QUERY]
* `--keep`: Leave the view in place afterwards instead of deleting.
* `--var TEXT`: `${name}` substitution in `name:value` form. Repeatable.
* `--format TEXT`: Output format: table (default), json, or csv.  [default: table]
* `--help`: Show this message and exit.

### `dhis2 metadata viz`

Visualization authoring (list / show / create / clone / delete).

**Usage**:

```console
$ dhis2 metadata viz [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every Visualization on the instance,...
* `list`: List every Visualization on the instance,...
* `show`: Show one Visualization with axes + data...
* `create`: Create a Visualization from flags — one...
* `clone`: Clone an existing Visualization with a...
* `delete`: Delete a Visualization.

#### `dhis2 metadata viz ls`

List every Visualization on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata viz ls [OPTIONS]
```

**Options**:

* `--type TEXT`: Filter by VisualizationType (LINE / COLUMN / PIVOT_TABLE / SINGLE_VALUE / ...).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata viz list`

List every Visualization on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata viz list [OPTIONS]
```

**Options**:

* `--type TEXT`: Filter by VisualizationType (LINE / COLUMN / PIVOT_TABLE / SINGLE_VALUE / ...).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata viz show`

Show one Visualization with axes + data dimensions + period / ou selection.

**Usage**:

```console
$ dhis2 metadata viz show [OPTIONS] VIZ_UID
```

**Arguments**:

* `VIZ_UID`: Visualization UID.  [required]

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata viz create`

Create a Visualization from flags — one command, no hand-rolled JSON.

Uses `VisualizationSpec` defaults per chart type: LINE / COLUMN / BAR /
etc. default to rows= / columns= / filters=; PIVOT_TABLE
defaults to rows= / columns= / filters=; SINGLE_VALUE
collapses to columns= / filters=. Override any slot with
--category-dim / --series-dim / --filter-dim.

**Usage**:

```console
$ dhis2 metadata viz create [OPTIONS]
```

**Options**:

* `--name TEXT`: Display name for the new Visualization.  [required]
* `--type TEXT`: VisualizationType: LINE, COLUMN, STACKED_COLUMN, BAR, PIVOT_TABLE, SINGLE_VALUE, etc.  [required]
* `--de TEXT`: DataElement UID (repeat for multi-DE charts).  [required]
* `--pe TEXT`: Period ID (e.g. 202401, 2024Q1, 2024). Repeat for multi-period.  [required]
* `--ou TEXT`: OrganisationUnit UID. Repeat for multi-OU.  [required]
* `--description TEXT`: Optional long description.
* `--uid TEXT`: Explicit UID (11 chars). Auto-generates when omitted.
* `--category-dim TEXT`: Override category axis: dx / pe / ou.
* `--series-dim TEXT`: Override series dimension: dx / pe / ou.
* `--filter-dim TEXT`: Override filter dimension: dx / pe / ou.
* `--json`: Emit the created viz as raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata viz clone`

Clone an existing Visualization with a fresh UID + new name.

**Usage**:

```console
$ dhis2 metadata viz clone [OPTIONS] SOURCE_UID
```

**Arguments**:

* `SOURCE_UID`: Source Visualization UID.  [required]

**Options**:

* `--new-name TEXT`: Display name for the cloned Visualization.  [required]
* `--new-uid TEXT`: Explicit UID for the clone (11 chars). Auto-generates when omitted.
* `--new-description TEXT`: Override the source&#x27;s description on the clone.
* `--json`: Emit the clone as raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata viz delete`

Delete a Visualization.

**Usage**:

```console
$ dhis2 metadata viz delete [OPTIONS] VIZ_UID
```

**Arguments**:

* `VIZ_UID`: Visualization UID to delete.  [required]

**Options**:

* `-y, --yes`: Skip the confirmation prompt.
* `--help`: Show this message and exit.

### `dhis2 metadata dashboard`

Dashboard composition (list / show / add-item / remove-item).

**Usage**:

```console
$ dhis2 metadata dashboard [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every Dashboard on the instance,...
* `list`: List every Dashboard on the instance,...
* `show`: Show one Dashboard with every...
* `add-item`: Add a Visualization or Map item to a...
* `remove-item`: Remove one dashboardItem by its UID.

#### `dhis2 metadata dashboard ls`

List every Dashboard on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata dashboard ls [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata dashboard list`

List every Dashboard on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata dashboard list [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata dashboard show`

Show one Dashboard with every dashboardItem resolved inline.

**Usage**:

```console
$ dhis2 metadata dashboard show [OPTIONS] DASHBOARD_UID
```

**Arguments**:

* `DASHBOARD_UID`: Dashboard UID.  [required]

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata dashboard add-item`

Add a Visualization or Map item to a dashboard.

Pass --viz to add a VISUALIZATION item or --map to add a MAP item
(exactly one required). Omit --x / --y / --width / --height to
auto-stack below existing items (full width); supply them when
you want side-by-side tiling.

**Usage**:

```console
$ dhis2 metadata dashboard add-item [OPTIONS] DASHBOARD_UID
```

**Arguments**:

* `DASHBOARD_UID`: Dashboard UID.  [required]

**Options**:

* `--viz TEXT`: Visualization UID (mutually exclusive with --map).
* `--map TEXT`: Map UID to add as a MAP-type dashboard item.
* `--x INTEGER`: Grid x coordinate (0-60). Auto-stacks when omitted.
* `--y INTEGER`: Grid y coordinate. Auto-stacks below existing when omitted.
* `--width INTEGER`: Slot width (1-60). Defaults to 60 when auto.
* `--height INTEGER`: Slot height. Defaults to 20 when auto.
* `--help`: Show this message and exit.

#### `dhis2 metadata dashboard remove-item`

Remove one dashboardItem by its UID.

**Usage**:

```console
$ dhis2 metadata dashboard remove-item [OPTIONS] DASHBOARD_UID ITEM_UID
```

**Arguments**:

* `DASHBOARD_UID`: Dashboard UID.  [required]
* `ITEM_UID`: DashboardItem UID to remove.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 metadata map`

Map authoring (list / show / create / clone / delete).

**Usage**:

```console
$ dhis2 metadata map [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every Map on the instance, sorted by...
* `list`: List every Map on the instance, sorted by...
* `show`: Show one Map with its viewport + every...
* `create`: Create a single-layer thematic choropleth...
* `clone`: Clone an existing Map with a fresh UID +...
* `delete`: Delete a Map.

#### `dhis2 metadata map ls`

List every Map on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata map ls [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata map list`

List every Map on the instance, sorted by name.

**Usage**:

```console
$ dhis2 metadata map list [OPTIONS]
```

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata map show`

Show one Map with its viewport + every mapViews layer.

**Usage**:

```console
$ dhis2 metadata map show [OPTIONS] MAP_UID
```

**Arguments**:

* `MAP_UID`: Map UID.  [required]

**Options**:

* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata map create`

Create a single-layer thematic choropleth Map from flags.

Multi-layer maps need raw `Map` / `MapView` construction — use
`client.maps.create_from_spec(MapSpec(layers=[...]))` from the
library side and extend the spec to include boundary / facility
/ event layers.

**Usage**:

```console
$ dhis2 metadata map create [OPTIONS]
```

**Options**:

* `--name TEXT`: Display name for the new Map.  [required]
* `--de TEXT`: DataElement UID for the thematic layer.  [required]
* `--pe TEXT`: Period ID. Repeat for multi-period.  [required]
* `--ou TEXT`: OrganisationUnit UID (usually the parent boundary). Repeat for multi.  [required]
* `--ou-level INTEGER`: OU hierarchy level(s) to render (e.g. 2 for provinces). Repeat for multi.  [required]
* `--description TEXT`
* `--uid TEXT`: Explicit UID (11 chars). Auto-generates when omitted.
* `--longitude FLOAT`: [default: 15.0]
* `--latitude FLOAT`: [default: 0.0]
* `--zoom INTEGER`: [default: 4]
* `--basemap TEXT`: [default: openStreetMap]
* `--classes INTEGER`: Number of color classes on the choropleth.  [default: 5]
* `--color-low TEXT`: Choropleth low-value colour (#hex).  [default: #fef0d9]
* `--color-high TEXT`: Choropleth high-value colour (#hex).  [default: #b30000]
* `--json`: Emit the created map as raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata map clone`

Clone an existing Map with a fresh UID + new name.

**Usage**:

```console
$ dhis2 metadata map clone [OPTIONS] SOURCE_UID
```

**Arguments**:

* `SOURCE_UID`: Source Map UID.  [required]

**Options**:

* `--new-name TEXT`: Display name for the cloned Map.  [required]
* `--new-uid TEXT`: Explicit UID for the clone.
* `--new-description TEXT`
* `--json`: Emit the clone as raw JSON.
* `--help`: Show this message and exit.

#### `dhis2 metadata map delete`

Delete a Map.

**Usage**:

```console
$ dhis2 metadata map delete [OPTIONS] MAP_UID
```

**Arguments**:

* `MAP_UID`: Map UID to delete.  [required]

**Options**:

* `-y, --yes`: Skip the confirmation prompt.
* `--help`: Show this message and exit.

## `dhis2 profile`

Manage DHIS2 profiles.

**Usage**:

```console
$ dhis2 profile [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List every known profile with its source...
* `list`: List every known profile with its source...
* `verify`: Verify one profile or all profiles by...
* `show`: Print one profile (secrets redacted by...
* `default`: Set `default = &lt;name&gt;` in the global...
* `add`: Add (or upsert) a profile.
* `remove`: Remove a profile.
* `rename`: Rename a profile in-place.
* `login`: Run the OAuth2 authorization-code flow for...
* `logout`: Clear persisted OAuth2 tokens for a profile.
* `bootstrap`: One-shot: provision a PAT or OAuth2 client...
* `oidc-config`: Populate an OAuth2 profile by discovering...

### `dhis2 profile ls`

List every known profile with its source and default status.

**Usage**:

```console
$ dhis2 profile ls [OPTIONS]
```

**Options**:

* `-a, --all`: Include shadowed profiles (global entries hidden by project ones).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

### `dhis2 profile list`

List every known profile with its source and default status.

**Usage**:

```console
$ dhis2 profile list [OPTIONS]
```

**Options**:

* `-a, --all`: Include shadowed profiles (global entries hidden by project ones).
* `--json`: Emit raw JSON.
* `--help`: Show this message and exit.

### `dhis2 profile verify`

Verify one profile or all profiles by hitting /api/system/info + /api/me.

**Usage**:

```console
$ dhis2 profile verify [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: Profile name to verify; omit to verify all.

**Options**:

* `--json`
* `--help`: Show this message and exit.

### `dhis2 profile show`

Print one profile (secrets redacted by default).

**Usage**:

```console
$ dhis2 profile show [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--secrets`: Include sensitive values.
* `--json`: Emit the raw profile JSON.
* `--help`: Show this message and exit.

### `dhis2 profile default`

Set `default = &lt;name&gt;` in the global (default) or project profiles.toml.

When `name` is omitted and stdin is a TTY, the command renders the
profile list + prompts for a numbered selection. Pass `--global` or
`--local` to pick the profiles.toml to write (`--global` is the
default).

**Usage**:

```console
$ dhis2 profile default [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: Profile name to set as default. Omit to pick interactively from a list.

**Options**:

* `--global`: Write to ~/.config/dhis2/profiles.toml (default).
* `--local`: Write to ./.dhis2/profiles.toml instead.
* `--verify`: Probe the instance after switching.
* `--help`: Show this message and exit.

### `dhis2 profile add`

Add (or upsert) a profile.

Secrets are never accepted as command-line flags (they&#x27;d leak into shell history).
Read from env (`DHIS2_PAT`, `DHIS2_PASSWORD`, `DHIS2_OAUTH_CLIENT_SECRET`) or
prompted interactively when missing.

**Usage**:

```console
$ dhis2 profile add [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--auth TEXT`: pat | basic | oauth2  [default: pat]
* `--username TEXT`: Basic-auth username.
* `--client-id TEXT`: OAuth2 client_id.
* `--scope TEXT`: OAuth2 scope (DHIS2 only recognises `ALL`).  [default: ALL]
* `--redirect-uri TEXT`: OAuth2 redirect URI (must match the registered client).  [default: http://localhost:8765]
* `--from-env`: Pull OAuth2 fields from DHIS2_OAUTH_CLIENT_ID / DHIS2_OAUTH_CLIENT_SECRET / DHIS2_OAUTH_REDIRECT_URI / DHIS2_OAUTH_SCOPES env vars (seeded .env.auth).
* `--global`: Save to ~/.config/dhis2/profiles.toml (default — user-wide, applies everywhere).
* `--local`: Save to ./.dhis2/profiles.toml instead (project-scoped, overrides global).
* `--default`: Set as default after adding.
* `--verify`: Probe /api/system/info + /api/me after saving.
* `--help`: Show this message and exit.

### `dhis2 profile remove`

Remove a profile. Without --global/--local, removes from whichever file holds it.

**Usage**:

```console
$ dhis2 profile remove [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--global`: Remove from ~/.config/dhis2/profiles.toml specifically.
* `--local`: Remove from ./.dhis2/profiles.toml specifically.
* `--help`: Show this message and exit.

### `dhis2 profile rename`

Rename a profile in-place. Preserves scope and updates default if needed.

**Usage**:

```console
$ dhis2 profile rename [OPTIONS] OLD_NAME NEW_NAME
```

**Arguments**:

* `OLD_NAME`: Current profile name.  [required]
* `NEW_NAME`: New profile name (letters, digits, underscores).  [required]

**Options**:

* `--verify`: Probe the instance after renaming.
* `--help`: Show this message and exit.

### `dhis2 profile login`

Run the OAuth2 authorization-code flow for a profile and persist its tokens.

Opens a browser to DHIS2&#x27;s authorization endpoint, listens on the profile&#x27;s
`redirect_uri` (local FastAPI+uvicorn), exchanges the code for tokens,
and writes them to the scope-appropriate tokens.sqlite. OAuth2 profiles only.

**Usage**:

```console
$ dhis2 profile login [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: Profile name; omit to use the default.

**Options**:

* `--help`: Show this message and exit.

### `dhis2 profile logout`

Clear persisted OAuth2 tokens for a profile.

Removes the row from the scope-appropriate `tokens.sqlite`. Next API call
triggers a fresh `profile login` flow. OAuth2 profiles only.

**Usage**:

```console
$ dhis2 profile logout [OPTIONS] [NAME]
```

**Arguments**:

* `[NAME]`: Profile name; omit to use the default.

**Options**:

* `--help`: Show this message and exit.

### `dhis2 profile bootstrap`

One-shot: provision a PAT or OAuth2 client on DHIS2, save a profile, (for oauth2) log in.

Secrets never come in via argv. Read from env
(`DHIS2_ADMIN_PAT`, `DHIS2_ADMIN_PASSWORD`, `DHIS2_OAUTH_CLIENT_SECRET`)
or prompted interactively when missing. Admin creds are used once to POST
`/api/apiToken` (pat) or `/api/oAuth2Clients` (oauth2), then discarded.

Re-runs for `auth=oauth2` fail at POST /api/oAuth2Clients if `client_id` is
taken — pass a different `--client-id` in that case. PAT bootstraps never
collide (DHIS2 mints a fresh server-side UID).

**Usage**:

```console
$ dhis2 profile bootstrap [OPTIONS] NAME
```

**Arguments**:

* `NAME`: Profile name to create.  [required]

**Options**:

* `--auth TEXT`: pat | oauth2 — which kind of profile to set up.  [default: oauth2]
* `--url TEXT`: DHIS2 base URL (also: DHIS2_URL env).
* `--admin-user TEXT`: Admin username (for basic bootstrap).
* `--client-id TEXT`: OAuth2 client_id to register (auth=oauth2).  [default: dhis2-utils-local]
* `--redirect-uri TEXT`: OAuth2 redirect URI.  [default: http://localhost:8765]
* `--scope TEXT`: OAuth2 scope.  [default: ALL]
* `--pat-description TEXT`: PAT description (auth=pat).
* `--pat-expires-in-days INTEGER`: PAT lifetime in days; omit for no expiry.
* `--global`: Save to ~/.config/dhis2/profiles.toml (default).
* `--local`: Save to ./.dhis2/profiles.toml instead.
* `--login / --no-login`: For auth=oauth2, run `profile login` after saving. Ignored for auth=pat.  [default: login]
* `--help`: Show this message and exit.

### `dhis2 profile oidc-config`

Populate an OAuth2 profile by discovering a DHIS2 instance&#x27;s OIDC endpoints.

Fetches `/.well-known/openid-configuration` from the given URL, validates the
response, and writes a profile with `auth=oauth2` + your client credentials.
Removes the &quot;hand-edit profiles.toml with the right issuer/auth/token URLs&quot;
step from the OAuth2 setup walkthrough.

The URL can be either the DHIS2 base URL (discovery path is appended
automatically) or the full discovery URL.

**Usage**:

```console
$ dhis2 profile oidc-config [OPTIONS] URL
```

**Arguments**:

* `URL`: DHIS2 base URL or full /.well-known/openid-configuration URL.  [required]

**Options**:

* `-n, --name TEXT`: Profile name to save as.  [required]
* `--client-id TEXT`: OAuth2 client_id (from your registration).  [required]
* `--client-secret TEXT`: OAuth2 client_secret.  [required]
* `--scope TEXT`: OAuth2 scope (DHIS2 only recognises `ALL`).  [default: ALL]
* `--redirect-uri TEXT`: OAuth2 redirect URI (match your registered client — default is the CLI&#x27;s loopback listener).  [default: http://localhost:8765]
* `--global`: Save to ~/.config/dhis2/profiles.toml (default, user-wide).
* `--local`: Save to ./.dhis2/profiles.toml instead (project-scoped).
* `--default`: Set as default after saving.
* `--login`: Trigger `dhis2 profile login &lt;name&gt;` immediately after saving.
* `--json`: Emit the discovery summary as JSON.
* `--help`: Show this message and exit.

## `dhis2 route`

DHIS2 integration routes.

**Usage**:

```console
$ dhis2 route [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List registered routes.
* `list`: List registered routes.
* `get`: Fetch one route by UID.
* `add`: Create a route via POST /api/routes.
* `update`: Replace a route via PUT /api/routes/{uid}.
* `patch`: Apply a JSON Patch to a route via PATCH...
* `delete`: Delete a route.
* `run`: Execute a route — DHIS2 proxies the...

### `dhis2 route ls`

List registered routes.

**Usage**:

```console
$ dhis2 route ls [OPTIONS]
```

**Options**:

* `--fields TEXT`: [default: id,code,name,url,disabled,auth]
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 route list`

List registered routes.

**Usage**:

```console
$ dhis2 route list [OPTIONS]
```

**Options**:

* `--fields TEXT`: [default: id,code,name,url,disabled,auth]
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 route get`

Fetch one route by UID.

**Usage**:

```console
$ dhis2 route get [OPTIONS] UID
```

**Arguments**:

* `UID`: [required]

**Options**:

* `--fields TEXT`
* `--json`: Emit the raw Route JSON.
* `--help`: Show this message and exit.

### `dhis2 route add`

Create a route via POST /api/routes.

With `--file`: pass a full JSON spec (advanced — see BUGS.md for the DHIS2 schema).

Without `--file`: guided wizard. Prompts for code, name, url, then asks which
upstream auth type to use. Secrets (basic password, bearer token, header/query
value, OAuth2 client_secret) never come in via argv — they&#x27;re read from env
(`DHIS2_ROUTE_UPSTREAM_*`) or at the hidden-input prompt.

**Usage**:

```console
$ dhis2 route add [OPTIONS]
```

**Options**:

* `--file PATH`: JSON file with the route definition (bypass the interactive wizard).
* `--code TEXT`
* `--name TEXT`
* `--url TEXT`: Target URL the route proxies to.
* `--authorities TEXT`: Comma-separated DHIS2 authorities allowed to run this route.
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 route update`

Replace a route via PUT /api/routes/{uid}.

DHIS2 PUT expects the complete object. For partial updates use `patch`.

**Usage**:

```console
$ dhis2 route update [OPTIONS] UID
```

**Arguments**:

* `UID`: [required]

**Options**:

* `--file PATH`: JSON file with the full route spec (PUT semantics).  [required]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 route patch`

Apply a JSON Patch to a route via PATCH /api/routes/{uid}.

**Usage**:

```console
$ dhis2 route patch [OPTIONS] UID
```

**Arguments**:

* `UID`: [required]

**Options**:

* `--file PATH`: JSON Patch array (RFC 6902).  [required]
* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 route delete`

Delete a route.

**Usage**:

```console
$ dhis2 route delete [OPTIONS] UID
```

**Arguments**:

* `UID`: [required]

**Options**:

* `--json`: Emit the raw WebMessageResponse envelope.
* `--help`: Show this message and exit.

### `dhis2 route run`

Execute a route — DHIS2 proxies the request to the configured target URL.

**Usage**:

```console
$ dhis2 route run [OPTIONS] UID
```

**Arguments**:

* `UID`: [required]

**Options**:

* `-X, --method TEXT`: [default: GET]
* `--body PATH`: JSON body file for POST/PUT.
* `--path TEXT`: Additional path segment appended to the route&#x27;s target URL.
* `--help`: Show this message and exit.

## `dhis2 system`

DHIS2 system info.

**Usage**:

```console
$ dhis2 system [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `whoami`: Print the authenticated DHIS2 user for the...
* `info`: Print DHIS2 system info (version, build,...

### `dhis2 system whoami`

Print the authenticated DHIS2 user for the current environment profile.

**Usage**:

```console
$ dhis2 system whoami [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `dhis2 system info`

Print DHIS2 system info (version, build, analytics state, env).

**Usage**:

```console
$ dhis2 system info [OPTIONS]
```

**Options**:

* `--json`: Emit the raw SystemInfo JSON.
* `--help`: Show this message and exit.

## `dhis2 user`

DHIS2 user administration.

**Usage**:

```console
$ dhis2 user [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List users.
* `list`: List users.
* `get`: Fetch one user by UID or username.
* `me`: Print the authenticated user&#x27;s `/api/me`...
* `invite`: Create a user and send the invitation email.
* `reinvite`: Re-send the invitation email for a pending...
* `reset-password`: Trigger DHIS2&#x27;s password-reset email (POST...

### `dhis2 user ls`

List users.

Examples:
  dhis2 user list
  dhis2 user list --filter &#x27;disabled:eq:true&#x27; --order &#x27;username:asc&#x27;
  dhis2 user list --filter &#x27;username:like:admin&#x27;

**Usage**:

```console
$ dhis2 user ls [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector. Supports plain lists (&#x27;id,username,email&#x27;), presets (&#x27;:identifiable&#x27;, &#x27;:nameable&#x27;, &#x27;:owner&#x27;, &#x27;:all&#x27;), and exclusions (&#x27;:all,!password&#x27;).  [default: id,username,displayName,email,disabled,lastLogin]
* `--filter TEXT`: Filter &#x27;property:operator:value&#x27; (repeatable).
* `--root-junction TEXT`: Combine repeated --filter as AND (default) or OR.  [default: AND]
* `--order TEXT`: Sort clause &#x27;property:asc|desc&#x27; (repeatable).
* `--page INTEGER`: Server-side page number (1-based).
* `--page-size INTEGER`: Server-side page size (default 50).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user list`

List users.

Examples:
  dhis2 user list
  dhis2 user list --filter &#x27;disabled:eq:true&#x27; --order &#x27;username:asc&#x27;
  dhis2 user list --filter &#x27;username:like:admin&#x27;

**Usage**:

```console
$ dhis2 user list [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector. Supports plain lists (&#x27;id,username,email&#x27;), presets (&#x27;:identifiable&#x27;, &#x27;:nameable&#x27;, &#x27;:owner&#x27;, &#x27;:all&#x27;), and exclusions (&#x27;:all,!password&#x27;).  [default: id,username,displayName,email,disabled,lastLogin]
* `--filter TEXT`: Filter &#x27;property:operator:value&#x27; (repeatable).
* `--root-junction TEXT`: Combine repeated --filter as AND (default) or OR.  [default: AND]
* `--order TEXT`: Sort clause &#x27;property:asc|desc&#x27; (repeatable).
* `--page INTEGER`: Server-side page number (1-based).
* `--page-size INTEGER`: Server-side page size (default 50).
* `--json`: Emit raw JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user get`

Fetch one user by UID or username. Prints a concise summary; `--json` for full payload.

**Usage**:

```console
$ dhis2 user get [OPTIONS] UID_OR_USERNAME
```

**Arguments**:

* `UID_OR_USERNAME`: User UID (11 chars) or username.  [required]

**Options**:

* `--fields TEXT`: DHIS2 field selector.
* `--json`: Emit the raw User payload instead of a summary.
* `--help`: Show this message and exit.

### `dhis2 user me`

Print the authenticated user&#x27;s `/api/me` summary. `--json` for full payload.

**Usage**:

```console
$ dhis2 user me [OPTIONS]
```

**Options**:

* `--json`: Emit the raw /api/me payload.
* `--help`: Show this message and exit.

### `dhis2 user invite`

Create a user and send the invitation email.

Hits POST /api/users/invite. DHIS2&#x27;s configured mailer sends the link;
the new user sets their password on accept. Prints the new user&#x27;s UID.

**Usage**:

```console
$ dhis2 user invite [OPTIONS] EMAIL
```

**Arguments**:

* `EMAIL`: Email address for the new user (receives the invitation link).  [required]

**Options**:

* `--first-name TEXT`: User&#x27;s given name.  [required]
* `--surname TEXT`: User&#x27;s surname.  [required]
* `--username TEXT`: Desired username. Omit to let DHIS2 derive from the email prefix.
* `--user-role TEXT`: User-role UID (repeatable). Grants the role on accept.
* `--org-unit TEXT`: Organisation-unit UID for capture scope (repeatable).
* `--help`: Show this message and exit.

### `dhis2 user reinvite`

Re-send the invitation email for a pending user (POST /api/users/{uid}/invite).

**Usage**:

```console
$ dhis2 user reinvite [OPTIONS] UID
```

**Arguments**:

* `UID`: UID of a user who hasn&#x27;t yet completed their invite.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 user reset-password`

Trigger DHIS2&#x27;s password-reset email (POST /api/users/{uid}/reset).

**Usage**:

```console
$ dhis2 user reset-password [OPTIONS] UID
```

**Arguments**:

* `UID`: UID of the user to reset.  [required]

**Options**:

* `--help`: Show this message and exit.

## `dhis2 user-group`

DHIS2 user-group administration.

**Usage**:

```console
$ dhis2 user-group [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List user groups.
* `list`: List user groups.
* `get`: Fetch one user group by UID.
* `add-member`: Add a user to a group (POST...
* `remove-member`: Remove a user from a group (DELETE...
* `sharing-get`: Print the current sharing block for one...
* `sharing-grant-user`: Grant one user access to a group (shortcut...

### `dhis2 user-group ls`

List user groups.

**Usage**:

```console
$ dhis2 user-group ls [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector.  [default: id,name,displayName,users]
* `--filter TEXT`: Filter &#x27;property:operator:value&#x27; (repeatable).
* `--order TEXT`: Sort clause &#x27;property:asc|desc&#x27; (repeatable).
* `--page-size INTEGER`: Server-side page size.
* `--json`: Emit JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user-group list`

List user groups.

**Usage**:

```console
$ dhis2 user-group list [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector.  [default: id,name,displayName,users]
* `--filter TEXT`: Filter &#x27;property:operator:value&#x27; (repeatable).
* `--order TEXT`: Sort clause &#x27;property:asc|desc&#x27; (repeatable).
* `--page-size INTEGER`: Server-side page size.
* `--json`: Emit JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user-group get`

Fetch one user group by UID. Prints a concise summary; `--json` for full payload.

**Usage**:

```console
$ dhis2 user-group get [OPTIONS] UID
```

**Arguments**:

* `UID`: User-group UID.  [required]

**Options**:

* `--fields TEXT`: DHIS2 field selector.
* `--json`: Emit the raw UserGroup JSON.
* `--help`: Show this message and exit.

### `dhis2 user-group add-member`

Add a user to a group (POST /api/userGroups/&lt;gid&gt;/users/&lt;uid&gt;).

**Usage**:

```console
$ dhis2 user-group add-member [OPTIONS] GROUP_UID USER_UID
```

**Arguments**:

* `GROUP_UID`: User-group UID.  [required]
* `USER_UID`: User UID to add.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 user-group remove-member`

Remove a user from a group (DELETE /api/userGroups/&lt;gid&gt;/users/&lt;uid&gt;).

**Usage**:

```console
$ dhis2 user-group remove-member [OPTIONS] GROUP_UID USER_UID
```

**Arguments**:

* `GROUP_UID`: User-group UID.  [required]
* `USER_UID`: User UID to remove.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 user-group sharing-get`

Print the current sharing block for one user group. `--json` for full payload.

**Usage**:

```console
$ dhis2 user-group sharing-get [OPTIONS] UID
```

**Arguments**:

* `UID`: User-group UID.  [required]

**Options**:

* `--json`: Emit the raw SharingObject JSON.
* `--help`: Show this message and exit.

### `dhis2 user-group sharing-grant-user`

Grant one user access to a group (shortcut over `/api/sharing`).

Preserves existing userAccesses/userGroupAccesses by fetching the current
sharing block first, then appending the new grant.

**Usage**:

```console
$ dhis2 user-group sharing-grant-user [OPTIONS] GROUP_UID USER_UID
```

**Arguments**:

* `GROUP_UID`: User-group UID.  [required]
* `USER_UID`: User UID to grant.  [required]

**Options**:

* `--metadata-write / --metadata-read`: Grant metadata write (default) or read-only.  [default: metadata-write]
* `--help`: Show this message and exit.

## `dhis2 user-role`

DHIS2 user-role administration.

**Usage**:

```console
$ dhis2 user-role [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `ls`: List user roles.
* `list`: List user roles.
* `get`: Fetch one user role by UID.
* `authorities`: Print the sorted authorities carried by...
* `add-user`: Grant a user a role (POST...
* `remove-user`: Revoke a role from a user (DELETE...

### `dhis2 user-role ls`

List user roles.

**Usage**:

```console
$ dhis2 user-role ls [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector.  [default: id,name,displayName,authorities,users]
* `--filter TEXT`: Filter (repeatable).
* `--order TEXT`: Sort clause (repeatable).
* `--page-size INTEGER`: Server-side page size.
* `--json`: Emit JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user-role list`

List user roles.

**Usage**:

```console
$ dhis2 user-role list [OPTIONS]
```

**Options**:

* `--fields TEXT`: DHIS2 field selector.  [default: id,name,displayName,authorities,users]
* `--filter TEXT`: Filter (repeatable).
* `--order TEXT`: Sort clause (repeatable).
* `--page-size INTEGER`: Server-side page size.
* `--json`: Emit JSON instead of a table.
* `--help`: Show this message and exit.

### `dhis2 user-role get`

Fetch one user role by UID. Prints a concise summary; `--json` for full payload.

**Usage**:

```console
$ dhis2 user-role get [OPTIONS] UID
```

**Arguments**:

* `UID`: User-role UID.  [required]

**Options**:

* `--fields TEXT`: DHIS2 field selector.
* `--json`: Emit the raw UserRole JSON.
* `--help`: Show this message and exit.

### `dhis2 user-role authorities`

Print the sorted authorities carried by one role, one per line.

**Usage**:

```console
$ dhis2 user-role authorities [OPTIONS] UID
```

**Arguments**:

* `UID`: User-role UID.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 user-role add-user`

Grant a user a role (POST /api/userRoles/&lt;rid&gt;/users/&lt;uid&gt;).

**Usage**:

```console
$ dhis2 user-role add-user [OPTIONS] ROLE_UID USER_UID
```

**Arguments**:

* `ROLE_UID`: User-role UID.  [required]
* `USER_UID`: User UID to grant the role to.  [required]

**Options**:

* `--help`: Show this message and exit.

### `dhis2 user-role remove-user`

Revoke a role from a user (DELETE /api/userRoles/&lt;rid&gt;/users/&lt;uid&gt;).

**Usage**:

```console
$ dhis2 user-role remove-user [OPTIONS] ROLE_UID USER_UID
```

**Arguments**:

* `ROLE_UID`: User-role UID.  [required]
* `USER_UID`: User UID to revoke the role from.  [required]

**Options**:

* `--help`: Show this message and exit.
