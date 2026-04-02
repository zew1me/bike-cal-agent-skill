from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import CalendarEvent
from .normalize import build_source_key


@dataclass(frozen=True, slots=True)
class MountainClassicEvent:
    label: str
    summary: str
    start_date: date
    location: str
    source_url: str
    description_lines: tuple[str, ...]


MOUNTAIN_CLASSICS_2026_EVENTS: tuple[MountainClassicEvent, ...] = (
    MountainClassicEvent(
        label="Mt. Baker Hill Climb",
        summary="Mt. Baker Hill Climb",
        start_date=date(2026, 9, 13),
        location="Snowater Road to Artist Point, Glacier, WA",
        source_url="https://bakerhillclimb.com/race-information/",
        description_lines=(
            "Official 2026 race day: Sunday, September 13, 2026.",
            "All start lines begin at Snowater Road, just east of Glacier, WA, and finish at Artist Point.",
            "Official rider categories and starts are Social 7:00 am, Recreational 8:00 am, and Competitive 8:30 am.",
        ),
    ),
)


def _description_for_event(event: MountainClassicEvent) -> str:
    lines = [f"{event.summary} official 2026 source verification."]
    lines.extend(event.description_lines)
    lines.append(f"Official page: {event.source_url}")
    lines.append("High Pass Challenge remains tracked in the mountain-classics family but is excluded from this verified batch until an official 2026 page is posted.")
    return "\n".join(lines)


def fetch_mountain_classics(*, target_year: int, family: str = "mountain-classics") -> list[CalendarEvent]:
    if target_year != 2026:
        raise ValueError("The mountain classics adapter is currently curated for the verified 2026 batch only.")

    events: list[CalendarEvent] = []
    for event in MOUNTAIN_CLASSICS_2026_EVENTS:
        start_iso = event.start_date.isoformat()
        events.append(
            CalendarEvent(
                summary=event.summary,
                start=start_iso,
                end=(event.start_date + timedelta(days=1)).isoformat(),
                family=family,
                source_key=build_source_key(family, event.label, start_iso),
                all_day=True,
                description=_description_for_event(event),
                location=event.location,
                source_url=event.source_url,
            )
        )
    return events
