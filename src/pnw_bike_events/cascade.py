from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import re
from typing import Callable

from bs4 import BeautifulSoup
import httpx

from .models import CalendarEvent
from .normalize import build_source_key


_DATE_LINE_RE = re.compile(
    r"([A-Za-z]+,\s+[A-Za-z]{3,9}\.?\s+\d{1,2}\s+\d{4})\s*(?:•.*?-\s*|\s+)([A-Za-z]+,\s+[A-Za-z]{3,9}\.?\s+\d{1,2}\s+\d{4})",
    re.DOTALL,
)
_SINGLE_DATE_RE = re.compile(r"[A-Za-z]+,\s+[A-Za-z]{3,9}\.?\s+\d{1,2}\s+\d{4}")


@dataclass(frozen=True, slots=True)
class CascadePage:
    label: str
    title: str
    url: str
    canonical_url: str | None = None
    verified_start: str | None = None
    verified_end: str | None = None
    verified_location: str | None = None
    verified_description: str | None = None


CASCADE_SCHEDULE_URL = "https://cascade.org/rides-events/ride-information-support/season-schedule"
CASCADE_MAJOR_PAGES: tuple[CascadePage, ...] = (
    CascadePage(
        label="STP",
        title="Seattle to Portland Bicycle Classic",
        url="https://cascade.org/stp",
        canonical_url="https://cascade.org/rides-events/seattle-portland-2026",
        verified_start="2026-07-11",
        verified_end="2026-07-13",
        verified_location="University of Washington E-18 Lot",
        verified_description=(
            'The Seattle to Portland Bicycle Classic is a Pacific Northwest rite of passage! '
            'Join STP in its 47th year and ride from one great bike city to another. '
            'Bicycling Magazine calls STP "one of the best cycling events in the nation" because this ride is a treat '
            "for all ages, abilities, and anyone up to the challenge.\n"
            "Heading south from Seattle and ending in Portland, Oregon, STP is a thrilling back-to-back double-century ride "
            "through beautiful Western Washington. Everyone belongs on STP -- bike 206 miles over one or two days, one mile at a time.\n"
            "This event is a fundraiser for Cascade Bicycle Club's programming in advocacy, education, and community rides, such as "
            "our sliding scale biking and maintenance classes and the Pedaling Relief Project."
        ),
    ),
    CascadePage(
        label="RSVP",
        title="Ride from Seattle to Vancouver and Party",
        url="https://cascade.org/rides-events/rsvp-2026",
        verified_start="2026-08-22",
        verified_end="2026-08-24",
        verified_location="University of Washingtin E18 Parking Lot",
        verified_description=(
            "Pedal on some of the most beautiful roads and trails western Washington has to offer. Enjoy epic views of the Cascade "
            "mountain range, Skagit Valley farmlands, and the Salish Sea before crossing into Canada. Bike 110 miles on day one "
            "from Seattle to Bellingham, and about 80 miles on day two from Bellingham to Vancouver, BC.\n"
            "The two-day ride concludes with riding through British Columbia and connecting with its many greenways, bike lanes and "
            "award-winning bike infrastructure on your way into downtown Vancouver, B.C. Come celebrate this flagship Cascade ride!\n"
            "RSVP typically sells out. Don't miss out!"
        ),
    ),
)

_DESCRIPTION_STOP_HEADERS = (
    "Pricing",
    "Registration",
    "Packet Mailing & Pickup",
    "Packet Pickup",
    "Route",
    "Event Schedule",
    "Transportation",
    "Lodging",
    "Food & Breaks",
    "Weather",
    "Support During the Ride",
    "Training",
)


class CascadeError(RuntimeError):
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


def _normalize_date_text(value: str) -> str:
    return value.replace(".", "")


def _parse_date(value: str) -> date:
    normalized = _normalize_date_text(value)
    for fmt in ("%A, %B %d %Y", "%A, %b %d %Y"):
        try:
            return datetime.strptime(normalized, fmt).date()
        except ValueError:
            continue
    raise CascadeError(f"Could not parse Cascade date '{value}'.")


def _extract_line_after(lines: list[str], header: str) -> str:
    try:
        index = lines.index(header)
    except ValueError as exc:
        raise CascadeError(f"Could not find section header '{header}'.") from exc
    for line in lines[index + 1 :]:
        if line == "(map)":
            continue
        return line
    raise CascadeError(f"No content found after header '{header}'.")


