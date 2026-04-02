from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.cyclocross_series import fetch_cyclocross_series


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch the current verified cyclocross batch from official 2026/2027 season pages.")
    parser.add_argument("--target-year", type=int, required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    events = fetch_cyclocross_series(target_year=args.target_year)
    output = Path(args.output or f"reports/cyclocross-series-{args.target_year}-candidates.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([event.to_dict() for event in events], indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
