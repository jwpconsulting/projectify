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
cd projectify-backend/backend
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


## Flake

There is a nix flake in this repository.

- https://github.com/nix-community/poetry2nix
- https://github.com/nix-community/nix-direnv

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
