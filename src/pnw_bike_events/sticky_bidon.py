from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .models import CalendarEvent
from .normalize import build_source_key


_PACIFIC = ZoneInfo("America/Los_Angeles")
_DEFAULT_RACE_DURATION = timedelta(minutes=75)
_SOURCE_URL = "https://www.stickybidon.com/"
_LOCATION = "Pacific Raceways, Kent, WA"


@dataclass(frozen=True, slots=True)
class StickyBidonRace:
    phase: str
    round_label: str
    race_label: str
    race_date: date
    course: str
    start_time: str
    event_label: str = ""


STICKY_BIDON_2026_RACES: tuple[StickyBidonRace, ...] = (
    StickyBidonRace("regular-season", "Round 1", "Race 1", date(2026, 4, 7), "Flat", "5:30", "Season Kickoff"),
    StickyBidonRace("regular-season", "Round 1", "Race 2", date(2026, 4, 7), "Flat", "6:45", "Season Kickoff"),
    StickyBidonRace("regular-season", "Round 2", "Race 1", date(2026, 5, 26), "Escape Route", "5:45"),
    StickyBidonRace("regular-season", "Round 2", "Race 2", date(2026, 5, 26), "Escape Route", "7:00"),
    StickyBidonRace("regular-season", "Round 3", "Race 1", date(2026, 6, 16), "Flat", "5:45", "WSBA Champs Night"),
    StickyBidonRace("regular-season", "Round 3", "Race 2", date(2026, 6, 16), "Flat", "7:00", "WSBA Champs Night"),
    StickyBidonRace("regular-season", "Round 4", "Race 1", date(2026, 6, 23), "Reverse S Bend", "5:45"),
    StickyBidonRace("regular-season", "Round 4", "Race 2", date(2026, 6, 23), "Reverse S Bend", "7:00"),
    StickyBidonRace("regular-season", "Round 5", "Race 1", date(2026, 6, 30), "Flat", "5:45", "Birthday Party"),
    StickyBidonRace("regular-season", "Round 5", "Race 2", date(2026, 6, 30), "Flat", "7:00", "Birthday Party"),
    StickyBidonRace("regular-season", "Round 6", "Race 1", date(2026, 7, 7), "Escape Route", "5:45"),
    StickyBidonRace("regular-season", "Round 6", "Race 2", date(2026, 7, 7), "Escape Route", "7:00"),
    StickyBidonRace("regular-season", "Round 7", "Race 1", date(2026, 7, 14), "Flat", "5:45", "Haley Insurance Night"),
    StickyBidonRace("regular-season", "Round 7", "Race 2", date(2026, 7, 14), "Flat", "7:00", "Haley Insurance Night"),
    StickyBidonRace("regular-season", "Round 8", "Race 1", date(2026, 8, 11), "Reverse S Bend", "5:45"),
    StickyBidonRace("regular-season", "Round 8", "Race 2", date(2026, 8, 11), "Reverse S Bend", "7:00"),
    StickyBidonRace("regular-season", "Round 9", "Race 1", date(2026, 8, 25), "Flat", "5:30"),
    StickyBidonRace("regular-season", "Round 9", "Race 2", date(2026, 8, 25), "Flat", "6:45"),
    StickyBidonRace("regular-season", "Round 10", "Race 1", date(2026, 9, 1), "Escape Route", "5:30", "Season Finale"),
    StickyBidonRace("regular-season", "Round 10", "Race 2", date(2026, 9, 1), "Escape Route", "6:45", "Season Finale"),
    StickyBidonRace("post-season", "Post Season 1", "Race 1", date(2026, 9, 8), "Flat", "6:00", "Post Season"),
    StickyBidonRace("post-season", "Post Season 2", "Race 1", date(2026, 9, 15), "Escape Route", "6:00", "Post Season"),
)


def _parse_clock(value: str) -> time:
    hour_text, minute_text = value.split(":")
    hour = int(hour_text)
    minute = int(minute_text)
    if hour < 8:
        hour += 12
    return time(hour=hour, minute=minute)


def _build_datetimes(race_date: date, start_time: str) -> tuple[str, str]:
    start_dt = datetime.combine(race_date, _parse_clock(start_time), tzinfo=_PACIFIC)
    end_dt = start_dt + _DEFAULT_RACE_DURATION
    return start_dt.isoformat(), end_dt.isoformat()


def _summary_for_race(race: StickyBidonRace) -> str:
    if race.phase == "post-season":
        return f"Pacific Raceways Circuit Races - {race.round_label}"
    return f"Pacific Raceways Circuit Races - {race.round_label} {race.race_label}"


def _description_for_race(race: StickyBidonRace) -> str:
    parts = [
        "Sticky Bidon Pacific Raceways Circuit Race Series 2026.",
        f"Phase: {race.phase.replace('-', ' ').title()}",
        f"Course: {race.course}",
        f"Scheduled start: {race.start_time} America/Los_Angeles",
    ]
    if race.event_label:
        parts.append(f"Series note: {race.event_label}")
    parts.append("Official series page: https://www.stickybidon.com/")
    parts.append("Schedule timing taken from the official 2026 Pacific Raceways series graphic provided for this repo.")
    return "\n".join(parts)


def fetch_sticky_bidon_raceways(*, target_year: int, family: str = "sticky-bidon-raceways") -> list[CalendarEvent]:
    if target_year != 2026:
        raise ValueError("Sticky Bidon raceways adapter is currently configured for the 2026 image-backed schedule only.")

    events: list[CalendarEvent] = []
    for race in STICKY_BIDON_2026_RACES:
        start_iso, end_iso = _build_datetimes(race.race_date, race.start_time)
        summary = _summary_for_race(race)
        events.append(
            CalendarEvent(
                summary=summary,
                start=start_iso,
                end=end_iso,
                family=family,
                source_key=build_source_key(family, summary, start_iso),
                all_day=False,
                timezone="America/Los_Angeles",
                description=_description_for_race(race),
                location=_LOCATION,
                source_url=_SOURCE_URL,
            )
        )
    return events
