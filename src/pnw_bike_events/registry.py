from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceFamily:
    slug: str
    title: str
    disciplines: tuple[str, ...]
    urls: tuple[str, ...]
    keywords: tuple[str, ...]
    notes: str


FAMILIES: tuple[SourceFamily, ...] = (
    SourceFamily(
        slug="ride-vicious",
        title="Ride Vicious",
        disciplines=("road", "gravel", "criterium"),
        urls=(
            "https://www.rideviciouscycle.com/",
            "https://www.rideviciouscycle.com/events",
        ),
        keywords=("vicious", "heaven of the south", "mudslinger"),
        notes="Primary source for Ride Vicious events and linked event pages.",
    ),
    SourceFamily(
        slug="sticky-bidon-raceways",
        title="Sticky Bidon / Pacific Raceways",
        disciplines=("criterium", "road"),
        urls=(
            "https://www.stickybidon.com/",
            "https://www.stickybidon.com/calendar",
        ),
        keywords=("sticky bidon", "pacific raceways", "circuit race", "season kickoff"),
        notes="Use Sticky Bidon plus explicit schedule graphics when race times are only published as images.",
    ),
    SourceFamily(
        slug="cascade-major-rides",
        title="Cascade Bicycle Club",
        disciplines=("road", "gravel"),
        urls=(
            "https://cascade.org/rides-and-events-major-rides",
            "https://cascade.org/",
        ),
        keywords=("cascade", "rsvp", "stp", "high pass", "kitsap", "woodinville"),
        notes="Includes major Cascade rides such as RSVP and STP; only promote current-year pages.",
    ),
    SourceFamily(
        slug="redmond-cycling-club",
        title="Redmond Cycling Club",
        disciplines=("road", "endurance"),
        urls=("https://www.redmondcyclingclub.org/",),
        keywords=("ramrod", "redmond cycling club", "sufferin summits"),
        notes="Includes RAMROD and other RCC marquee rides when current-year pages exist.",
    ),
    SourceFamily(
        slug="mountain-classics",
        title="Mountain Classics",
        disciplines=("road", "climb"),
        urls=(
            "https://www.belllapproductions.com/events",
            "https://ridewithgps.com/",
        ),
        keywords=("mt baker", "mount baker", "high pass", "hill climb"),
        notes="Use for Mt. Baker Hill Climb and High Pass Challenge when official pages are live.",
    ),
    SourceFamily(
        slug="cyclocross-series",
        title="Cyclocross Series",
        disciplines=("cyclocross", "xc"),
        urls=(
            "https://mfgcyclocross.bike/",
            "https://cascadecross.com/",
            "https://cxr.racing/",
            "https://sscxwc26bham.com/",
        ),
        keywords=("mfg", "cxr", "lemon peel", "cross", "cyclocross", "wnw", "single speed cyclocross world championship", "sscxwc", "sscxwc26bham"),
        notes="Bundle MFG, CXR, Lemon Peel, Cascade Cross, Wednesday Night Worlds cross-country, and marquee one-off cyclocross events such as SSCXWC in Bellingham.",
    ),
    SourceFamily(
        slug="wider-pnw",
        title="Wider PNW",
        disciplines=("gravel", "road", "stage-race"),
        urls=(
            "https://www.belgianwaffleride.bike/",
            "https://www.kettlemettle.ca/",
            "https://www.rebeccasprivateidaho.com/",
            "https://tourdewhatcom.com/",
            "https://www.tourdebloom.com/",
            "https://www.grinduro.com/",
            "https://obra.org/",
        ),
        keywords=(
            "tour de bloom",
            "tour de whatcom",
            "belgian waffle",
            "bwr bc",
            "kettle mettle",
            "rebecca's private idaho",
            "grinduro",
            "obra",
            "portland",
        ),
        notes="Catch-all for the wider-net family once core sources are handled; only apply events with exact current-year official dates.",
    ),
)


def family_by_slug(slug: str) -> SourceFamily:
    for family in FAMILIES:
        if family.slug == slug:
            return family
    raise KeyError(f"Unknown source family: {slug}")


def classify_family(summary: str, description: str = "") -> str:
    haystack = f"{summary} {description}".lower()
    for family in FAMILIES:
        if any(keyword in haystack for keyword in family.keywords):
            return family.slug
    return "unclassified"
