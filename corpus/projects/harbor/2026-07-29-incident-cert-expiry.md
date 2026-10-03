---
created: 2026-07-29T07:55:00
source: note
tags: [harbor, incident, tls]
---

# Incident: certificate expiry on staging

**Date:** 2026-07-28 night.
**Impact:** staging only. Browser warnings; Priya's colleague noticed first.

## Cause
Caddy renews certificates automatically, but the DNS record for the staging hostname had been changed during a cleanup and ACME validation failed quietly for weeks. The last good certificate expired.

## Fix
- Restored the DNS record, forced a renewal, checked the logs. Fine in 5 minutes.
- Added an external check that fails loudly when a certificate has fewer than 14 days left.

## Lesson
Quiet failures are the worst. Every automated thing needs a loud failure path. Added this to the infra note as a standing rule.

Production was not affected; the hostname there was untouched. Checked twice anyway.

Sent a two-line mail to Tomasz so he hears it from me, not from Priya. His reply: "Thanks. Good that it is an external check."
