---
created: 2024-09-02T09:58:00
source: note
tags: [lumen, decision]
---
# Decision: Imports run asynchronously with a job table

Considered synchronous import with a long timeout. Rejected because a 500 MB upload would hold a worker for minutes and fail on proxy timeouts. Decision: upload returns a job id, a worker streams the file, user sees progress and gets an email. Job table keeps state, retries are idempotent via a key per upload.
