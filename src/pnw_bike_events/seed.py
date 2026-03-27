from __future__ import annotations

from datetime import date

from .calendar_cli import list_events
from .models import CalendarEvent
from .normalize import google_event_to_model


def build_seed_catalog(year: int, calendar_name: str = "PNW Bike Events") -> list[CalendarEvent]:
    time_min = f"{year}-01-01T00:00:00-08:00"
    time_max = f"{year + 1}-01-01T00:00:00-08:00"
    return [google_event_to_model(item) for item in list_events(calendar_name, time_min=time_min, time_max=time_max)]


def future_window_start() -> str:
    return date.today().isoformat()

