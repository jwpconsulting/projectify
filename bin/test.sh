#!/bin/sh
set -e
target="${1-.}"
if poetry run mypy "$target"
then
    echo "mypy ran successfully"
else
    echo "There was an error running mypy"
    exit 1
fi
if poetry run flake8 "$target"
then
    echo "flake8 ran successfully"
else
    echo "There was an error running flake8"
    exit 1
fi
if poetry run pytest -n auto --maxprocesses=8 --lf "$target"
then
    echo "pytest ran successfully"
else
    echo "There was an error running pytest"
    exit 1
fi
