from __future__ import annotations

import argparse
import json

from pnw_bike_events.promotion import promote_matching_events


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone or refresh linked copies of master bike events.")
    parser.add_argument("--source", default="PNW Bike Events")
    parser.add_argument("--destination", required=True)
    parser.add_argument("--match", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    results = promote_matching_events(
        source_calendar=args.source,
        destination_calendar=args.destination,
        match_text=args.match,
        dry_run=args.dry_run,
    )
    print(json.dumps([item.to_dict() for item in results], indent=2))


if __name__ == "__main__":
    main()
