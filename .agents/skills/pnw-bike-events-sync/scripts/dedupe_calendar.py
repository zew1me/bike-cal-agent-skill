from __future__ import annotations

import argparse
import json

from pnw_bike_events.dedupe import dedupe_calendar


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete legacy duplicate events while keeping canonical synced entries.")
    parser.add_argument("--calendar", default="PNW Bike Events")
    parser.add_argument("--match", default=None)
    parser.add_argument("--time-min", default=None)
    parser.add_argument("--time-max", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    results = dedupe_calendar(
        calendar_name=args.calendar,
        match_text=args.match,
        time_min=args.time_min,
        time_max=args.time_max,
        dry_run=args.dry_run,
    )
    print(json.dumps([item.to_dict() for item in results], indent=2))


if __name__ == "__main__":
    main()
