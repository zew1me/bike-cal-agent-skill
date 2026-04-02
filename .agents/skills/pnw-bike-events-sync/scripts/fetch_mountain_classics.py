from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.mountain_classics import fetch_mountain_classics


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch the mountain classics batch from verified official 2026 event pages.")
    parser.add_argument("--target-year", type=int, required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    events = fetch_mountain_classics(target_year=args.target_year)
    output = Path(args.output or f"reports/mountain-classics-{args.target_year}-candidates.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([event.to_dict() for event in events], indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
