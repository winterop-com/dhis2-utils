# Generated-model helpers

Version selection + module loading for the codegen-produced modules (`dhis2w_client.generated.v{N}`). The hand-written client + plugin trees use these helpers when they need typed access to a specific DHIS2 major's wire shape.

## When to reach for it

- Picking the right schema module at runtime when you don't know which DHIS2 version the connected instance is running.
- Importing a v43-only model directly (e.g. when the v42-typed accessor doesn't surface a v43-only field — see [Schema diff: v41 -> v42 -> v43](../architecture/schema-diff-v41-v42-v43.md)).
- Checking which generated versions a particular `dhis2w-client` install carries (codegen is per-version + opt-in; not every build has every tree).

## Worked example — pick a generated module by version

```python
from dhis2w_client import Dhis2
from dhis2w_client.generated import available_versions, load

# Which versions has this install committed?
print(available_versions())  # e.g. ['v41', 'v42', 'v43']

# Load one by enum.
gen_v43 = load(Dhis2.V43)
print(gen_v43.__name__)  # 'dhis2w_client.generated.v43'

# Read a specific v43 schema typed.
from dhis2w_client.generated.v43.schemas.program import Program as ProgramV43

# `Program` here is the v43-typed model with `enableChangeLog`,
# `enrollmentsLabel`, etc. — fields that don't exist on the v42 model.
```

## Pairs with the version-aware client

The top-level `Dhis2Client` auto-detects the connected DHIS2 version on `connect()` and binds the matching generated module to `client.resources`, `client.models`, etc. Read [Version-aware clients](../architecture/versioning.md) for the runtime dispatch story; the helpers here are the low-level building blocks the dispatcher uses.

::: dhis2w_client.generated
