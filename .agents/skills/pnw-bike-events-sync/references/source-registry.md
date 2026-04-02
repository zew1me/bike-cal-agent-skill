# Source Registry

Default organizer families:

- `ride-vicious`: `https://www.rideviciouscycle.com/` and `https://www.rideviciouscycle.com/events`
- `sticky-bidon-raceways`: `https://www.stickybidon.com/` plus published Pacific Raceways schedule graphics
- `cascade-major-rides`: `https://cascade.org/rides-events/ride-information-support/season-schedule`, `https://cascade.org/stp`, and current-year RSVP pages
- `redmond-cycling-club`: `https://www.redmondcyclingclub.org/` and current Redmond Cycling Club notices
- `mountain-classics`: current-year pages for Mt. Baker Hill Climb (`https://bakerhillclimb.com/race-information/`) or High Pass Challenge
- `cyclocross-series`: MFG, CXR, Cascade Cross, Lemon Peel, Wednesday Night Worlds XC, and SSCXWC26BHAM (`https://sscxwc26bham.com/`)
- `wider-pnw`: BWR BC (`https://www.belgianwaffleride.bike/blogs/news/bwr-british-columbia`), Kettle Mettle (`https://www.kettlemettle.ca/`), Rebecca's Private Idaho (`https://www.rebeccasprivateidaho.com/`), Tour de Bloom (`https://www.tourdebloom.com/`), Tour de Whatcom (`https://tourdewhatcom.com/`), Grinduro, OBRA, and other wider-net sources

Batch handling notes:

- Prefer official current-year pages over secondary calendars.
- When a source only publishes a schedule image, record the image-derived entries in a candidate JSON file and note the source URL or asset in each item.
- If a current-year page is not live yet, keep the event unresolved instead of copying the prior-season date.
- Cascade currently serves `403 Forbidden` to simple scripted fetches, so use a browser-verified official snapshot when the live page fetch is blocked.
- BWR BC remains tracked for the wider-net family, but do not write it until the official site posts an exact current-year event date rather than a season/month teaser.
- Redmond Cycling Club currently states that RAMROD is canceled for 2026, so do not add RAMROD unless that official status changes.
- For cyclocross, treat January 2026 races as part of the closing 2025/2026 season; the upcoming verified batch should focus on fall 2026 onward for the 2026/2027 season.
