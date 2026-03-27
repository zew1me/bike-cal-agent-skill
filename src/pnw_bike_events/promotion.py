from __future__ import annotations

from datetime import date

from .calendar_cli import insert_event, list_events, patch_event
from .models import CalendarEvent, PromotionResult
from .normalize import google_event_to_model, model_to_google_body


def _promotion_property(source_event_id: str) -> str:
    return f"pnw_master_event_id={source_event_id}"


def build_promoted_copy(source: CalendarEvent, destination_label: str) -> dict:
    promoted = CalendarEvent(
        summary=source.summary,
        start=source.start,
        end=source.end,
        family=source.family,
        source_key=source.source_key,
        all_day=source.all_day,
        description=source.description,
        location=source.location,
        source_url=source.source_url,
        status=source.status,
        transparency=source.transparency,
        extended_private={
            "pnw_master_event_id": source.event_id or "",
            "pnw_destination_role": destination_label,
        },
    )
    return model_to_google_body(promoted)


def promote_matching_events(
    *,
    source_calendar: str,
    destination_calendar: str,
    match_text: str,
    dry_run: bool = False,
) -> list[PromotionResult]:
    today = date.today().isoformat()
    next_year = f"{date.today().year + 1}-12-31"
    source_events = [
        google_event_to_model(item)
        for item in list_events(
            source_calendar,
            time_min=f"{today}T00:00:00-08:00",
            time_max=f"{next_year}T23:59:59-08:00",
            q=match_text,
        )
    ]
    results: list[PromotionResult] = []
    for source in source_events:
        property_filter = _promotion_property(source.event_id or "")
        destination_matches = list_events(
            destination_calendar,
            time_min=f"{today}T00:00:00-08:00",
            time_max=f"{next_year}T23:59:59-08:00",
            private_extended_property=property_filter,
        )
        body = build_promoted_copy(source, destination_calendar)
        if destination_matches:
            existing_id = destination_matches[0]["id"]
            patch_event(destination_calendar, existing_id, body, dry_run=dry_run)
            results.append(
                PromotionResult(
                    destination=destination_calendar,
                    source_event_id=source.event_id or "",
                    summary=source.summary,
                    action="patch",
                    destination_event_id=existing_id,
                )
            )
            continue

        created = insert_event(destination_calendar, body, dry_run=dry_run)
        results.append(
            PromotionResult(
                destination=destination_calendar,
                source_event_id=source.event_id or "",
                summary=source.summary,
                action="insert",
                destination_event_id=created.get("id"),
            )
        )
    return results

