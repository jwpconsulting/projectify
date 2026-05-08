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
- `ALLOWED_HOST`: Allowed host name
- `STATIC_ROOT`: Where to store static files
- `MEDIA_ROOT`: Where to store user uploaded files

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

## Emails

Set the email *from* address with the following credential value:

- `DEFAULT_FROM_EMAIL` (optional): default is `"Projectify" <hello@projectifyapp.com>`

Projectify uses the `DEFAULT_FROM_EMAIL` address for the following emails:

- Transactional emails to user
- Error messages to administrator at `ADMIN_EMAIL`

If you use an SMTP server with implicit TLS (port 465), set these credentials:

- `EMAIL_HOST`: The hostname of the SMTP server to connect to.
- `EMAIL_PORT` (optional): Projectify assumes it can reach your mail server at
  port 465 by default if you don't set this value.
- `EMAIL_HOST_USER`: The username to authenticate as when connecting to the
  SMTP server at `EMAIL_HOST`.
- `EMAIL_HOST_PASSWORD`: The password to authenticate with when connecting to the
  SMTP server at `EMAIL_HOST`.

If you use Lettermint, make sure to active the **Enable SMTP** setting
in the **Settings** tab for your Lettermint project. You can reach the
project settings by going the **Projects** page from the left navigation
bar. Then,

1. create an **API token** and use it as the `EMAIL_HOST_PASSWORD` for
Projectify.
2. Use `smpt.lettermint.co` as `EMAIL_HOST`.
3. Use `lettermint` as `EMAIL_HOST_USER`.

If you want to use explicil TLS and you can reach your SMTP server at port 587,
set `EMAIL_PORT` to `587`.

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

EMAIL_HOST = "smtp...."
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# Optional:
EMAIL_HOST_PORT

ALLAUTH_GITHUB_CLIENT_ID = "..."
ALLAUTH_GITHUB_SECRET = "..."
ALLAUTH_GOOGLE_CLIENT_ID = "XXX.apps.googleusercontent.com"
ALLAUTH_GOOGLE_SECRET = "GOCSPX-XXX"
```
