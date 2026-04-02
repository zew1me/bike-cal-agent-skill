import pytest

from pnw_bike_events.mountain_classics import fetch_mountain_classics


def test_fetch_mountain_classics_builds_verified_mt_baker_batch() -> None:
    events = fetch_mountain_classics(target_year=2026)
    assert len(events) == 1
    event = events[0]
    assert event.summary == "Mt. Baker Hill Climb"
    assert event.start == "2026-09-13"
    assert event.end == "2026-09-14"
    assert event.location == "Snowater Road to Artist Point, Glacier, WA"
    assert "High Pass Challenge remains tracked" in event.description
    assert event.family == "mountain-classics"


def test_fetch_mountain_classics_rejects_other_years() -> None:
    with pytest.raises(ValueError):
        fetch_mountain_classics(target_year=2025)
