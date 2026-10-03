---
created: 2026-09-17T16:35:00
source: email
tags: [harbor, mail, carriers]
---

# Email digest: carrier integration proposal, first round

**Mara to Priya (draft proposal, one page):**
> Three ways to get carrier data in: (1) keep polling, (2) webhooks where the carrier supports them, (3) buy an aggregator. My recommendation: webhooks where possible, polling as a fallback, no aggregator for now. Risks: sandbox access time, duplicates, one more public endpoint.

**Priya:**
> Clear. One question: does option three mean paying someone else per shipment?
> Short answer from me: no aggregator, Tomasz does not like extra vendors.

**Mara:** agreed, noted it as a reason.

**Priya (later):**
> I will forward to Tomasz tomorrow. Please do not start building yet.

Action items
- Wait for her go.
- Prepare questions for the carrier's sandbox request.
