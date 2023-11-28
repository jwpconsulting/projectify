#!/bin/sh
set -e
target="${1-.}"
echo "Testing $target"

if poetry run mypy "$target"
then
    echo "mypy ran successfully"
else
    echo "There was an error running mypy"
    exit 1
fi

if poetry run pyright "$target"
then
    echo "pyright ran successfully"
else
    echo "There was an error running pyright"
    exit 1
fi

if ! poetry run ruff format --check "$target"
then
    echo "There was an error running ruff format. Attempting to fix"
    if ! poetry run ruff format "$target"
    then
        echo "ruff format didn't finish successfully"
        exit 1
    fi
fi
echo "ruff format ran successfully"

if ! poetry run ruff "$target"
then
    echo "ruff didn't finish successfully"
    if ! poetry run ruff --fix "$target"
    then
        echo "ruff didn't finish successfully"
        exit 1
    fi
fi
echo "ruff ran successfully"

if poetry run pytest -n auto --maxprocesses=8 --lf "$target"
then
    echo "pytest ran successfully"
else
    echo "There was an error running pytest"
    exit 1
fi
