---
name: pnw-bike-events-sync
description: Reconcile Pacific Northwest bike race and ride events into the `PNW Bike Events` Google Calendar in organizer-based batches. Use this when Codex should compare prior-season calendar entries against current official sources, build a verified batch plan, update stale links or dates, or apply inserts and patches for criteriums, road races, gravel events, major Cascade rides, RCC events, mountain classics, and cyclocross series.
---

# PNW Bike Events Sync

Use this skill to maintain the master `PNW Bike Events` calendar.

## Workflow

1. Confirm `gws` auth works and that `PNW Bike Events` resolves:
   ```bash
   gws calendar calendarList list --format table
   ```
2. Build or refresh the prior-season seed catalog:
   ```bash
   uv run python .agents/skills/pnw-bike-events-sync/scripts/build_seed_catalog.py --year 2025
   ```
3. Pick exactly one source family and read the family notes in `references/source-registry.md`.
4. Gather current-year candidate events from official pages or a manual schedule capture. For built-in source adapters:
   ```bash
   uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_ride_vicious.py --target-year 2026
   uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_cascade_major_rides.py --target-year 2026
   uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_sticky_bidon_raceways.py --target-year 2026
   uv run python .agents/skills/pnw-bike-events-sync/scripts/fetch_wider_pnw_marquee.py --target-year 2026
   ```
5. Build a reconciliation report:
   ```bash
   uv run python .agents/skills/pnw-bike-events-sync/scripts/reconcile_batch.py \
     --family ride-vicious \
     --target-year 2026 \
     --seed-catalog reports/seeds-2025.json \
     --candidates reports/ride-vicious-2026-candidates.json
   ```
6. Inspect the plan JSON before writing anything.
7. Apply the plan only when every action is verified:
   ```bash
   uv run python .agents/skills/pnw-bike-events-sync/scripts/apply_batch.py \
     --plan reports/ride-vicious-2026-plan.json
   ```
8. If the calendar already has older legacy entries for the same event, run the dedupe pass:
   ```bash
   uv run python .agents/skills/pnw-bike-events-sync/scripts/dedupe_calendar.py --match "Cascade -"
   ```

## Rules

- Process one organizer family at a time.
- Write directly to `PNW Bike Events` only for verified current-year sources.
- Leave uncertain or not-yet-posted events in the report's `unresolved` list instead of guessing.
- Preserve idempotence by storing `pnw_source_family` and `pnw_source_key` in extended properties.
- Use all-day dates unless the official source gives reliable times, such as the Pacific Raceways series schedule.

## Resources

- `scripts/build_seed_catalog.py` builds a normalized prior-season seed file from the current master calendar.
- `scripts/fetch_ride_vicious.py` fetches the current Ride Vicious batch from official source pages.
- `scripts/fetch_cascade_major_rides.py` fetches the currently posted Cascade flagship rides from official source pages.
- `scripts/fetch_sticky_bidon_raceways.py` builds the Pacific Raceways timed series from the official 2026 schedule image plus Sticky Bidon series context.
- `scripts/fetch_wider_pnw_marquee.py` builds the current verified wider-net marquee batch from official 2026 pages such as Tour de Bloom, Kettle Mettle, Tour de Whatcom, and Rebecca's Private Idaho.
- `scripts/reconcile_batch.py` compares normalized candidates against prior-season seeds and emits an insert/patch/unchanged plan.
- `scripts/apply_batch.py` applies a verified plan through `gws`.
- `scripts/dedupe_calendar.py` removes older duplicate entries while keeping the canonical synced event with `pnw_source_*` metadata.
- `references/source-registry.md` lists the default source families, URLs, and handling notes.
- `references/event-policy.md` captures which event types belong in scope.
