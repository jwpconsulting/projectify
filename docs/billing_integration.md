<!--
SPDX-FileCopyrightText: 2024,2026 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Stripe events

Right now, Projectify handles the following Stripe billing events:

- `checkout.session.completed`: Activates a customer subscription
- `customer.subscription.updated`: Updates the number of seats in a customer
  account
- `invoice.payment_failed`: Triggered when an initial or subsequent
  subscription payment fails. May deactivate a subscription.
- `customer.subscription.deleted`: Triggered when a customer unsubscribes. Deactivates a customer subscription.

## Unhandled events

The Stripe billing logic in Projectify currently doesn't handle these events:

- `charge.succeeded`
- `payment_method.attached`
- `customer.created`
- `customer.updated`
- `customer.subscription.created`
- `customer.subscription.updated`: triggered, for example, when a user cancles
  their subscription, but it has a remaining subscription duration.
- `payment_intent.created`
- `payment_intent.succeeded`
- `invoice.created`
- `invoice.finalized`
- `invoice.updated`
- `billing_portal.session.created`: triggered when Projectify creates a billing
portal session.

# How to test Stripe billing

Log in to Stripe with the following command:

```bash
stripe login
```

Follow the instructions and link your Stripe account to the Stripe CLI.

Listen to webhook events using the `stripe listen` command:

```bash
# Note the trailing slash here
stripe listen --forward-to http://localhost:8000/corporate/stripe-webhook/
```

Test these events:

- `checkout.session.completed`
- `customer.subscription.updated`
- `invoice.payment_failed`
- `customer.subscription.deleted`

You can achieve this by running the following `stripe trigger` commands:

```bash
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.deleted
```

Resend events from the **Workbench** > **Events** page:


```bash
stripe events resend evt_XXXXXXXXXXXXXXXXXXXXXXXX
```
