from __future__ import annotations

import hashlib
import re
from typing import Any

from .models import CalendarEvent
from .registry import classify_family


_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def normalized_summary(summary: str) -> str:
    cleaned = _NON_ALNUM_RE.sub("-", summary.lower()).strip("-")
    return cleaned or "event"


def build_source_key(family: str, summary: str, start: str) -> str:
    base = f"{family}:{normalized_summary(summary)}:{start}"
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
    return f"{normalized_summary(summary)}-{digest}"


def google_event_to_model(item: dict[str, Any]) -> CalendarEvent:
    start_payload = item.get("start", {})
    end_payload = item.get("end", {})
    start = start_payload.get("date") or start_payload.get("dateTime")
    end = end_payload.get("date") or end_payload.get("dateTime")
    summary = item.get("summary", "Untitled Event")
    description = item.get("description", "")
    family = classify_family(summary, description)
    source_key = (
        item.get("extendedProperties", {})
        .get("private", {})
        .get("pnw_source_key")
        or build_source_key(family, summary, start)
    )
    all_day = "date" in item.get("start", {})
    private_props = dict(item.get("extendedProperties", {}).get("private", {}))
    source_url = private_props.get("pnw_source_url")
    return CalendarEvent(
        summary=summary,
        start=start,
        end=end,
        family=family,
        source_key=source_key,
        all_day=all_day,
        timezone=start_payload.get("timeZone") or end_payload.get("timeZone"),
        description=description,
        location=item.get("location", ""),
        event_id=item.get("id"),
        source_url=source_url,
        status=item.get("status", "confirmed"),
        transparency=item.get("transparency", "transparent"),
        extended_private=private_props,
    )


def model_to_google_body(event: CalendarEvent) -> dict[str, Any]:
    private_props = {
        "pnw_source_family": event.family,
        "pnw_source_key": event.source_key,
    }
    if event.source_url:
        private_props["pnw_source_url"] = event.source_url
    private_props.update(event.extended_private)

    if event.all_day:
        start = {"date": event.start}
        end = {"date": event.end}
    else:
        start = {"dateTime": event.start}
        end = {"dateTime": event.end}
        if event.timezone:
            start["timeZone"] = event.timezone
            end["timeZone"] = event.timezone

    body: dict[str, Any] = {
        "summary": event.summary,
        "description": event.description,
        "location": event.location,
        "start": start,
        "end": end,
        "status": event.status,
        "transparency": event.transparency,
        "extendedProperties": {"private": private_props},
    }
    return body
