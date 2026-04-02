from pnw_bike_events.dedupe import dedupe_candidates
from pnw_bike_events.models import CalendarEvent


def test_dedupe_candidates_prefers_canonical_metadata_event() -> None:
    canonical = CalendarEvent(
        summary="Cascade - STP",
        start="2026-07-11",
        end="2026-07-13",
        family="cascade-major-rides",
        source_key="stp-1ddeb8a32c15",
        event_id="canonical",
        description="Official current description",
        source_url="https://cascade.org/rides-events/seattle-portland-2026",
        extended_private={"pnw_source_key": "stp-1ddeb8a32c15", "pnw_source_url": "https://cascade.org/rides-events/seattle-portland-2026"},
    )
    legacy = CalendarEvent(
        summary="Cascade - STP ",
        start="2026-07-18",
        end="2026-07-20",
        family="cascade-major-rides",
        source_key="legacy-stp",
        event_id="legacy",
        description="Old link",
    )

    results = dedupe_candidates([legacy, canonical])
    assert results == [(canonical, legacy)]
