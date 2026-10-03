---
created: 2024-06-26T17:27:00
source: note
tags: [lumen, incident]
---
# Incident: Alert emails sent twice after a retry

A mail provider timeout triggered a retry without an idempotency key, 112 CS owners got two emails each. Apologised in the channel. Fixed with a send-once table. Lesson: any retry needs a key, even for emails nobody reads.
