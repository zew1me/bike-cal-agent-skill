# PNW Bike Events Repo

This repository is organized around Codex skills plus a shared Python package.

## Layout

- `.agents/skills/` is the canonical skill source for local Codex discovery.
- `src/pnw_bike_events/` contains the shared logic used by both skills.
- `tests/` contains unit tests for normalization, diffing, and promotion behavior.
- `reports/` is for generated JSON plans and seed catalogs and should be treated as ephemeral output.

## Working Rules

- Keep reusable logic in `src/pnw_bike_events/`; keep skill scripts as thin wrappers.
- Prefer dynamic calendar lookup by summary over checked-in calendar ids.
- Store link metadata in Google Calendar extended properties so updates remain idempotent.
- Keep skill instructions concise and move detailed source notes into each skill's `references/`.

## Tooling

- Use `uv` for dependency management and command execution.
- Run `uv sync --extra dev` after cloning or when dependencies change.
- Run `uv run pytest`.
- Run `uv run --extra dev python -m build --no-isolation`.
- Run `uv run python -m py_compile src/pnw_bike_events/*.py .agents/skills/pnw-bike-events-sync/scripts/*.py .agents/skills/pnw-bike-events-promote/scripts/*.py`.

## Entry Points

- `uv run python .agents/skills/pnw-bike-events-sync/scripts/build_seed_catalog.py --year 2025`
- `uv run python .agents/skills/pnw-bike-events-sync/scripts/reconcile_batch.py --family ride-vicious --target-year 2026 --seed-catalog reports/seeds-2025.json --candidates tests/fixtures/ride_vicious_2026.json`
- `uv run python .agents/skills/pnw-bike-events-sync/scripts/apply_batch.py --plan reports/ride-vicious-2026-plan.json`
- `uv run python .agents/skills/pnw-bike-events-promote/scripts/promote_events.py --destination "Tentative Calendar" --match "Vicious"`

## Recurring Observations

- `gws calendar events move` is not the right primitive for personal planning copies because it changes the organizer and leaves a cancelled stub behind on the source calendar.
- Promotion should clone and sync linked copies using extended properties instead of literally moving the master event.
- Reconciliation is meant to run in organizer batches, not as one large blind scrape.
