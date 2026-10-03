---
created: 2024-10-30T14:13:00
source: note
tags: [lumen, design]
---
# Notes on SFTP pulls

Rules I wrote after the stuck-file incident:
- Never pull a file whose size changed in the last minute.
- Keep a checksum before and after.
- Customer credentials are stored encrypted, rotated by the customer every 90 days, and never logged.
- Empty file is an alert, not an import.
- A missing scheduled file at the expected time is an alert, not silence.
