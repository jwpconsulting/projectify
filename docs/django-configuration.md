<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring the Projectify backend

This document contains a listing of all required backend (including worker and
Django manage command) environment variables. Furthermore, a brief explanation
of the backend's usage of _django configurations_ is included.

# Production Environment Variables

See `projectify/settings/hetzner.py` as well.

The following variables need to be provided in the process environment to
ensure that the Projectify backend will launch correctly.

## General

- `DJANGO_SETTINGS_MODULE`: For Hetzner deployment, use
  `projectify.settings.hetzner`
- `DJANGO_CONFIGURATION`: For Hetzner deployment, use `Hetzner`

## Networking

- `PORT`: Used for gunicorn to determine which port to bind to, OR,
- `SOCKET`: Used for gunicorn to determine which UNIX socket to bind to.
- `FRONTEND_URL`: URL for where Projectify frontend is served.

## Database

- `DATABASE_URL`:
  [dj-database-url](https://github.com/jazzband/dj-database-url) compatible
  database url

# Credentials

Provide the following values as variables in a credentials file. Pass
the file path as the `CREDENTIALS_PATH` environment variable.

## General

- `SECRET_KEY`: Used for session cookie generation

## Error reporting

These two values are used for error logging. When the Django backend logs
an error, it also sends an email to the `ADMIN_EMAIL` email address with the
contents of the logged error.

- `ADMIN_NAME`: Administrator name. The backend prints a warning if this isn't set.
- `ADMIN_EMAIL`: Administrator email address. The backend prints a warning if
  this isn't set.

## Stripe

See also `docs/billing_integration.md`.

- `STRIPE_PUBLISHABLE_KEY`: Stripe key that can be revealed to client. See
  [Stripe's docs](https://docs.stripe.com/keys#obtain-api-keys)
- `STRIPE_SECRET_KEY`: Stripe key that may not be revealed.
- `STRIPE_ENDPOINT_SECRET`: Key used by stripe for signing their requests when
  calling our [webhook](https://docs.stripe.com/webhooks#events-overview).
- `STRIPE_PRICE_OBJECT`: Price object we use for Stripe billing

## Mailgun

- `MAILGUN_API_KEY`: API key for Mailgun
- `MAILGUN_DOMAIN`: Domain used for Mailgun

## OAuth

See `docs/auth.md` under **django-allauth**.

- `ALLAUTH_GITHUB_CLIENT_ID`: GitHub OAuth client id
- `ALLAUTH_GITHUB_SECRET`: GitHub OAuth client secret
- `ALLAUTH_GOOGLE_CLIENT_ID`: Google OAuth client id
- `ALLAUTH_GOOGLE_SECRET`: Google Oauth client secret

## Sample credentials file

Use the following file as a template credentials TOML file:

```toml
SECRET_KEY = "..."

ADMIN_EMAIL = "user@localhost"
ADMIN_NAME = "..."

STRIPE_PUBLISHABLE_KEY = "pk_test_XXX"
STRIPE_SECRET_KEY = "sk_test_XXX"
STRIPE_ENDPOINT_SECRET = "whsec_XXX"
STRIPE_PRICE_OBJECT = "price_XXX"

MAILGUN_API_KEY = "..."
MAILGUN_DOMAIN = "..."

ALLAUTH_GITHUB_CLIENT_ID = "..."
ALLAUTH_GITHUB_SECRET = "..."
ALLAUTH_GOOGLE_CLIENT_ID = "XXX.apps.googleusercontent.com"
ALLAUTH_GOOGLE_SECRET = "GOCSPX-XXX"
```
