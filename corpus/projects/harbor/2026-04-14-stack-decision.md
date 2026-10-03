---
created: 2026-04-14T21:05:00
source: note
tags: [harbor, decision, frontend]
---

# Stack decision, Harbor

Spent the weekend and today comparing three options for the dashboard frontend: Next.js, SvelteKit, and plain Vue 3 with Vite. Built the same shipment list page (filters, sort, a status pill, a map placeholder) in the first two.

**Decision: Decided on SvelteKit for the Harbor frontend (team is small, Priya liked the prototype speed); backend stays on FastAPI.**

Why, in order of weight:
1. Team is small. It is me, Jon on design, and Kestrel's one part-time developer who will maintain this after the contract. Less framework surface to learn is a real advantage.
2. The SvelteKit prototype took about half a day; the Next.js one took most of a day because of the data fetching conventions. Priya saw both on the Tuesday call and said the Svelte one "felt instant".
3. Bundle size on the shipment table is a lot smaller. Kestrel's dispatchers use older laptops in the warehouse office.

Why not Next.js: heavier, and I would be reinventing half of the server-side bits that FastAPI already does well.

Backend: no change, FastAPI with Postgres. The API contract is described in an OpenAPI file that Jon and I both read.

## Follow ups
- Mail Tomasz the one-page version (done tonight, short).
- Set up the repo skeleton and CI tomorrow.
- Ask Jon to export the status colours as CSS tokens.
- Open question: component library or hand-rolled? Leaning hand-rolled for the table, off-the-shelf for dialogs.
