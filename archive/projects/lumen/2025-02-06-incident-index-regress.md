---
created: 2025-02-06T12:50:00
source: note
tags: [lumen, incident]
---
# Incident: Slow duplicate check after a migration

A migration dropped a partial index on the big customer's table. Imports took 40 seconds longer per batch. Restored the index, added the index to the migration checklist.
