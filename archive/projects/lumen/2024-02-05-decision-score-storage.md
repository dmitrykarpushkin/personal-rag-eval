---
created: 2024-02-05T12:07:00
source: note
tags: [lumen, decision]
---
# Decision: Where to compute the health score

We discussed three options: compute on read, nightly batch into a table, or a materialised view. Compute on read was the quickest to build but the dashboard took six seconds to load with real data. The nightly table is simple but data is a day old. We chose the materialised view refreshed every 30 minutes: fresh enough for CS, fast enough for the page. Owner: me. Revisit if row count passes 50 million.
