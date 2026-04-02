from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import date

from .calendar_cli import delete_event, list_events
from .models import CalendarEvent, DedupeResult
from .normalize import google_event_to_model, normalized_summary


def _event_year(value: str) -> str:
    return value[:4]


def _canonical_score(event: CalendarEvent) -> tuple[int, int, int]:
    private = event.extended_private
    score = 0
    if private.get("pnw_source_key"):
        score += 100
    if private.get("pnw_source_url"):
        score += 20
    if event.source_url:
        score += 10
    if event.summary == event.summary.strip():
        score += 1
    return (score, len(event.description), -len(event.start))


def dedupe_candidates(events: Iterable[CalendarEvent]) -> list[tuple[CalendarEvent, CalendarEvent]]:
    groups: dict[tuple[str, str], list[CalendarEvent]] = defaultdict(list)
    for event in events:
        groups[(normalized_summary(event.summary), _event_year(event.start))].append(event)

    duplicates: list[tuple[CalendarEvent, CalendarEvent]] = []
    for grouped in groups.values():
        if len(grouped) < 2:
            continue
        ordered = sorted(grouped, key=_canonical_score, reverse=True)
        keep = ordered[0]
        for loser in ordered[1:]:
            duplicates.append((keep, loser))
    return duplicates


def dedupe_calendar(
    *,
    calendar_name: str,
    match_text: str | None = None,
    time_min: str | None = None,
    time_max: str | None = None,
    dry_run: bool = False,
) -> list[DedupeResult]:
    start = time_min or f"{date.today().year}-01-01T00:00:00-08:00"
    end = time_max or f"{date.today().year + 1}-12-31T23:59:59-08:00"
    items = list_events(calendar_name, time_min=start, time_max=end, q=match_text)
    events = [google_event_to_model(item) for item in items]

    results: list[DedupeResult] = []
    for keep, delete in dedupe_candidates(events):
        delete_event(calendar_name, delete.event_id or "", dry_run=dry_run)
        reason = "Kept canonical event with pnw_source metadata." if keep.extended_private.get("pnw_source_key") else "Kept higher-quality duplicate."
        results.append(
            DedupeResult(
                calendar=calendar_name,
                summary=keep.summary.strip(),
                year=_event_year(keep.start),
                kept_event_id=keep.event_id or "",
                deleted_event_id=delete.event_id or "",
                action="delete" if not dry_run else "dry-run-delete",
                reason=reason,
            )
        )
    return results
