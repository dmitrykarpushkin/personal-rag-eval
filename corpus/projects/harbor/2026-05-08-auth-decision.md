---
created: 2026-05-08T14:20:00
source: note
tags: [harbor, auth, decision]
---

# Auth decision

Magic links worked for the demo but are wrong for dispatchers who share a warehouse PC and have shifts. Options:

1. Keep magic links with short sessions. Simple but annoying.
2. Username and password with a proper reset flow. Boring and fine.
3. Kestrel's identity provider via OIDC. Best, but their IT has not set it up and I will not wait on that.

**Decision:** go with option 2 now, with a clean seam so option 3 can slot in later. Passwords hashed with argon2, sessions in secure cookies, a lockout after repeated failures.

Tomasz agreed in a short mail: "Fine for now, I want OIDC before it grows beyond the dispatch team." Added to the later list.

Tickets:
- HRB-124: login form and session handling
- HRB-127: password reset by email
- HRB-129: admin page to create and disable users (Priya will use it)

Not in scope: roles beyond dispatcher and viewer. Resist the urge.

About 10 hours of work. Will do after the infra note is out.
