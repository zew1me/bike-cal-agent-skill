import json
from pathlib import Path

from pnw_bike_events.diffing import reconcile_family
from pnw_bike_events.models import CalendarEvent


def test_reconcile_family_creates_insert_and_patch_actions() -> None:
    existing = [
        CalendarEvent(
            summary="Vicious - Heaven of the South",
            start="2025-03-02",
            end="2025-03-03",
            family="ride-vicious",
            source_key="vicious-heaven-of-the-south-2026",
            description="Old description",
            event_id="abc123",
        )
    ]
    candidates = [
        CalendarEvent(
            summary="Vicious - Heaven of the South",
            start="2026-03-01",
            end="2026-03-02",
            family="ride-vicious",
            source_key="vicious-heaven-of-the-south-2026",
            description="Official event page for Heaven of the South.",
            location="Enumclaw, WA",
        ),
        CalendarEvent(
            summary="Vicious - Mudslinger",
            start="2026-04-19",
            end="2026-04-20",
            family="ride-vicious",
            source_key="vicious-mudslinger-2026",
            description="Official event page for Mudslinger.",
            location="Pacific Raceways, WA",
        ),
    ]
    plan = reconcile_family(
        family="ride-vicious",
        target_year=2026,
        calendar_name="PNW Bike Events",
        existing=existing,
        candidates=candidates,
    )
    assert [action.action for action in plan.actions] == ["patch", "insert"]


def test_fixture_candidate_file_can_be_loaded() -> None:
    payload = json.loads(Path("tests/fixtures/ride_vicious_2026.json").read_text(encoding="utf-8"))
    assert len(payload) == 2
    assert payload[0]["family"] == "ride-vicious"

