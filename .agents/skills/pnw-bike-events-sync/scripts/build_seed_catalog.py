from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.seed import build_seed_catalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a prior-season seed catalog from PNW Bike Events.")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--calendar", default="PNW Bike Events")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    catalog = build_seed_catalog(args.year, calendar_name=args.calendar)
    output = Path(args.output or f"reports/seeds-{args.year}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([event.to_dict() for event in catalog], indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
