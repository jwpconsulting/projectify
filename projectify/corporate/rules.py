# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""
Corporate app rules.

The order of rules follows the ordering of models.
"""
import rules

from workspace.rules import (
    is_at_least_owner,
)

# Customer
rules.add_perm(
    "corporate.can_create_customer",
    is_at_least_owner,
)
rules.add_perm(
    "corporate.can_read_customer",
    is_at_least_owner,
)
rules.add_perm(
    "corporate.can_update_customer",
    is_at_least_owner,
)
rules.add_perm(
    "corporate.can_delete_customer",
    is_at_least_owner,
)
