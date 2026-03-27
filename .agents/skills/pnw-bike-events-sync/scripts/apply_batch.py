from __future__ import annotations

import argparse
import json
from pathlib import Path

from pnw_bike_events.calendar_cli import insert_event, patch_event


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a verified reconciliation plan to the master calendar.")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    payload = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    calendar = payload["calendar"]
    results: list[dict] = []
    for action in payload["actions"]:
        kind = action["action"]
        if kind == "insert":
            results.append(insert_event(calendar, action["payload"], dry_run=args.dry_run))
        elif kind == "patch":
            results.append(
                patch_event(
                    calendar,
                    action["existing_event_id"],
                    action["payload"],
                    dry_run=args.dry_run,
                )
            )
        else:
            results.append({"action": kind, "source_key": action["source_key"]})

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
