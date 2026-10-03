---
created: 2024-04-22T11:49:00
source: note
tags: [lumen, incident]
---
# Incident: Nightly job finished at 08:40 instead of 03:00

The nightly usage load slowed after a customer sent a spike of events. Dashboard was stale until after the CS stand-up. Short-term: added an index and a timeout. Follow-up: alert when the job passes 05:00. No customer was affected.
