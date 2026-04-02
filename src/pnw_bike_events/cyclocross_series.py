from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import CalendarEvent
from .normalize import build_source_key


@dataclass(frozen=True, slots=True)
class CyclocrossEvent:
    label: str
    summary: str
    start_date: date
    end_date: date
    location: str
    source_url: str
    description_lines: tuple[str, ...]


UPCOMING_CYCLOCROSS_2026_EVENTS: tuple[CyclocrossEvent, ...] = (
    CyclocrossEvent(
        label="SSCXWC26BHAM",
        summary="Single Speed Cyclocross World Championship",
        start_date=date(2026, 10, 2),
        end_date=date(2026, 10, 4),
        location="Bellingham, WA",
        source_url="https://sscxwc26bham.com/",
        description_lines=(
            "Official SSCXWC26BHAM festival dates: October 2-4, 2026.",
            "Hosted in Bellingham, Washington as part of the upcoming 2026/2027 cyclocross season.",
            "This verified batch intentionally excludes January 2026 races from the prior 2025/2026 season.",
        ),
    ),
)


def _description_for_event(event: CyclocrossEvent) -> str:
    lines = [f"{event.summary} official 2026 source verification."]
    lines.extend(event.description_lines)
    lines.append(f"Official page: {event.source_url}")
    lines.append("Additional MFG, CXR, Lemon Peel, and other 2026/2027 series races should be added once official schedules post.")
    return "\n".join(lines)


def fetch_cyclocross_series(*, target_year: int, family: str = "cyclocross-series") -> list[CalendarEvent]:
    if target_year != 2026:
        raise ValueError("The cyclocross-series adapter is currently curated for the verified 2026/2027 season batch only.")

    events: list[CalendarEvent] = []
    for event in UPCOMING_CYCLOCROSS_2026_EVENTS:
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
