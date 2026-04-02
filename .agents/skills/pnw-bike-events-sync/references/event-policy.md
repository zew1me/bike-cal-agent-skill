# Event Policy

Included event types:

- criteriums
- road races
- gravel rides and gravel races
- major Cascade Bicycle Club rides such as RSVP and STP
- marquee RCC events such as RAMROD
- Mt. Baker Hill Climb and High Pass Challenge when current-year sources exist
- Pacific Raceways Circuit Race Series
- cyclocross and cross-country series such as MFG, CXR, Lemon Peel, Wednesday Night Worlds XC, and marquee one-off events like the Single Speed Cyclocross World Championship
- the wider-net family: BWR BC, Grinduro, Tour de Bloom, Tour de Whatcom, Kettle Mettle, Rebecca's Private Idaho, Mudslinger, and selected OBRA events

Normalization defaults:

- all-day dates unless the source provides reliable time-of-day details
- `America/Los_Angeles` as the default timezone
- source URL preserved in the description or extended properties
- direct writes only for verified batches
- wider-net marquee batches may intentionally exclude tracked events such as BWR BC until the official source publishes an exact current-year date
