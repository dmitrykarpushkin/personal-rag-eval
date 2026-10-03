---
created: 2026-06-04T14:30:00
source: voice
tags: [harbor, meeting, tomasz, architecture]
---

# Architecture review with Tomasz (and Priya listening in)

One hour. I brought a one-page diagram, a list of risks and the restore numbers.

Walked through
- Components: SvelteKit, FastAPI, Postgres, import worker, Caddy, Docker Compose.
- Hosting: one dedicated server for production, one small VM for staging; the infra note from May.
- Backups: nightly dump, 30 days, restore tested.
- Secrets: env file owned by root. Tomasz asked me to move to a proper secrets store when the project grows; not now.
- Auth: password login, OIDC later.

Tomasz's questions
- What happens if the box dies? Answer: restore from backup to a new box, expected under two hours, mostly DNS waiting.
- Can Kestrel's ops reproduce the setup without me? Answer: yes, the Compose files and a runbook are in the repo.
- Why not a managed Postgres? Answer: cost and lock-in; revisit if volume jumps.

Outcome
- He signed off on the architecture as presented. Two follow ups: a runbook page, and a monthly restore drill.
- He also asked, for later, about live carrier data. Parked.

Felt good: he engaged properly and asked sharp questions.
