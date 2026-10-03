---
created: 2024-03-05T13:57:00
source: note
tags: [lumen, incident]
---
# Incident: Weekly usage counted twice for two-owner accounts

Found by Maris on Tuesday: accounts with two owners showed double usage. Cause: join on owners table inflated rows before aggregation. Fix: aggregate first, then join. Backfilled the weekly table. Impact: about 40 accounts had wrong scores for six days; nobody had acted on them. Added a test with two owners.
