<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

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

# MacOS installation (Using homebrew)

Make sure you have Postgres 15 and its dev library installed.

```
brew install postgresql@15
brew install libpq
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
cd backend
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

Go to Django admin page and login at `localhost:8000/admin/`

username: `admin@localhost` \
password: `password`


Furthermore, to run a celery worker:

`celery -A projectify worker -c 1`

To run neovim with the correct pyright:

```
poetry run nvim
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
