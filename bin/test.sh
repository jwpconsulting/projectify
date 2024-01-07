#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
