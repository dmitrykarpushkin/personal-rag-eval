---
created: 2024-12-17T18:16:00
source: note
tags: [lumen, incident]
---
# Incident: Upload bucket lifecycle missing, disk alert at 91%

No lifecycle rule on the upload bucket meant failed uploads piled up. Aleksei caught the alert before it hit 100%. Added a 14 day expiry and a weekly report of bucket size.
