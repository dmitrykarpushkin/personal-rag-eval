---
created: 2026-09-08T21:30:00
source: journal
tags: [harbor, carriers, planning]
---

Evening, thinking on paper. Back to work after the marathon, legs still heavy, head clearer than I expected.

In the sync today Priya hinted that the next phase might be about carriers. Not formal yet. But let me think it through so I am not improvising.

What exists: the nightly import gives a view from yesterday. What dispatchers want: live updates from carriers themselves. Each carrier has its own API shape; some push webhooks, some only have polling endpoints, and every one has an auth scheme designed by a committee.

My rough approach:
1. A raw events table that stores whatever the carrier sends, untouched.
2. An adapter per carrier that turns raw events into our normalised statuses.
3. Idempotent processing, because carriers retry, duplicate, reorder.
4. A replay tool, because I will debug this for weeks.

Big carriers first. Start with whichever has the cleanest documentation. Do not promise a list of carriers until I have read the docs.

Risks: sandbox access takes forever; Tomasz must approve a public endpoint; rate limits.

Nothing is signed. Do not start building before Priya confirms scope. Draft the proposal anyway.
