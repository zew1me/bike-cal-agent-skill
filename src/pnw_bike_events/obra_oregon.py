from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import CalendarEvent
from .normalize import build_source_key


OBRA_ROAD_SCHEDULE_URL = "https://obra.org/schedule/2026/list/road"
OBRA_CRITERIUM_SCHEDULE_URL = "https://obra.org/schedule/2026/criterium"


@dataclass(frozen=True, slots=True)
class ObraEvent:
    label: str
    summary: str
    start_date: date
    end_date: date
    location: str
    source_url: str
    description_lines: tuple[str, ...]


OBRA_2026_EVENTS: tuple[ObraEvent, ...] = (
    ObraEvent(
        label="Monday Night PIR",
        summary="Monday Night PIR",
        start_date=date(2026, 4, 20),
        end_date=date(2026, 6, 15),
        location="Portland International Raceway, Portland, OR",
        source_url=OBRA_ROAD_SCHEDULE_URL,
        description_lines=(
            "Official OBRA 2026 road schedule lists weekly Monday Night PIR dates from April 20 through June 15, 2026.",
            "This is a recurring Portland race series at Portland International Raceway.",
        ),
    ),
    ObraEvent(
        label="Tuesday Night PIR",
        summary="Tuesday Night PIR",
        start_date=date(2026, 5, 5),
        end_date=date(2026, 6, 9),
        location="Portland International Raceway, Portland, OR",
        source_url=OBRA_ROAD_SCHEDULE_URL,
        description_lines=(
            "Official OBRA 2026 road schedule lists weekly Tuesday Night PIR dates from May 5 through June 9, 2026.",
            "This is a recurring Portland race series at Portland International Raceway.",
        ),
    ),
    ObraEvent(
        label="Mount Tabor Circuit Race",
        summary="Mount Tabor Circuit Race",
        start_date=date(2026, 6, 3),
        end_date=date(2026, 7, 22),
        location="Mount Tabor Park, Portland, OR",
        source_url=OBRA_ROAD_SCHEDULE_URL,
        description_lines=(
            "Official OBRA 2026 road schedule lists weekly Mount Tabor Circuit Race dates from June 3 through July 22, 2026.",
            "This is a recurring Portland road race series at Mount Tabor Park.",
        ),
    ),
    ObraEvent(
        label="Barton Park Road Race",
        summary="Barton Park Road Race",
        start_date=date(2026, 5, 9),
        end_date=date(2026, 5, 9),
        location="Barton Park, OR",
        source_url=OBRA_ROAD_SCHEDULE_URL,
        description_lines=(
            "Official OBRA 2026 road schedule lists Barton Park Road Race on May 9, 2026.",
        ),
    ),
    ObraEvent(
        label="Portland Criterium",
        summary="Portland Criterium",
        start_date=date(2026, 8, 15),
        end_date=date(2026, 8, 16),
        location="Portland, OR",
        source_url=OBRA_CRITERIUM_SCHEDULE_URL,
        description_lines=(
            "Official OBRA 2026 criterium schedule lists Portland Criterium on August 15-16, 2026.",
            "The schedule specifically shows the Lloyd District OBRA Criterium Championship on the second day.",
        ),
    ),
)


def _description_for_event(event: ObraEvent) -> str:
    lines = [f"{event.summary} official 2026 source verification."]
    lines.extend(event.description_lines)
    lines.append(f"Official page: {event.source_url}")
    lines.append("This OBRA batch is intentionally limited to Oregon road and criterium events already posted on the official 2026 schedule.")
    return "\n".join(lines)


def fetch_obra_oregon_events(*, target_year: int, family: str = "obra-oregon") -> list[CalendarEvent]:
    if target_year != 2026:
        raise ValueError("The OBRA Oregon adapter is currently curated for the verified 2026 schedule batch only.")

    events: list[CalendarEvent] = []
    for event in OBRA_2026_EVENTS:
        start_iso = event.start_date.isoformat()
        events.append(
            CalendarEvent(
                summary=event.summary,
                start=start_iso,
                end=(event.end_date + timedelta(days=1)).isoformat(),
                family=family,
                source_key=build_source_key(family, event.label, start_iso),
                all_day=True,
                description=_description_for_event(event),
                location=event.location,
                source_url=event.source_url,
            )
        )
    return events
