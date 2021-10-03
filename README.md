# Simple Todo backend

# Requirements

- Python > 3.8
- pipenv
- PostgreSQL

# Quickstart

```
git clone git@github.com:justuswilhelm/simpletodo-backend.git
cd simpletodo-backend
pipenv install
pipenv shell
cp .env.template .env
vim .env
# Edit DATABASE_URL
createdb simpletodo
./manage.py migrate
./manage.py seeddb
./manage.py runserver
```

# Production Environment Variables

- `DJANGO_SETTINGS_MODULE`
- `DATABASE_URL`
- `SECRET_KEY`
