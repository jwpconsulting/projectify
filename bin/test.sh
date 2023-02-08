#!/usr/bin/env sh
set -e
pipenv run flake8
pipenv run pytest
