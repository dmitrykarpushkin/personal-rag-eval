---
created: 2024-08-23T16:37:00
source: note
tags: [lumen, atlas, sprint]
---
# Sprint 16 (Atlas import)

**Goal:** undo and idempotency.

## Done
- undo last import within 24 hours (ATL-24)
- idempotency key per upload
- fixed double-counted rows when the same file was uploaded twice

## Slipped
- customer-facing docs

The undo feature turned out to be mostly a question of what 'undo' means for rows another import already touched. Settled on: last import only.
