from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.diffing import reconcile_family
from pnw_bike_events.models import CalendarEvent


def _load_events(path: Path) -> list[CalendarEvent]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [CalendarEvent(**item) for item in payload]


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare candidate events with prior-season seeds for one family.")
    parser.add_argument("--family", required=True)
    parser.add_argument("--target-year", type=int, required=True)
    parser.add_argument("--calendar", default="PNW Bike Events")
    parser.add_argument("--seed-catalog", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    existing = _load_events(Path(args.seed_catalog))
    candidates = _load_events(Path(args.candidates))
    plan = reconcile_family(
        family=args.family,
        target_year=args.target_year,
        calendar_name=args.calendar,
        existing=existing,
        candidates=candidates,
    )
    output = Path(args.output or f"reports/{args.family}-{args.target_year}-plan.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan.to_dict(), indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
