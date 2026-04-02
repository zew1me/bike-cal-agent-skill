from __future__ import annotations

from collections.abc import Iterable

from .models import ActionPlan, CalendarEvent, PlanAction
from .normalize import build_source_key, model_to_google_body, normalized_summary


def _event_year(value: str) -> str:
    return value[:4]


def _match_existing(candidate: CalendarEvent, existing_by_key: dict[str, CalendarEvent], existing_events: list[CalendarEvent]) -> CalendarEvent | None:
    match = existing_by_key.get(candidate.source_key)
    if match is not None:
        return match
    candidate_summary = normalized_summary(candidate.summary)
    for event in existing_events:
        if normalized_summary(event.summary) == candidate_summary and _event_year(event.start) == _event_year(candidate.start):
            return event
    return None


def reconcile_family(
    *,
    family: str,
    target_year: int,
    calendar_name: str,
    existing: Iterable[CalendarEvent],
    candidates: Iterable[CalendarEvent],
) -> ActionPlan:
    existing_events = [event for event in existing if event.family == family or family == "all"]
    existing_by_key = {event.source_key: event for event in existing_events}
    actions: list[PlanAction] = []
    unresolved: list[str] = []

    for candidate in candidates:
        if not candidate.source_key:
            candidate.source_key = build_source_key(family, candidate.summary, candidate.start)
        match = _match_existing(candidate, existing_by_key, existing_events)
        payload = model_to_google_body(candidate)
        if match is None:
            actions.append(
                PlanAction(
                    action="insert",
                    family=family,
                    source_key=candidate.source_key,
                    summary=candidate.summary,
                    reason="No matching master event found.",
                    payload=payload,
                )
            )
            continue

        if model_to_google_body(match) == payload:
            actions.append(
                PlanAction(
                    action="unchanged",
                    family=family,
                    source_key=candidate.source_key,
                    summary=candidate.summary,
                    reason="Existing master event already matches normalized candidate data.",
                    payload=payload,
                    existing_event_id=match.event_id,
                )
            )
            continue

        actions.append(
            PlanAction(
                action="patch",
                family=family,
                source_key=candidate.source_key,
                summary=candidate.summary,
                reason="Matching master event exists but normalized fields differ.",
                payload=payload,
                existing_event_id=match.event_id,
            )
        )

    if not actions:
        unresolved.append(f"No candidate events were supplied for family '{family}'.")

    return ActionPlan(
        family=family,
        target_year=target_year,
        calendar=calendar_name,
        actions=actions,
        unresolved=unresolved,
    )
