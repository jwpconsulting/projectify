#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
# Note:
# Run within uv shell, nix flake shell, or similar environment
set -e
target="${1-.}"
echo "Testing $target"

if mypy "$target"
then
    echo "mypy ran successfully"
else
    echo "There was an error running mypy"
    exit 1
fi

if ruff format "$target"; then
    echo "ruff format ran successfully"
else
    echo "ruff format didn't finish successfully"
    exit 1
fi

if djlint --check "$target"
then
    echo "djlint --check ran successfully"
else
    echo "There was an error running djlint --check"
    djlint --reformat "$target"
    if ! djlint --check "$target"; then
        echo "Couldn't fix with djlint --reformat"
        exit 1
    fi
fi

if ruff check --fix "$target"; then
    echo "ruff ran successfully"
else
    echo "ruff didn't finish successfully"
    exit 1
fi

if djlint --lint "$target"
then
    echo "djlint --lint ran successfully"
else
    echo "There was an error running djlint --lint"
    exit 1
fi

if pytest -n auto --maxprocesses=8 --lf "$target"
then
    echo "pytest ran successfully"
else
    echo "There was an error running pytest"
    exit 1
fi

if vulture .
then
    echo "Vulture did not find any issues"
else
    echo "There were some issues when running vulture. See the output above."
    exit 1
fi

if reuse lint
then
    echo "reuse lint did not find any issues"
else
    echo "There was an error running reuse lint"
    exit 1
fi
