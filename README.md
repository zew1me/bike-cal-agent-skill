# PNW Bike Events

This repo builds Codex-native skills for maintaining cycling events across three Google Calendars:

- `PNW Bike Events` as the master seasonal calendar
- `Tentative Calendar` for planning candidates
- `primary` for events you actually want on your personal calendar

The repo has two local skills backed by one shared Python package:

- `.agents/skills/pnw-bike-events-sync/` reconciles prior-season events against current sources in organizer batches
- `.agents/skills/pnw-bike-events-promote/` clones and syncs selected master events into `Tentative Calendar` or `primary`
- `src/pnw_bike_events/` holds the shared registry, normalization, diffing, and Google Calendar wrappers both skills use

## Setup

```bash
uv sync --extra dev
```

The workflows rely on the `gws` CLI already being installed and authenticated:

```bash
gws auth login
gws calendar calendarList list --format table
```

## Build And Test

```bash
uv run pytest
uv run --extra dev python -m build --no-isolation
uv run python -m py_compile src/pnw_bike_events/*.py \
  .agents/skills/pnw-bike-events-sync/scripts/*.py \
  .agents/skills/pnw-bike-events-promote/scripts/*.py
```

## Main Workflows

Build a prior-season seed catalog from the master calendar:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/build_seed_catalog.py \
  --year 2025 \
  --output reports/seeds-2025.json
```

Prepare a reconciliation report for one organizer family:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_ride_vicious.py \
  --target-year 2026 \
  --output reports/ride-vicious-2026-candidates.json
```

Then reconcile that live official-source batch against the prior-season seeds:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/reconcile_batch.py \
  --family ride-vicious \
  --target-year 2026 \
  --seed-catalog reports/seeds-2025.json \
  --candidates reports/ride-vicious-2026-candidates.json \
  --output reports/ride-vicious-2026-plan.json
```

Fetch the posted Cascade major rides batch from official pages:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_cascade_major_rides.py \
  --target-year 2026 \
  --output reports/cascade-major-rides-2026-candidates.json
```

Then reconcile that batch:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/reconcile_batch.py \
  --family cascade-major-rides \
  --target-year 2026 \
  --seed-catalog reports/seeds-2025.json \
  --candidates reports/cascade-major-rides-2026-candidates.json \
  --output reports/cascade-major-rides-2026-plan.json
```

Build the Sticky Bidon / Pacific Raceways race series from the official 2026 schedule graphic:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_sticky_bidon_raceways.py \
  --target-year 2026 \
  --output reports/sticky-bidon-raceways-2026-candidates.json
```

Then reconcile that batch:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/reconcile_batch.py \
  --family sticky-bidon-raceways \
  --target-year 2026 \
  --seed-catalog reports/seeds-2025.json \
  --candidates reports/sticky-bidon-raceways-2026-candidates.json \
  --output reports/sticky-bidon-raceways-2026-plan.json
```

Apply a verified batch to `PNW Bike Events`:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/apply_batch.py \
  --plan reports/ride-vicious-2026-plan.json
```

Promote or refresh linked copies on another calendar:

```bash
uv run python .agents/skills/pnw-bike-events-promote/scripts/promote_events.py \
  --destination "Tentative Calendar" \
  --match "Vicious"
```

Use `--dry-run` on the apply and promote scripts to inspect actions without writing changes.

Clean up legacy duplicates after inserting canonical synced events:

```bash
uv run python .agents/skills/pnw-bike-events-sync/scripts/dedupe_calendar.py \
  --calendar "PNW Bike Events" \
  --match "Cascade -" \
  --time-min "2026-07-01T00:00:00-07:00" \
  --time-max "2026-09-01T00:00:00-07:00"
```

## Calendars

The code resolves these calendars dynamically by summary:

- `PNW Bike Events`
- `Tentative Calendar`
- `primary`

That keeps the repo portable and avoids hard-coding personal calendar ids in tracked files.