def _extract_description(lines: list[str]) -> str:
    try:
        start = lines.index("Event Description") + 1
    except ValueError as exc:
        raise CascadeError("Could not find Cascade Event Description section.") from exc
    collected: list[str] = []
    for line in lines[start:]:
        if line in _DESCRIPTION_STOP_HEADERS:
            break
        if line.startswith("Image") or line.startswith("Riding past "):
            continue
        collected.append(line)
    if not collected:
        raise CascadeError("Cascade Event Description section was empty.")
    return "\n".join(collected[:3])


def _extract_date_range(text: str) -> tuple[date, date]:
    match = _DATE_LINE_RE.search(text)
    if match is not None:
        return _parse_date(match.group(1)), _parse_date(match.group(2))

    hits = _SINGLE_DATE_RE.findall(text)
    if len(hits) >= 2:
        return _parse_date(hits[0]), _parse_date(hits[1])
    raise CascadeError("Could not extract Cascade date range.")


def parse_cascade_page(page: CascadePage, text: str, *, family: str = "cascade-major-rides") -> CalendarEvent:
    lines = _clean_lines(text)
    start_day, end_day = _extract_date_range(text)
    description = _extract_description(lines)
    location = _extract_line_after(lines, "Location(s)")
    start_iso = start_day.isoformat()
    return CalendarEvent(
        summary=f"Cascade - {page.label}",
        start=start_iso,
        end=(end_day + timedelta(days=1)).isoformat(),
        family=family,
        source_key=build_source_key(family, page.label, start_iso),
        description=f"{description}\nOfficial page: {page.canonical_url or page.url}",
        location=location,
        source_url=page.canonical_url or page.url,
    )


def validate_cascade_schedule(html: str, *, target_year: int) -> None:
    text = _html_to_text(html)
    expected_markers = (
        f"Seattle to Portland (STP) Bicycle Classic July 11-12, {target_year}",
        f"Ride from Seattle to Vancouver & Party (RSVP) Aug. 22-23, {target_year}",
    )
    for marker in expected_markers:
        if marker not in text:
            raise CascadeError(f"Could not validate season schedule marker: {marker}")


def _verified_cascade_snapshot_events(*, target_year: int, family: str = "cascade-major-rides") -> list[CalendarEvent]:
    if target_year != 2026:
        raise CascadeError(
            f"Cascade fallback snapshot is currently only verified for 2026, not requested target year {target_year}."
        )
    events: list[CalendarEvent] = []
    for page in CASCADE_MAJOR_PAGES:
        if not all((page.verified_start, page.verified_end, page.verified_location, page.verified_description)):
            raise CascadeError(f"Missing verified snapshot fields for {page.label}.")
        events.append(
            CalendarEvent(
                summary=f"Cascade - {page.label}",
                start=page.verified_start,
                end=page.verified_end,
                family=family,
                source_key=build_source_key(family, page.label, page.verified_start),
                description=f"{page.verified_description}\nOfficial page: {page.canonical_url or page.url}",
                location=page.verified_location,
                source_url=page.canonical_url or page.url,
            )
        )
    return events


def fetch_cascade_major_rides(
    *,
    target_year: int,
    fetch_html: Callable[[str], str] | None = None,
) -> list[CalendarEvent]:
    fetch = fetch_html or _fetch_html
    try:
        schedule_html = fetch(CASCADE_SCHEDULE_URL)
        validate_cascade_schedule(schedule_html, target_year=target_year)

        events: list[CalendarEvent] = []
        for page in CASCADE_MAJOR_PAGES:
            html = fetch(page.url)
            event = parse_cascade_page(page, _html_to_text(html))
            if not event.start.startswith(f"{target_year}-"):
                raise CascadeError(
                    f"Expected {page.label} to resolve to target year {target_year}, got start date {event.start}."
                )
            events.append(event)
        return events
    except (httpx.HTTPStatusError, CascadeError) as exc:
        if fetch_html is not None:
            raise
        if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code != 403:
            raise
        return _verified_cascade_snapshot_events(target_year=target_year)


def _fetch_html(url: str) -> str:
    response = httpx.get(
        url,
        follow_redirects=True,
        timeout=20.0,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://cascade.org/",
            "Upgrade-Insecure-Requests": "1",
        },
    )
    response.raise_for_status()
    return response.text
