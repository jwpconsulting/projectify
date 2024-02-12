# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.signals import send_workspace_change_signal


# Create
# TODO atomic
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
    label = Label.objects.create(workspace=workspace, name=name, color=color)
    send_workspace_change_signal(workspace)
    return label


# Update
# TODO atomic
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
    send_workspace_change_signal(label.workspace)
    return label


# Delete
# TODO atomic
def label_delete(*, who: User, label: Label) -> None:
    """Delete a label."""
    validate_perm("workspace.can_delete_label", who, label)
    label.delete()
    send_workspace_change_signal(label.workspace)
