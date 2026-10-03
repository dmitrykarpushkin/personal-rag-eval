---
created: 2026-09-09T09:20:00
source: email
tags: [harbor, mail, bug]
---

# Email digest: ETA timezone report

**Priya forwarding a message from the Rotterdam dispatcher:**
> The ETAs in Harbor are an hour off compared to the carrier portal. Is this a bug?

**Priya:**
> I guess it is. Could you look at it before Friday?

**Mara:** reproduced in ten minutes. Stored values are right, rendering uses Tallinn time. Fix is in the next sprint plan: render in the viewer's own zone, show the zone on hover. Replied with a short explanation, no blame, no drama.

**Dispatcher (Rotterdam), via Priya:**
> Thanks, I thought I was going crazy.

Action items
- Fix and test with three zones.
- Mention in the Friday mail to Tomasz.

Lesson: write the timezone test earlier next time.
