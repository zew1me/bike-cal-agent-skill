from pnw_bike_events.sticky_bidon import fetch_sticky_bidon_raceways
from pnw_bike_events.normalize import model_to_google_body


def test_fetch_sticky_bidon_raceways_builds_timed_series() -> None:
    events = fetch_sticky_bidon_raceways(target_year=2026)
    assert len(events) == 22
    assert events[0].summary == "Pacific Raceways Circuit Races - Round 1 Race 1"
    assert events[0].start == "2026-04-07T17:30:00-07:00"
    assert events[0].end == "2026-04-07T18:45:00-07:00"
    assert events[0].all_day is False
    assert events[0].timezone == "America/Los_Angeles"
    assert events[-1].summary == "Pacific Raceways Circuit Races - Post Season 2"
    assert "official 2026 Pacific Raceways series graphic" in events[-1].description


def test_timed_event_body_includes_timezone_metadata() -> None:
    event = fetch_sticky_bidon_raceways(target_year=2026)[0]
    body = model_to_google_body(event)
    assert body["start"]["timeZone"] == "America/Los_Angeles"
    assert body["end"]["timeZone"] == "America/Los_Angeles"
