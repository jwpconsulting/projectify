#!/usr/bin/env sh
set -e
export DJANGO_SETTINGS_MODULE=projectify.settings.test
export TEST_STATICFILES_STORAGE=
poetry run ./manage.py collectstatic --noinput
