from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.cascade import fetch_cascade_major_rides


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch official Cascade STP and RSVP event pages.")
    parser.add_argument("--target-year", type=int, required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    events = fetch_cascade_major_rides(target_year=args.target_year)
    output = Path(args.output or f"reports/cascade-major-rides-{args.target_year}-candidates.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([event.to_dict() for event in events], indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
