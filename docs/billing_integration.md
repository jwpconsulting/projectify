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

## Manual test steps

Use these steps when you want to test Stripe billing in a local
Projectify development environment
with test API keys.

**Create a workspace**:

1. Create an account with a valid email address. Stripe does not accept `@localhost`
addresses.
1. Create a new workspace by opening <http://localhost:8000/onboarding/welcome>
in a browser.

**Go to checkout**:

1. Go to **Workspace settings** > **Billing**.
2. Enter `10` **Workspace seats** and press **Go to checkout**.
3. Verify that you're on the `checkout.stripe.com` domain.

**Test with declined card**:

1. Use the credit card number `4000000000000002` to simulate a declined
   payment[^declined-payment].
2. Enter `11/55` for the **MM / YY** valid date, and `111` for the **CVC**
3. Enter `1` as the **Cardholder name**
4. Press **Subscribe**
5. Stripe should show the following error: "Your credit card was declined. Try paying with a Your credit card was declined. Try paying with a debit card instead.debit card instead."

**Test with normal card**:

1. Now use the credit card number `4242 4242 4242 4242`
2. Enter `11/55` for the **MM / YY** valid date, and `111` for the **CVC**
3. Enter `1` as the **Cardholder name**
4. Press **Subscribe**
5. You should be directed back to the **Billing** settings page on your local
Projectify environment.
6. The **Number of seats:** entry should state **10 seats in total, 9 seats remaining**.

**Edit billiing details**:

1. Now press **Edit billing details** on the same **Billing** settings page.
   This takes you to the **Projectify Billing Portal** on `billing.stripe.com`.
2. Under **INVOICE HISTORY**, select the invoice for "Projectify Seat".
3. Press **Download receipt**. This should download a PDF file with a receipt.
4. Press **Update subscription**
5. Enter the seat count `20` under **Quantity**
6. Press **Continue**
7. Under **Confirm your updates**, you should see an updated monthly total
of $160.
8. Press **Confirm**
9. You should be back on the **Projectify Billing Portal** on
   `billing.stripe.com`.
10. Press **<- Return to PROJECT_NAME**, where PROJECT_NAME is the project name
that you've configured in your Stripe test environment.
11. You're now on the **Billing** settings page for your workspace again.
12. The **Number of seats:** entry should now state **20 seats in total, 19
    seats remaining**.

**Cancel subscription**:

1. Press **Edit billing details** on the **Billing** settings page again.
2. Press **Cancel subscription** on the **Projectify Billing Portal** page.
3. Confirm by pressing **Cancel subscription** on the **Confirm cancellation**
   page.
4. Press **<- Return to PROJECT_NAME**.
5. The **Number of seats:** entry should still state **20 seats in total, 19
    seats remaining**.

**Simulate subscription ending**:

1. On the Stripe dashboard for your test project, go to **Subscriptions**.
2. Select the current workspace's subscription.
3. Select **Run simulation \>**.
4. Select **+ 1 month** and press **Advance time**.
5. Go back to the **Billing** settings page for your workspace.
6. The text below the settings tabs should say **Subscription cancelled**

[^declined-payment]: <https://docs.stripe.com/testing#declined-payments>

# Stripe configuration

## Customer portal

To let customers adjust their seat count, enable the **Customers can change
quantity of their plan** setting under **Settings** > **Billing**. Make
sure to add a **product** in the **Find a product...** input that appears
below. Make sure to press **Save changes**.
