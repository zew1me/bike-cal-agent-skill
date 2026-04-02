from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CalendarEvent:
    summary: str
    start: str
    end: str
    family: str
    source_key: str
    all_day: bool = True
    timezone: str | None = None
    description: str = ""
    location: str = ""
    event_id: str | None = None
    source_url: str | None = None
    status: str = "confirmed"
    transparency: str = "transparent"
    extended_private: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PlanAction:
    action: str
    family: str
    source_key: str
    summary: str
    reason: str
    payload: dict[str, Any]
    existing_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ActionPlan:
    family: str
    target_year: int
    calendar: str
    actions: list[PlanAction]
    unresolved: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "target_year": self.target_year,
            "calendar": self.calendar,
            "actions": [action.to_dict() for action in self.actions],
            "unresolved": list(self.unresolved),
        }


@dataclass(slots=True)
class PromotionResult:
    destination: str
    source_event_id: str
    summary: str
    action: str
    destination_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DedupeResult:
    calendar: str
    summary: str
    year: str
    kept_event_id: str
    deleted_event_id: str
    action: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
