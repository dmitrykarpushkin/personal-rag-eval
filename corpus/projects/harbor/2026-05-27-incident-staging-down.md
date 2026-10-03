---
created: 2026-05-27T08:50:00
source: note
tags: [harbor, incident, staging]
---

# Incident: staging down

**When:** 2026-05-26, evening, found 07:30 on 05-27.
**Impact:** staging only. Priya's team could not preview the saved filters before the sync.

## What happened
The disk on the staging VM filled up. The import worker had been writing verbose debug logs for the whole week and the Docker log driver had no size limit. Postgres then refused writes and the app returned 500s.

## Fix
- Cleared logs, restarted the stack. Back at 07:55.
- Set log rotation (size and file count) in the Compose file for every service.
- Added a disk usage check to the nightly job: warns by mail above 80%.

## Lessons
- Staging deserves the same hygiene as production. I treated it as disposable and it bit me.
- Noisy debug logging should never ship. Opened a small ticket to review log levels.

No customer data affected. Told Priya in the morning sync, she shrugged and asked for the filters preview anyway, which worked after the fix.
