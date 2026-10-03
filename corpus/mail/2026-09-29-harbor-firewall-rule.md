---
created: 2026-09-29T17:50:00
source: email
tags: [harbor, mail, infra]
---

# Email digest: firewall rule for webhooks

**Mara to Tomasz (cc Priya):**
> For the carrier webhook work I need one inbound HTTPS path opened on the production host, restricted to the carrier's published address ranges, with signature verification in the app. Details below. Staging first.

**Tomasz:**
> Approved for staging now, production after I have seen it working there. Send me the address ranges once you have them. Logging on that endpoint must be on.

**Priya:**
> Thanks both. I will add it to the December demo plan.

Action items
- Request the address ranges from the carrier.
- Set up request logging on the endpoint (no payload bodies in logs).
- Note the approval in the runbook.

Tone: efficient. Tomasz said more in one mail than usual.
