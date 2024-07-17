# Projectify Supervisor

Use [Supervisor](http://supervisord.org/index.html) to conveniently launch
all processes as a regular user, without having to use systemd. This means
that supervisor will launch all of the below

- Projectify frontend
- Projectify backend
- Celery background worker
- Reverse proxy

This is useful for

- end-to-end testing Projectify
- verifying server configurations

Why have a `docker-compose.yml` file as well? Building docker containers is
quite slow. With Nix build caching, we can regenerate the frontend and backend
binaries very quickly.

# How to run

Install all dependencies and activate the current folder's nix shell using

```bash
nix shell
```

It's recommended to use [direnv](https://direnv.net/) to automatically activate the shell.

```bash
direnv allow
```

Run supervisord like so, which in turn will run all the relevant processes:

```bash
supervisord -n
```

Seeding the database using `projectify-manage seeddb` is not possible at the
moment.

Create a superuser like so: (excuse the config passing)

```bash
env STRIPE_ENDPOINT_SECRET="" STRIPE_PRICE_OBJECT="" STRIPE_SECRET_KEY="" STRIPE_PUBLISHABLE_KEY="" MAILGUN_DOMAIN="" MAILGUN_API_KEY="" FRONTEND_URL="http://localhost:12000" ALLOWED_HOSTS=localhost SECRET_KEY="" REDIS_URL="redis://localhost:12003" DJANGO_SETTINGS_MODULE=projectify.settings.production DJANGO_CONFIGURATION=Production DATABASE_URL="sqlite:///projectify-backend.sqlite" SECRET_KEY=do-not-use-in-production projectify-manage shell
```

```python
from projectify.user.services import internal
internal.user_create_superuser(email="admin@localhost", password="password")
```
