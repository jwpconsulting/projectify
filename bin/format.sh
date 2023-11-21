#!/usr/bin/env sh
set -e
poetry run ruff format .
poetry run ruff --fix .
