---
created: 2026-04-07T20:15:00
source: journal
tags: [harbor, discovery]
---

Rambling notes after the first weekly sync and a long look at the sample export.

The CSV from their TMS is worse than I hoped. Same shipment appears on several rows, one per leg, and the "status" column holds numbers with no legend. Priya went and asked the ops lead, who sent a list from memory. We now believe 1 = booked, 3 = in transit, 5 = at port, 7 = delivered, 9 = cancelled. Not sure about 4 and 6. Written down as "unknown, ask" and moved on.

Things I like: they have a stable shipment reference (alphanumeric, always the same prefix), so deduplication is easy. Things I do not: dates in two formats, depending on which office exported them.

Interesting conversation with Priya about who the users really are. Not managers. Five dispatchers, each with their own habits. She suggested I sit with one of them over video for an hour. Yes. Book it.

Plan for tomorrow:
- Sketch the shipment and leg tables.
- Write the import as a script first, make it a worker later.
- Send Jon the screenshots of the current spreadsheet so he sees the real mess.

Tired but it feels like a good project. The kind where the users will say thank you.
