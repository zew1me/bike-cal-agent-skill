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


def test_reconcile_family_does_not_patch_prior_year_summary_match() -> None:
    existing = [
        CalendarEvent(
            summary="Cascade - STP",
            start="2025-07-12",
            end="2025-07-14",
            family="cascade-major-rides",
            source_key="stp-2025",
            description="Old STP",
            event_id="old-stp",
        )
    ]
    candidates = [
        CalendarEvent(
            summary="Cascade - STP",
            start="2026-07-11",
            end="2026-07-13",
            family="cascade-major-rides",
            source_key="stp-2026",
            description="New STP",
            location="University of Washington E-18 Lot",
        )
    ]
    plan = reconcile_family(
        family="cascade-major-rides",
        target_year=2026,
        calendar_name="PNW Bike Events",
        existing=existing,
        candidates=candidates,
    )
    assert [action.action for action in plan.actions] == ["insert"]
