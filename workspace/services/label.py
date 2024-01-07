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
"""Label services."""

from projectify.lib.auth import validate_perm
from user.models import User
from workspace.models.label import Label
from workspace.models.workspace import Workspace


# Create
def label_create(
    *,
    workspace: Workspace,
    name: str,
    # TODO enum this?
    color: int,
    who: User,
) -> Label:
    """Create a label."""
    validate_perm("workspace.can_create_label", who, workspace)
    return Label.objects.create(
        workspace=workspace,
        name=name,
        color=color,
    )


# Update
def label_update(
    *,
    who: User,
    label: Label,
    name: str,
    color: int,
) -> Label:
    """Update a label with new name and color."""
    validate_perm("workspace.can_update_label", who, label)
    label.name = name
    label.color = color
    label.save()
    return label


# Delete
def label_delete(*, who: User, label: Label) -> None:
    """Delete a label."""
    validate_perm("workspace.can_delete_label", who, label)
    label.delete()
