#!/usr/bin/env sh
set -e
poetry run mypy .
poetry run flake8
poetry run pytest -n auto --maxprocesses=8
