#!/usr/bin/env sh
set -e
export PIPENV_DOTENV_LOCATION=.env.test
export TEST_STATICFILES_STORAGE=
pipenv run ./manage.py collectstatic --noinput
