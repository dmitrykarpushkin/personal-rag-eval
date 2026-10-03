---
created: 2026-04-02T09:15:00
source: note
tags: [harbor, project, kestrel]
---

# Harbor

Shipment-tracking dashboard for Kestrel Freight, a freelance contract. Kestrel is a freight forwarder; dispatchers currently live in spreadsheets and carrier portals. Harbor gives them one list of shipments with ETA, status and exceptions.

## People
- Priya Raman, product manager at Kestrel, my day-to-day contact (weekly sync).
- Tomasz Wójcik, CTO, signs off on architecture.
- Jon Ahlberg, freelance designer, works with me on the UI.

## Contract
- Contract: €85/h, started April 2026 (older section, may say initial terms).
- Billing: monthly invoice to Kestrel Freight OÜ, net 14 days.
- Scope at start: dashboard (list, detail, filters), nightly import from their TMS, basic alerts.
- Notice: 30 days either side.

## Stack
SvelteKit frontend, FastAPI backend, Postgres, Docker Compose. Hosting details are in the infra log.

## Where things are
- Dated logs live in projects/harbor/.
- Meetings with Priya, Jon and Tomasz are in meetings/ with "harbor" in the name.
- Email digests in mail/.

## Status line (April)
Kickoff done, stack chosen, first sprint planned. Demo to Priya at the end of April.

## Standing rules for myself
- Never promise dates in a call. Check the board, then mail.
- Keep a short written trail for every decision; Tomasz likes to read it later.
- Hours go into the time sheet the same day.
