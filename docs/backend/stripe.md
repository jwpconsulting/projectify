<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Stripe testing

Login with
```
stripe login
```

Then

```
stripe listen --forward-to localhost:8000/corporate/stripe-webhook/
```

Test these events:

- checkout.session.completed
- customer.subscription.updated
- invoice.payment_failed
- customer.subscription.deleted

You can achieve this by running

```
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.deleted
```
