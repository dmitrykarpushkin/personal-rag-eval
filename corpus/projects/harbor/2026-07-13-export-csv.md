---
created: 2026-07-13T16:10:00
source: note
tags: [harbor, export, csv]
---

# CSV export, working notes

Built HRB-159. Things I learned:

- Dispatchers open the CSV in Excel on Windows. Excel treats UTF-8 files without a BOM as garbage, so city names like "Göteborg" came out broken. Added the BOM. Looks silly, works.
- Semicolon vs comma: Kestrel's locale makes Excel expect semicolons. Gave the export a setting, default semicolon.
- Dates written as ISO with explicit zone, since the timezone matters (see the earlier ETA discussion). Do not localise inside the file.
- Big exports: stream the response, do not build the file in memory. Tested with 40k rows, constant memory.

Open question: should the export include the "changed today" flag? Decided yes, as a text column.

Tests: three, plus a manual check in Excel from a borrowed laptop. Jon sent the button design: icon plus label, because icon-only confused the test user.

Shipping to staging on Friday.
