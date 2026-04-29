# System module

`Me`, `SystemInfo`, `DhisCalendar`, and the small `SystemModule` accessor bound to `Dhis2Client.system`.

::: dhis2_client.system

## System cache

`Dhis2Client` ships a per-client TTL-bounded cache for system-level reads.

::: dhis2_client.system_cache

## Calendar

DHIS2 ships nine canonical calendars — the names are the values DHIS2 accepts on the `keyCalendar` system setting. `DhisCalendar` enumerates them; `iso8601` is the server default.

```python
async with Dhis2Client(...) as client:
    name = await client.system.calendar()        # "iso8601" by default
    await client.system.set_calendar(DhisCalendar.ETHIOPIAN)
```

The CLI mirrors this:

```bash
dhis2 system calendar             # print current value
dhis2 system calendar ethiopian   # set new value
```

NOTE: at least on `play.im.dhis2.org/dev-2-42`, `POST /api/systemSettings/keyCalendar` returns `200 OK` with a confirming message but the value does not persist on the next read. See `BUGS.md` entry 32.
