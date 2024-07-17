# Configuring the Projectify backend

This document contains a listing of all required backend (including worker
and Django manage command) environment variables. Furthermore, a brief
explanation of the backend's usage of _django configurations_ is included.

# Production Environment Variables

The following variables need to be provided in the process environment to
ensure that the Projectify backend will launch correctly.

## General
- `DJANGO_SETTINGS_MODULE`: Usually set to `projectify.settings.production`
- `DJANGO_CONFIGURATION`: Usually set to `Production`
- `SECRET_KEY`: Used for session cookie generation, Redis symmetric encryption

## Networking
- `PORT`: Used for gunicorn to determine which port to bind to
- `ALLOWED_HOSTS`: Which host names to permit in HTTP Host header. Comma
separated values.
- `FRONTEND_URL`: URL for where Projectify frontend is served.

## Database
- `DATABASE_URL`:
[dj-database-url](https://github.com/jazzband/dj-database-url) compatible
database url
- `REDIS_TLS_URL`: URL for Redis server. Might work with keydb. TLS cert not
verified. Use `REDIS_URL` instead for even fewer dubious security merits.

## Stripe
- `STRIPE_PUBLISHABLE_KEY`: Stripe key that can be revealed to client. See
[Stripe's docs](https://docs.stripe.com/keys#obtain-api-keys)
- `STRIPE_SECRET_KEY`: Stripe key that may not be revealed.
- `STRIPE_PRICE_OBJECT`: Price object we use for Stripe billing
- `STRIPE_ENDPOINT_SECRET`: Key used by stripe for signing their requests when
  calling our [webhook](https://docs.stripe.com/webhooks#events-overview).

## Mailgun

- `MAILGUN_API_KEY`: API key for Mailgun
- `MAILGUN_DOMAIN`: Domain used for Mailgun

# Internals

We would like to use _django configurations_ by jazzband.

- [Repository](https://github.com/jazzband/django-configurations)
- [Documentation](https://django-configurations.readthedocs.io/en/latest/)

Some other options are

- [Django Classy
  Settings](https://django-classy-settings.readthedocs.io/en/latest/)
- [django-class-settings](https://django-class-settings.readthedocs.io/en/latest/)

But given that jazzband has a good reputation of maintaining packages
long-term, we choose to go with the first option.

## Problems that need solving

### Middleware

Django debug toolbar is in the middleware, always. Even if we launch the Projectify backend in production mode, it is still there. Not only does that slow down the
application, but one can't help but feel anxiety over a _debug_ toolbar
potentially leaking into a production application.

### Failed deploys

Too often, we have settings that break only during production because
environment variable edge cases are not handled neatly. The redis instance unit
on Heroku having a different environment variable depending on whether it is
free or not. If we are able to define data types here, we could potentially
have a static type checker catch these issues.

### Weird module import based inheritance

The way it is right now, we are importing from projectify.settings.base into
each individual settings module. That is sort of like inheritance, but much
less predictable.
