---
created: 2026-08-11T13:30:00
source: note
tags: [harbor, notifications, decision]
---

# Notifications: which channel?

Dispatchers want to know about exceptions without staring at the dashboard. Options:

- **Email**: already works for lateness alerts. People ignore email.
- **Browser push**: dispatchers keep the tab open all day, so push could work, but the warehouse PCs share browsers.
- **Chat integration** (Kestrel uses Teams): most natural, but depends on Kestrel IT.
- **Sound in the app**: Lena's request, cheap, and surprisingly good.

Decision (small): ship email digests plus an in-app badge and an optional sound. Postpone Teams until Tomasz's team has someone to own the webhook on their side.

Kept the notification settings per user: which exception kinds, which carriers, quiet hours.

Mailed Priya the decision, with a mockup from Jon. She answered "sound!!" with two exclamation marks, which is more excitement than she normally shows about notifications.

Tickets: HRB-172 (UI part), HRB-176 (badge), HRB-178 (sound toggle).
