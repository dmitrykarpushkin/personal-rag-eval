---
created: 2026-06-23T21:10:00
source: note
tags: [harbor, incident, performance]
---

# Incident: slow dashboard

Back from Lisbon two days ago; Priya pinged me: "dashboard feels slow since Monday". Checked while on the sofa.

**Symptoms:** the shipment list took 4 to 6 seconds to load for dispatchers, was under one second before.
**Cause:** the nightly import had grown the events table and the "changed since yesterday" query had no index on received_at. It was scanning the whole table for every list load.
**Fix:** added a composite index on events (shipment_id, received_at) and rewrote the query to use a lateral join. List load back under 400 ms on the real data.

## Follow ups
- HRB-158: slow query log enabled on production
- Add a performance test on the seeded data with 50k events
- Mention in the weekly sync: be honest, it was my miss on a code review of my own code

Nothing lost. Priya: "Thanks for fixing it so quickly." Slightly embarrassed anyway.
