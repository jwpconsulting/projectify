# Simple Todo backend

## Requirements

- Python > 3.8
- pipenv
- PostgreSQL

## Quickstart

```
git clone git@github.com:justuswilhelm/simpletodo-backend.git
cd simpletodo-backend
pipenv install
pipenv shell
cp .env.template .env
vim .env
createdb simpletodo
./manage.py migrate
./manage.py seeddb
./manage.py runserver
```
