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

if ruff --fix "$target"; then
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
