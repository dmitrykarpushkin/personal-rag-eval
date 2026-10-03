---
created: 2024-10-29T16:24:00
source: note
tags: [lumen, incident]
---
# Incident: SFTP pull stuck on a locked file

A customer's server kept the file open while we pulled, so we imported half a file. Rows were wrong for two hours. Fix: check size is stable for 60 seconds before pulling, and use a checksum. Customer informed by Kertu.
