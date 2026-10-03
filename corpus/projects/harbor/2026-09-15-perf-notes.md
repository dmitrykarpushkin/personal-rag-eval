---
created: 2026-09-15T16:00:00
source: note
tags: [harbor, performance]
---

# Performance notes

Checked the dashboard on the real data after the timezone fix and the digest work.

Numbers (measured on production, a quiet afternoon, 5 runs each, medians):
- Shipment list, no filter: about 350 ms
- Shipment list with three filters: about 420 ms
- Detail page: about 180 ms
- CSV export of the full list: starts streaming in under a second

All fine. The events table is the thing to watch; it grows every night. Plan:
- Partition by month when it passes a few million rows (not yet)
- Keep the slow query log on, review weekly

No action now. Added a recurring reminder for the first Monday of the month to check table sizes.

Side note: the timezone change made the list slightly faster because the formatting moved to the client. Nice accident.
