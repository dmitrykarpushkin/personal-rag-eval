---
created: 2026-04-10T16:30:00
source: note
tags: [harbor, data-model, postgres]
---

# Data model v1

Postgres tables, first pass:

- `shipments`: id, kestrel_ref, customer, origin, destination, status, eta_utc, created_at
- `legs`: shipment_id, seq, carrier, mode, depart_utc, arrive_utc, status
- `events`: shipment_id, source, kind, payload (jsonb), received_at
- `exceptions`: shipment_id, kind, opened_at, resolved_at, note
- `users`: id, name, role (dispatcher or viewer)

Decisions:
- Times stored in UTC everywhere. (Say it again so I do not forget: UTC everywhere.)
- Status is an enum on our side, mapped from the TMS numbers in one lookup table so changes are a one-line fix.
- Raw imports kept in a separate staging table for a week, to debug "why did this shipment disappear".

Not yet decided: whether exceptions are derived (computed from late ETA) or entered manually by dispatchers. Probably both. Ask Priya on Tuesday.

Wrote a seed script with 300 fake shipments so Jon can design against realistic density.

Estimated this took 4 hours including the argument with myself about jsonb. jsonb won.
