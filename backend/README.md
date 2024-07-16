# Projectify Backend

# Requirements

- Python ~3.11.6 (I recommend using [asdf](https://asdf-vm.com/))
- [poetry](https://python-poetry.org/docs/)
- PostgreSQL >= 15.5
- Redis (6 >= for production)

## Debian 12 (bullseye) installation

Make sure you have Postgres 15 and its dev library installed.

```
sudo apt install postgresql-15 libpq-dev
# Optionally run this, if not using nix flake
sudo apt install libpq-dev
```

Managing Python is convenient using asdf:

```
asdf plugin-add python
# This is the version used at the time of writing, subject to change
asdf install python 3.11.6
```

# Quickstart

To get started, you have to

1. Clone the repository,
2. cd into `backend` directory,
3. create a `.env` file from `.env.template`,
4. edit the `.env` file to add a `DATABASE_URL` and `REDIS_TLS_URL` for a local
   Redis and PostgreSQL 15 instance, and
5. create the projectify PostgreSQL database. Then,
6. inside a poetry shell,
  a. migrate the database,
  b. seed it with test data, and then
  c. run the development server

The commands to run are these:

```
git clone git@github.com:jwp-consulting/projectify-backend.git
cd projectify-backend/backend
poetry install --with dev --with test --no-root
cp .env.template .env
vim .env
# Inside .env:
# 1) Edit DATABASE_URL
# 2) Edit REDIS_TLS_URL
# Create the database
createdb projectify
# Now you can run the server
poetry shell
./manage.py migrate
./manage.py seeddb
./manage.py runserver
```

Furthermore, to run a celery worker:

`celery -A projectify worker -c 1`

To run neovim with the correct pyright:

```
poetry run nvim
```

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

# Updating poetry dependencies

When updating a package installed by poetry, make sure to recreate and check in
requirements.txt by running

```bash
poetry lock --no-update
poetry install --sync
bin/update-requirements
git add requirements.txt
# Maybe git commit here
```

# Nix

The Projectify backend can be run using Nix. There are three entry points to
the application:

- projectify-backend: the Projectify backend wrapped inside gunicorn
- projectify-celery: the Projectify background worker wrapped in celery
- projectify-manage: the Projectify backend's management tool, using Django
management commands.

There are sample configuration variables in `.env.production-sample`. These are
all variables needed to load up the above three commands.

Assuming you have direnv installed, all the necessary configuration variables
can be exposed using `dotenv -f .env.production run COMMAND`.

## Launching projectify-backend

You can launch and test the start-up behavior of a production-like `projectify-backend` locally like so:

<!-- Note: update if production variables change -->

```bash
# Adjust env vars accordingly
env PORT=2000 STRIPE_ENDPOINT_SECRET= STRIPE_PRICE_OBJECT= STRIPE_SECRET_KEY= STRIPE_PUBLISHABLE_KEY= MAILGUN_DOMAIN= MAILGUN_API_KEY= FRONTEND_URL= ALLOWED_HOSTS=localhost SECRET_KEY= REDIS_URL= DJANGO_SETTINGS_MODULE=projectify.settings.production DJANGO_CONFIGURATION=Production nix run .#projectify-backend
```

## Launching projectify-celery

You can launch a production-like `projectify-celery` locally like so:

```
dotenv -f .env.production-sample run nix run .#projectify-celery
```

## Launching projectify-manage

You can launch a production-like `projectify-manage` locally like so:

```
dotenv -f .env.production-sample run nix run .#projectify-manage help
```

## Flake

There is a nix flake in this repository.

- https://github.com/nix-community/poetry2nix
- https://github.com/nix-community/nix-direnv

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
