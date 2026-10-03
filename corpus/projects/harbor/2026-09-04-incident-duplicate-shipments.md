---
created: 2026-09-04T18:20:00
source: note
tags: [harbor, incident, import]
---

# Incident: duplicate shipments in the list

**Seen:** Thursday afternoon, reported by a dispatcher through Priya.
**Impact:** about 20 shipments appeared twice in the list for one night. Dispatchers saw doubles; no data lost.

## Cause
Kestrel's TMS export started including a "re-issued" flag where the shipment reference had a suffix ("-R") for amended bookings. Our import treated the suffix as a different shipment. Dedupe keyed on the exact reference.

## Fix
- Normalise the reference by stripping the amendment suffix, keep the original in a separate column.
- Merge the existing duplicates with a one-off script, keeping the oldest record's history.
- Added a test file with amended references from the real export (anonymised).

## Lessons
- Never assume upstream formats are stable. Ask Priya to warn me before the TMS team changes anything, and she agreed to try.
- Idempotency is the main theme of anything we ingest. This will matter much more once data arrives from carriers directly.

Written up in two lines for Tomasz's Friday mail.
