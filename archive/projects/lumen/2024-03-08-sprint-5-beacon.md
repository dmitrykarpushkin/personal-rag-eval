---
created: 2024-03-08T15:41:00
source: note
tags: [lumen, beacon, sprint]
---
# Beacon, sprint 5 review

Timezone bug was embarrassing. Everything was UTC in storage and Tallinn time in the chart. Wrote a test that would have caught it.

Goal was to renewal date filter and alert emails.

Shipped: renewal date filter (BCN-57); alert emails with the approved text, sent through the existing mail service; fixed timezone shift in weekly buckets, Sunday usage was landing in the wrong week.

Not shipped: SSO login.
