---
created: 2026-09-18T11:15:00
source: note
tags: [harbor, pagination, decision]
---

# Decision: cursor pagination for the list

The list has been using offset pagination, and the jump bug (HRB-167) showed its weakness: new events shift rows, and users end up on the wrong page.

**Decision:** switch the shipment list to cursor-based pagination, ordered by (eta, id). Infinite scroll stays, but with a visible "loaded 200 of 1,430" counter so people know where they are.

Why: stable position when data changes, faster on deep pages, simpler to reason about.

Trade-offs:
- Jumping to "page 40" is impossible. Nobody does it; Priya checked with the dispatchers.
- Slightly more frontend state. Fine.

Tickets: HRB-195 (backend cursor), HRB-197 (frontend loader), HRB-199 (counter). Estimate: two days.

Jon liked the counter and asked for a "back to top" button; added to HRB-199 as small print.
