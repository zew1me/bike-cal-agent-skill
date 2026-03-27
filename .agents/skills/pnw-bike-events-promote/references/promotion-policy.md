# Promotion Policy

Promotion semantics:

- `PNW Bike Events` remains the source of truth.
- Promoted events are linked copies, not moved organizers.
- `Tentative Calendar` is for maybes and soft planning.
- `primary` is for committed plans.

Update policy:

- Match destination events by `pnw_master_event_id`.
- Patch existing linked copies when they already exist.
- Avoid free-text duplicate detection when a linked copy exists.
- Use `--dry-run` before promoting a broad search term.
