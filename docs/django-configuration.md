<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring the Projectify backend

This document contains a listing of all required backend (including worker and
Django manage command) environment variables. Furthermore, a brief explanation
of the backend's usage of _django configurations_ is included.

# Production Environment Variables

The following variables need to be provided in the process environment to
ensure that the Projectify backend will launch correctly.

## General

- `DJANGO_SETTINGS_MODULE`: Usually set to `projectify.settings.production`
- `DJANGO_CONFIGURATION`: Usually set to `Production`
- `SECRET_KEY`: Used for session cookie generation
- `SITE_TITLE` (**optional**): Title of site, defaults to
  `Projectify Production`

## Error reporting

These two values are used for error logging. When the Django backend logs
an error, it also sends an email to the `ADMIN_EMAIL` email address with the
contents of the logged error.

- `ADMIN_NAME`: Administrator name. The backend prints a warning if this isn't set.
- `ADMIN_EMAIL`: Administrator email address. The backend prints a warning if
  this isn't set.

## Networking

- `PORT`: Used for gunicorn to determine which port to bind to
- `ALLOWED_HOSTS`: Which host names to permit in HTTP Host header. Comma
  separated values.
- `FRONTEND_URL`: URL for where Projectify frontend is served.
- `SECURITY_ORIGINS` (**optional**): Allowed URLs for
  [CORS](https://pypi.org/project/django-cors-headers/)/[CSRF](https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-trusted-origins).
  Defaults to `ALLOWED_HOSTS`.
- `CSRF_COOKIE_DOMAIN` (**optional**): Domain for CSRF cookie. Defaults to
  None. See
  [Django documentation](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-CSRF_COOKIE_DOMAIN);

## Database

- `DATABASE_URL`:
  [dj-database-url](https://github.com/jazzband/dj-database-url) compatible
  database url

## Stripe

See also `docs/billing_integration.md`.

- `STRIPE_PUBLISHABLE_KEY`: Stripe key that can be revealed to client. See
  [Stripe's docs](https://docs.stripe.com/keys#obtain-api-keys)
- `STRIPE_SECRET_KEY`: Stripe key that may not be revealed.
- `STRIPE_PRICE_OBJECT`: Price object we use for Stripe billing
- `STRIPE_ENDPOINT_SECRET`: Key used by stripe for signing their requests when
  calling our [webhook](https://docs.stripe.com/webhooks#events-overview).

## Mailgun

- `MAILGUN_API_KEY`: API key for Mailgun
- `MAILGUN_DOMAIN`: Domain used for Mailgun

## OAuth

See `docs/auth.md` under **django-allauth**.

- `ALLAUTH_GITHUB_CLIENT_ID`: GitHub OAuth client id
- `ALLAUTH_GITHUB_SECRET`: GitHub OAuth client secret
- `ALLAUTH_GOOGLE_CLIENT_ID`: Google OAuth client id
- `ALLAUTH_GOOGLE_SECRET`: Google Oauth client secret
