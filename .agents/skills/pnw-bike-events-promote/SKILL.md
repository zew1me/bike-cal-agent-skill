---
name: pnw-bike-events-promote
description: Clone and sync selected events from the `PNW Bike Events` master calendar into `Tentative Calendar` or the primary calendar without changing the master event organizer. Use this when Codex should promote bike events for personal planning, refresh linked copies after the master calendar changes, or keep tentative and committed calendars aligned with the source event.
---

# PNW Bike Events Promote

Use this skill after the master calendar is up to date.

## Workflow

1. Confirm the source calendar already contains the events you want to plan around.
2. Decide the destination:
   - `Tentative Calendar` for maybes
   - `primary` for committed events
3. Promote matching events:
   ```bash
   uv run python .agents/skills/pnw-bike-events-promote/scripts/promote_events.py \
     --destination "Tentative Calendar" \
     --match "Vicious"
   ```
4. Re-run the same command later to refresh linked copies instead of creating duplicates.

## Rules

- Do not use Google Calendar `events.move` for personal planning copies.
- Store `pnw_master_event_id` on promoted events so reruns patch the existing copy.
- Keep summary, date, description, location, and source metadata synced from the master event.
- Use `--dry-run` first when the search term is broad.

## Resources

- `scripts/promote_events.py` creates or refreshes linked copies on the destination calendar.
- `references/promotion-policy.md` documents destination semantics and recommended promotion patterns.
