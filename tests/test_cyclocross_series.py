import pytest

from pnw_bike_events.cyclocross_series import fetch_cyclocross_series


def test_fetch_cyclocross_series_builds_sscxwc_batch() -> None:
    events = fetch_cyclocross_series(target_year=2026)
    assert len(events) == 1
    event = events[0]
    assert event.summary == "Single Speed Cyclocross World Championship"
    assert event.start == "2026-10-02"
    assert event.end == "2026-10-05"
    assert event.location == "Bellingham, WA"
    assert "October 2-4, 2026" in event.description
    assert "prior 2025/2026 season" in event.description
    assert event.family == "cyclocross-series"


def test_fetch_cyclocross_series_rejects_other_years() -> None:
    with pytest.raises(ValueError):
        fetch_cyclocross_series(target_year=2025)
