#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Note:
# Run within a poetry, nix, or similar environment
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

if pyright "$target"
then
    echo "pyright ran successfully"
else
    echo "There was an error running pyright"
    exit 1
fi

if ruff format "$target"; then
    echo "ruff format ran successfully"
else
    echo "ruff format didn't finish successfully"
    exit 1
fi

if ruff check --fix "$target"; then
    echo "ruff ran successfully"
else
    echo "ruff didn't finish successfully"
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
fi
