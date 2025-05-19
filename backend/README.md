<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Projectify Backend

# Development Requirements

- Python 3.12 (I recommend using [asdf](https://asdf-vm.com/))
- [poetry](https://python-poetry.org/docs/)
- [PostgreSQL](https://www.postgresql.org/) >= 15.5
- [Node.js 22](https://github.com/nodejs/node)

## Installing Python 3.12 and Node.js 22

Managing Python and Node.js versions is convenient using [asdf](https://asdf-vm.com/):

```bash
asdf plugin-add python
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
# These are the version used at the time of writing, subject to change
asdf install python 3.12.7
asdf install node.js 22.15.0
```

[Here's how to install asdf](https://asdf-vm.com/guide/getting-started.html)
on your computer.

## Installing PostgreSQL on Debian 12 (bullseye)

Run the following commands to install PostgreSQL 15 on Debian 12:

```bash
sudo apt install postgresql-15 libpq-dev
# Optionally run this, if not using nix flake
sudo apt install libpq-dev
```

Check whether you can connect to your local PostgreSQL instance by using the
following command:

```bash
psql
```

# Installing PostgreSQL on macOS using homebrew

Run the following commands to install PostgreSQL 15 on macOS:

```bash
brew install postgresql@15
brew install libpq
```

Make sure that you can connect to your local PostgreSQL instance by using the
`psql` command.

# Quickstart

To get started, you have to perform the following steps:

1. Clone the repository.
2. Change into the `backend` directory using `cd`.
3. Install all dependencies using the Python `poetry` tool.
4. Create a `.env` environemtn file by copying the `.env.template` file.
5. Edit the `DATABASE_URL` variable in the `.env` file and point it to your
   local PostgreSQL 15 instance.
6. Create a `projectify` PostgreSQL database inside your local PostgreSQL 15
   instance using the `createdb` command.
7. Then, inside a `poetry` shell, perform the following:
  a. Migrate the `projectify` database that you have just created.
  b. Seed the `projectify` database with test data using the `seeddb` command.
  c. Start the development server
  d. Install the Django-Tailwind tool dependencies
  e. Start the Django-Tailwind tool

Run the following commands in your terminal to perform these steps:

```bash
# Clone the repository
git clone git@github.com:jwpconsulting/projectify.git
# Change into the backend directory
cd backend
# Install dependencies
poetry install --with dev --with test --no-root
# Create your `.env` file
cp .env.template .env
# Edit the `.env` file using your preferred editor:
vim .env
# Inside .env, edit the DATABASE_URL, then save your changes.
# Create the database using the PostgreSQL `createdb` command
createdb projectify
```

Configure Projectify using the following management commands:

```bash
# Switch into a poetry shell
poetry shell
# Run the Django migration command
./manage.py migrate
# Seed the database with test data using `seeddb`
./manage.py seeddb
# Start the development server
./manage.py runserver
```

Projectify uses [Django-Tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html) to generate CSS utility classes.
Django-Tailwind uses [tailwindcss](https://tailwindcss.com/).
To configure and start Django-Tailwind in a separate shell, run
the following commands:

```bash
# Make sure that you are in the backend/ directory
# Launch a poetry shell
poetry shell
# Install the tailwind development tool dependencies
./manage.py tailwind install
# Run the tailwind development tool
./manage.py tailwind start
```

Once you have done all of this, go to Django administration page at
<http://localhost:8000/admin/>. The `seeddb` command created an administrator
account with the following credentials for you:

- Username: `admin@localhost`
- Password: `password`

Log in using these credentials and you have full access to the administration
page.

## Celery

If you need to run the celery worker, make sure that you have KeyDB or Redis installed.
KeyDB is compatible with Redis.

- [KeyDB installation instructions](https://docs.keydb.dev/docs/open-source-getting-started)
- [Redis installation instructions](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/)

Make sure that you can access your KeyDB or Redis at the following URL:

```
redis://localhost:6379/0
```

If you have Redis installed, this is how you can test whether the Redis server
is available:

```bash
redis-cli -u redis://localhost:6379/0
```

If you see a message like the following, please check whether Redis is running
correctly:

```
Could not connect to Redis at localhost:6379: Connection refused
```

Now, add the following variable to your `.env` file:

```
REDIS_TLS_URL = redis://localhost:6379/0
```

Once you have made sure that KeyDB or Redis runs correctly, start the `celery`
worker like so:

```bash
# Make sure that you are inside a poetry shell
celery -A projectify worker -c 1
```

## Neovim

You can use Neovim with the [Pyright](https://github.com/microsoft/pyright) Language Server Protococol (LSP) server. To make sure that Neovim uses the right Pyright from
this repository, run neovim inside a poetry environment like so:

```
poetry run nvim
```

# Formatting
```
cd backend
poetry run bin/format.sh
```

# Copyright and licencing information
To look for files missing copyright and licencing information:

```
# Assume you are in backend directory
cd ../tools
poetry install
poetry run reuse lint
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

# Translations

Projectify uses Django's built-in GNU gettext-based translation. Learn more
about Django's translation features [here](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/#translate-template-tag).

You can update the translation files by running the following commands:

```bash
./manage.py makemessages --ignore=bin/ -l en --ignore='gunicorn.conf.py' --ignore=manage.py
```

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
