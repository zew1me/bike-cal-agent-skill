from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import CalendarEvent
from .normalize import build_source_key


@dataclass(frozen=True, slots=True)
class WiderPnwMarqueeEvent:
    summary: str
    start_date: date
    end_date: date
    location: str
    source_url: str
    notes: tuple[str, ...]


WIDER_PNW_2026_MARQUEE_EVENTS: tuple[WiderPnwMarqueeEvent, ...] = (
    WiderPnwMarqueeEvent(
        summary="Tour de Bloom",
        start_date=date(2026, 5, 14),
        end_date=date(2026, 5, 19),
        location="Wenatchee Valley, WA",
        source_url="https://www.tourdebloom.com/",
        notes=(
            "Official 2026 Tour de Bloom dates: May 14-19, 2026.",
            "Stage race weekend based in the Wenatchee Valley.",
        ),
    ),
    WiderPnwMarqueeEvent(
        summary="Kettle Mettle Gravel Fondo",
        start_date=date(2026, 6, 20),
        end_date=date(2026, 6, 20),
        location="Princeton, BC, Canada",
        source_url="https://www.kettlemettle.ca/",
        notes=(
            "Official 2026 event date: June 20, 2026.",
            "Canadian gravel fondo in the Similkameen Valley.",
        ),
    ),
    WiderPnwMarqueeEvent(
        summary="Tour de Whatcom",
        start_date=date(2026, 7, 18),
        end_date=date(2026, 7, 18),
        location="Bellingham, WA",
        source_url="https://tourdewhatcom.com/",
        notes=(
            "Official 2026 event date: Saturday, July 18, 2026.",
            "Cascade Bicycle Club-supported ride and fundraiser for local youth programs.",
        ),
    ),
    WiderPnwMarqueeEvent(
        summary="Rebecca's Private Idaho",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12),
        location="Sun Valley, ID",
        source_url="https://www.rebeccasprivateidaho.com/",
        notes=(
            "Official 2026 main event date: September 12, 2026.",
            "The official site also shows surrounding festival activities earlier that week.",
        ),
    ),
)


def _description_for_event(event: WiderPnwMarqueeEvent) -> str:
    parts = [f"{event.summary} official 2026 source verification."]
    parts.extend(event.notes)
    parts.append(f"Official page: {event.source_url}")
    parts.append("BWR BC remains tracked in the wider-net source registry but is excluded from this verified batch until an exact 2026 date is posted on an official page.")
    return "\n".join(parts)


def _exclusive_end_date(event: WiderPnwMarqueeEvent) -> str:
    return (event.end_date + timedelta(days=1)).isoformat()


def fetch_wider_pnw_marquee_events(*, target_year: int, family: str = "wider-pnw") -> list[CalendarEvent]:
    if target_year != 2026:
        raise ValueError("The wider PNW marquee adapter is currently curated for the verified 2026 batch only.")

    events: list[CalendarEvent] = []
    for event in WIDER_PNW_2026_MARQUEE_EVENTS:
        start_iso = event.start_date.isoformat()
        summary = event.summary
        events.append(
            CalendarEvent(
                summary=summary,
                start=start_iso,
                end=_exclusive_end_date(event),
                family=family,
                source_key=build_source_key(family, summary, start_iso),
                all_day=True,
                description=_description_for_event(event),
                location=event.location,
                source_url=event.source_url,
            )
        )
    return events
