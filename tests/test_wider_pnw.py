import pytest

from pnw_bike_events.wider_pnw import fetch_wider_pnw_marquee_events


def test_fetch_wider_pnw_marquee_events_builds_verified_batch() -> None:
    events = fetch_wider_pnw_marquee_events(target_year=2026)
    assert [event.summary for event in events] == [
        "Tour de Bloom",
        "Kettle Mettle Gravel Fondo",
        "Tour de Whatcom",
        "Rebecca's Private Idaho",
    ]
    assert events[0].start == "2026-05-14"
    assert events[0].end == "2026-05-20"
    assert events[1].location == "Princeton, BC, Canada"
    assert events[2].source_url == "https://tourdewhatcom.com/"
    assert "September 12, 2026" in events[3].description
    assert all(event.family == "wider-pnw" for event in events)


def test_fetch_wider_pnw_marquee_events_rejects_other_years() -> None:
    with pytest.raises(ValueError):
        fetch_wider_pnw_marquee_events(target_year=2025)
