#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
# Note:
# This script prefixes commands with `uv run`
set -e
target="${1-.}"
echo "Testing $target"

if uv run mypy "$target"
then
    echo "mypy ran successfully"
else
    echo "There was an error running mypy"
    exit 1
fi

if uv run ruff format "$target"; then
    echo "ruff format ran successfully"
else
    echo "ruff format didn't finish successfully"
    exit 1
fi

if uv run djlint --check "$target"
then
    echo "djlint --check ran successfully"
else
    echo "There was an error running djlint --check"
    uv run djlint --reformat "$target"
    if ! uv run djlint --check "$target"; then
        echo "Couldn't fix with djlint --reformat"
        exit 1
    fi
fi

if uv run ruff check --fix "$target"; then
    echo "ruff ran successfully"
else
    echo "ruff didn't finish successfully"
    exit 1
fi

if uv run djlint --lint "$target"
then
    echo "djlint --lint ran successfully"
else
    echo "There was an error running djlint --lint"
    exit 1
fi

if uv run pytest -n auto --lf "$target"
then
    echo "pytest ran successfully"
else
    echo "There was an error running pytest"
    exit 1
fi

if uv run vulture .
then
    echo "Vulture did not find any issues"
else
    echo "There were some issues when running vulture. See the output above."
    exit 1
fi

if uv run reuse lint
then
    echo "reuse lint did not find any issues"
else
    echo "There was an error running reuse lint"
    exit 1
fi
