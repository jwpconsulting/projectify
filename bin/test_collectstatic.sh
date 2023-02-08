#!/usr/bin/env sh
set -e
export PIPENV_DOTENV_LOCATION=.env.test-collectstatic
pipenv run ./manage.py collectstatic --noinput
