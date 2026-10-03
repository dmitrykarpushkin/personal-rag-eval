---
created: 2026-08-14T08:40:00
source: email
tags: [mail, stripe, payout, glaze, bank]
---
# Stripe: payout failed

Email digest from Stripe, plus what I did about it.

> Subject: Your payout has failed
> Payout po_1Q8xK2 could not be delivered to your bank account. Please check your bank details and try again.

What happened: Payout po_1Q8xK2 failed: bank rejected because the IBAN on file was the old LHV account; updated to Wise. I had closed the old account in the spring and forgot that the shop payouts were still pointed at it.

Steps taken:
- Changed the payout account in the Stripe dashboard
- Stripe will retry automatically within a few days
- Told myself to review every place with bank details before the Lisbon move

Amount was small, just the last few orders of the month.
