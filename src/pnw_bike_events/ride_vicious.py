from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import re
from typing import Callable

from bs4 import BeautifulSoup
import httpx

from .models import CalendarEvent
from .normalize import build_source_key


_DATE_RE = re.compile(r"Date:\s*([A-Za-z]+,\s+[A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)\s+\d{4})")
_LOCATION_RE = re.compile(r"(?:Location|Meet):\s*(.+)")
_YEAR_RE = re.compile(r"\b(20\d{2})\s+Schedule\b")
_ORDINAL_RE = re.compile(r"(\d+)(st|nd|rd|th)")


@dataclass(frozen=True, slots=True)
class RideViciousPage:
    title: str
    url: str


RIDE_VICIOUS_PAGES: tuple[RideViciousPage, ...] = (
    RideViciousPage("Heaven of the South", "https://www.rideviciouscycle.com/heaven-of-the-south"),
    RideViciousPage("Gran Fondo Ephrata", "https://www.rideviciouscycle.com/gran-fondo-ephrata"),
    RideViciousPage("Wahkiacus Gravel Premier", "https://www.rideviciouscycle.com/wahkiacus-gravel-premier"),
    RideViciousPage("Gran Fondo Leavenworth", "https://www.rideviciouscycle.com/gran-fondo-leavenworth"),
    RideViciousPage("HI90 Grindy", "https://www.rideviciouscycle.com/hi90-grindy"),
    RideViciousPage("Twisp River Rambler", "https://www.rideviciouscycle.com/twisp-river-rambler"),
)


class RideViciousError(RuntimeError):
    pass


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text("\n")


def _clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if line:
            lines.append(line)
    return lines


def _parse_date(date_text: str) -> date:
    cleaned = _ORDINAL_RE.sub(r"\1", date_text)
    return datetime.strptime(cleaned, "%A, %B %d %Y").date()


def _extract_section(lines: list[str], header: str, stop_headers: tuple[str, ...]) -> list[str]:
    try:
        start = lines.index(header) + 1
    except ValueError as exc:
        raise RideViciousError(f"Could not find section header '{header}'.") from exc
    collected: list[str] = []
    for line in lines[start:]:
        if line in stop_headers:
            break
        collected.append(line)
    return collected


def _parse_intro(lines: list[str], title: str) -> str:
    try:
        core_index = lines.index("The Core Details")
    except ValueError:
        return ""

    title_index = -1
    for index, line in enumerate(lines[:core_index]):
        if line == title:
            title_index = index
    if title_index == -1:
        return ""

    for line in lines[title_index + 1 : core_index]:
        if len(line) > 20 and line not in {"Use tab to navigate through the menu items.", "Cycling and Event Promotion"}:
            return line
    return ""


def _parse_start_times(lines: list[str]) -> str:
    section = _extract_section(lines, "Start time:", ("Length:", "Price:", "Registration: Opens Jan 1st"))
    return "; ".join(section)


def parse_ride_vicious_page(page: RideViciousPage, text: str, *, family: str = "ride-vicious") -> CalendarEvent:
    lines = _clean_lines(text)
    intro = _parse_intro(lines, page.title)
    date_match = _DATE_RE.search(text)
    if date_match is None:
        raise RideViciousError(f"Could not parse date for {page.title}.")
    day = _parse_date(date_match.group(1))

    location_match = _LOCATION_RE.search(text)
    if location_match is None:
        raise RideViciousError(f"Could not parse location for {page.title}.")
    location = location_match.group(1).strip()

    start_times = _parse_start_times(lines)
    description_parts = [part for part in (intro, f"Official page: {page.url}", f"Start times: {start_times}") if part]
    start_iso = day.isoformat()
    return CalendarEvent(
        summary=f"Vicious - {page.title}",
        start=start_iso,
        end=(day + timedelta(days=1)).isoformat(),
        family=family,
        source_key=build_source_key(family, page.title, start_iso),
        description="\n".join(description_parts),
        location=location,
        source_url=page.url,
    )


def validate_ride_vicious_homepage(html: str, *, target_year: int) -> None:
    text = _html_to_text(html)
    match = _YEAR_RE.search(text)
    if match is None:
        raise RideViciousError("Could not find Ride Vicious schedule year on the homepage.")
    published_year = int(match.group(1))
    if published_year != target_year:
        raise RideViciousError(
            f"Ride Vicious homepage schedule is for {published_year}, not requested target year {target_year}."
        )


def fetch_ride_vicious_events(
    *,
    target_year: int,
    fetch_html: Callable[[str], str] | None = None,
) -> list[CalendarEvent]:
    fetch = fetch_html or _fetch_html
    homepage_html = fetch("https://www.rideviciouscycle.com/")
    validate_ride_vicious_homepage(homepage_html, target_year=target_year)

    events: list[CalendarEvent] = []
    for page in RIDE_VICIOUS_PAGES:
        html = fetch(page.url)
        event = parse_ride_vicious_page(page, _html_to_text(html))
        if not event.start.startswith(f"{target_year}-"):
            raise RideViciousError(
                f"Expected {page.title} to resolve to target year {target_year}, got start date {event.start}."
            )
        events.append(event)
    return events


def _fetch_html(url: str) -> str:
    response = httpx.get(
        url,
        follow_redirects=True,
        timeout=20.0,
        headers={"User-Agent": "pnw-bike-events/0.1 (+https://www.rideviciouscycle.com/)"},
    )
    response.raise_for_status()
    return response.text
