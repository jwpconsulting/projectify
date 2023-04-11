# Projectify Backend

# Requirements

- Python >= 3.10.9
- pipenv
- PostgreSQL
- Redis (6 >= for production)

## Debian 11 (bullseye) installation

Make sure you have Postgres 13 and its dev library installed.

```
sudo apt install postgresql-13 libpq-dev
```

Managing Python is convenient using asdf:

```
asdf plugin-add python
asdf install python 3.10.9
```

# Quickstart

```
git clone git@github.com:jwp-consulting/projectify-backend.git
cd projectify-backend
pipenv install --dev
pipenv shell
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

# Production Environment Variables

- `DJANGO_SETTINGS_MODULE`
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

# Postgres troubleshooting

> psql: error: FATAL:  role "$USER" does not exist

```
CREATE ROLE $USER WITH LOGIN SUPERUSER;
```

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

Make sure to restart PostgreSQL, e.g. by running

```
sudo systemctl restart postgresql.service
```

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
