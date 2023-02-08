# Projectify Backend

# Requirements

- Python >= 3.10.9
- pipenv
- PostgreSQL
- Redis (6 >= for production)

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

# License

This project is licensed under AGPL. See the LICENSE file in this repository.
