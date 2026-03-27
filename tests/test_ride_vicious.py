from pnw_bike_events.ride_vicious import (
    RIDE_VICIOUS_PAGES,
    RideViciousPage,
    fetch_ride_vicious_events,
    parse_ride_vicious_page,
)


SAMPLE_PAGE = """
Cycling and Event Promotion
Heaven of the South
Kicking off the Vicious Cycle Gravel Fondo Series, Heaven of the South promises to leave its mark.
The Core Details
Date: Sunday, March 29th 2026
Location: Southridge High School, Kennewick, WA
Start time:
Grande – 9:00 am
Medio – 10:00 am
Length:
Grande: 85 miles
"""


def test_parse_ride_vicious_page_extracts_fields() -> None:
    event = parse_ride_vicious_page(
        RideViciousPage("Heaven of the South", "https://www.rideviciouscycle.com/heaven-of-the-south"),
        SAMPLE_PAGE,
    )
    assert event.summary == "Vicious - Heaven of the South"
    assert event.start == "2026-03-29"
    assert event.end == "2026-03-30"
    assert event.location == "Southridge High School, Kennewick, WA"
    assert "Start times: Grande – 9:00 am; Medio – 10:00 am" in event.description


def test_fetch_ride_vicious_events_uses_official_page_list() -> None:
    pages = {
        "https://www.rideviciouscycle.com/": "<html><body><h2>2026 Schedule</h2></body></html>",
    }
    dates = [
        "Sunday, March 29th 2026",
        "Sunday, April 12th 2026",
        "Sunday, May 3rd 2026",
        "Sunday, May 17th 2026",
        "Saturday, June 6th 2026",
        "Saturday, September 26th 2026",
    ]
    locations = [
        "Southridge High School, Kennewick, WA",
        "Ephrata High School",
        "Goldendale High school",
        "Cascade High School, Leavenworth WA",
        "Dru Bru Cle Elum",
        "Twisp Park",
    ]
    for page, event_date, location in zip(RIDE_VICIOUS_PAGES, dates, locations, strict=True):
        pages[page.url] = (
            f"<html><body><h1>{page.title}</h1>"
            f"<p>A marquee Ride Vicious event.</p>"
            f"<h2>The Core Details</h2>"
            f"<p>Date: {event_date}</p>"
            f"<p>Meet: {location}</p>"
            f"<p>Start time:</p>"
            f"<p>Grande – 9:00 am</p>"
            f"<p>Medio – 10:00 am</p>"
            f"<p>Length:</p>"
            f"</body></html>"
        )

    events = fetch_ride_vicious_events(target_year=2026, fetch_html=pages.__getitem__)
    assert len(events) == len(RIDE_VICIOUS_PAGES)
    assert events[0].source_url == RIDE_VICIOUS_PAGES[0].url
    assert events[-1].summary == "Vicious - Twisp River Rambler"
