from __future__ import annotations

import json
import subprocess
from typing import Any


class CalendarCliError(RuntimeError):
    pass


def _run_gws(args: list[str], params: dict[str, Any] | None = None, body: dict[str, Any] | None = None) -> dict[str, Any]:
    command = ["gws", *args, "--format", "json"]
    if params is not None:
        command.extend(["--params", json.dumps(params)])
    if body is not None:
        command.extend(["--json", json.dumps(body)])
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise CalendarCliError(completed.stderr.strip() or completed.stdout.strip())
    stdout = completed.stdout
    start = stdout.find("{")
    if start == -1:
        raise CalendarCliError(f"Expected JSON output, got: {stdout.strip()}")
    return json.loads(stdout[start:])


def list_calendars() -> list[dict[str, Any]]:
    payload = _run_gws(["calendar", "calendarList", "list"], params={"minAccessRole": "owner"})
    return payload.get("items", [])


def resolve_calendar_id(name: str) -> str:
    if name == "primary":
        return "primary"
    for item in list_calendars():
        if item.get("summary") == name or item.get("id") == name:
            return item["id"]
    raise CalendarCliError(f"Could not resolve calendar: {name}")


def list_events(
    calendar_name: str,
    *,
    time_min: str,
    time_max: str,
    single_events: bool = True,
    order_by: str = "startTime",
    q: str | None = None,
    private_extended_property: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "calendarId": resolve_calendar_id(calendar_name),
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": single_events,
        "orderBy": order_by,
        "maxResults": 250,
    }
    if q:
        params["q"] = q
    if private_extended_property:
        params["privateExtendedProperty"] = [private_extended_property]
    payload = _run_gws(["calendar", "events", "list"], params=params)
    return payload.get("items", [])


def insert_event(calendar_name: str, body: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"dry_run": True, "calendar": calendar_name, "body": body}
    params = {"calendarId": resolve_calendar_id(calendar_name), "sendUpdates": "none"}
    return _run_gws(["calendar", "events", "insert"], params=params, body=body)


def patch_event(calendar_name: str, event_id: str, body: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"dry_run": True, "calendar": calendar_name, "eventId": event_id, "body": body}
    params = {
        "calendarId": resolve_calendar_id(calendar_name),
        "eventId": event_id,
        "sendUpdates": "none",
    }
    return _run_gws(["calendar", "events", "patch"], params=params, body=body)

