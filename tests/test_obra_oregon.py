import pytest

from pnw_bike_events.obra_oregon import fetch_obra_oregon_events


def test_fetch_obra_oregon_events_builds_verified_batch() -> None:
    events = fetch_obra_oregon_events(target_year=2026)
    assert [event.summary for event in events] == [
        "Monday Night PIR",
        "Tuesday Night PIR",
        "Mount Tabor Circuit Race",
        "Barton Park Road Race",
        "Portland Criterium",
    ]
    assert events[0].start == "2026-04-20"
    assert events[0].end == "2026-06-16"
    assert events[-1].start == "2026-08-15"
    assert events[-1].end == "2026-08-17"
    assert all(event.family == "obra-oregon" for event in events)


def test_fetch_obra_oregon_events_rejects_other_years() -> None:
    with pytest.raises(ValueError):
        fetch_obra_oregon_events(target_year=2025)
