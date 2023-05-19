#!/usr/bin/env sh
set -e
pipenv run mypy .
pipenv run flake8
pipenv run pytest -n auto --maxprocesses=8
