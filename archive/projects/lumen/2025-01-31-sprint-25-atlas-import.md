---
created: 2025-01-31T18:03:00
source: note
tags: [lumen, atlas, sprint]
---
# Sprint 25 (Atlas import)

**Goal:** performance and observability.

## Done
- tracing across upload, parse, validate, write (ATL-76)
- p95 import time chart
- slow query on duplicate check fixed with a partial index

## Slipped
- bulk template edit

The partial index cut the duplicate check from 40 seconds to under 2 on the big customer.
