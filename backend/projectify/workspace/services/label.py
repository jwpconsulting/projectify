# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Label services."""

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.signals import send_change_signal


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
    validate_perm("workspace.create_label", who, workspace)
    label = Label.objects.create(workspace=workspace, name=name, color=color)
    send_change_signal("changed", workspace)
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
    validate_perm("workspace.update_label", who, label.workspace)
    label.name = name
    label.color = color
    label.save()
    send_change_signal("changed", label.workspace)
    return label


# Delete
# TODO atomic
def label_delete(*, who: User, label: Label) -> None:
    """Delete a label."""
    validate_perm("workspace.delete_label", who, label.workspace)
    label.delete()
    send_change_signal("changed", label.workspace)
