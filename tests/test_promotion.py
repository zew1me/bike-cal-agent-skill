from pnw_bike_events.models import CalendarEvent
from pnw_bike_events.promotion import build_promoted_copy


def test_build_promoted_copy_sets_master_link_metadata() -> None:
    source = CalendarEvent(
        summary="Vicious - Heaven of the South",
        start="2026-03-01",
        end="2026-03-02",
        family="ride-vicious",
        source_key="vicious-heaven-of-the-south-2026",
        event_id="master123",
        description="Official page",
    )
    body = build_promoted_copy(source, "Tentative Calendar")
    private_props = body["extendedProperties"]["private"]
    assert private_props["pnw_master_event_id"] == "master123"
    assert private_props["pnw_destination_role"] == "Tentative Calendar"

