#!/usr/bin/env sh
set -e
poetry run isort .
poetry run black .
