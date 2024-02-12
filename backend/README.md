# Projectify Backend

# Requirements

- Python 3.11 (I recommend using [asdf](https://asdf-vm.com/))
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
asdf install python 3.11.4
```

# Quickstart

```
git clone git@github.com:jwp-consulting/projectify-backend.git
cd projectify-backend
poetry install --with dev --with test
poetry shell
cp .env.template .env
vim .env
# Edit DATABASE_URL
# Edit REDIS_TLS_URL
createdb projectify
./manage.py migrate
./manage.py seeddb
./manage.py runserver
```

To run a celery worker:

`celery -A projectify worker -c 1`

To run neovim with the correct pyright:

```
poetry run nvim
```

# Production Environment Variables

- `DJANGO_SETTINGS_MODULE`
- `DJANGO_CONFIGURATION`
- `DATABASE_URL`
- `SECRET_KEY`
- `MAILGUN_API_KEY`
- `MAILGUN_DOMAIN`
- `FRONTEND_URL`
- `REDIS_TLS_URL`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_PRICE_OBJECT`
- `STRIPE_ENDPOINT_SECRET`

# Updating poetry dependencies

When updating a package installed by poetry, make sure to recreate and check in
requirements.txt by running

```
bin/update-requirements
git add requirements.txt
# Maybe git commit here
```

# PostgreSQL troubleshooting

## Use PostgreSQL with unix domain sockets

Referring to the [dj-database-url documentation on URL schema](https://github.com/jazzband/dj-database-url?tab=readme-ov-file#url-schema), we see that we can write unix domain socket paths like so:

```
postgres://%2Fvar%2Flib%2Fpostgresql/dbname
```

In our case, running PostgreSQL 15 installed through Nix on macOS, we see
that there is a socket in `/tmp/.s.PGSQL.5432`. We therefore craft the following link:

```
DATABASE_URL = postgres://%2Ftmp/projectify
```

## Creating a db after installing with MacPorts

Connecting is a big finicky, as you need to navigate away from your home dir
sub folder.

```
pushd /opt/local/lib/postgresql15; sudo -u postgres /opt/local/lib/postgresql15/bin/psql
```

## Psycopg2 installation with macports

Try this:

```
env PATH="/opt/local/lib/postgresql15/bin:$PATH" poetry install
```

## No user role

> psql: error: FATAL:  role "$USER" does not exist

```
CREATE USER $USER WITH CREATEDB;
```

Make sure to run `createdb` if you'd like the bare `psql` command to work.

## Local password-less auth

**Note**: This was written with PostgreSQL 13 in mind.

> django.db.utils.OperationalError: fe_sendauth: no password supplied

```
--- /etc/postgresql/13/main/pg_hba.conf.backup	2023-04-11 11:43:00.074697069 +0900
+++ /etc/postgresql/13/main/pg_hba.conf	2023-04-11 11:43:25.015054408 +0900
@@ -93,9 +93,9 @@
 # "local" is for Unix domain socket connections only
 local   all             all                                     peer
 # IPv4 local connections:
-host    all             all             127.0.0.1/32            md5
+host    all             all             127.0.0.1/32            trust
 # IPv6 local connections:
-host    all             all             ::1/128                 md5
+host    all             all             ::1/128                 trust
 # Allow replication connections from localhost, by a user with the
 # replication privilege.
 local   replication     all                                     peer
```

## PostgreSQL started, but can't connect

Systemctl showed PostgreSQL 15 started, but `psql` couln't connect, not even
as `sudo -u postgres psql`:

```
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
        Is the server running locally and accepting connections on that socket?
```

The solution: `/etc/postgresql/15/main/postgresql.conf` had this line that I
had to fix from

```
port = 5433                             # (change requires restart)
```

to

```
port = 5432                             # (change requires restart)
```

Remember to restart.

## Restarting PostgreSQL

Make sure to restart PostgreSQL, e.g. by running

```
sudo systemctl restart postgresql.service
```

## Flake

There is a nix flake in this repository.

- https://github.com/nix-community/poetry2nix
- https://github.com/nix-community/nix-direnv

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
