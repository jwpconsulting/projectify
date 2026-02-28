# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Label services."""

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import Label, Workspace


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
    return label


# Delete
# TODO atomic
def label_delete(*, who: User, label: Label) -> None:
    """Delete a label."""
    validate_perm("workspace.delete_label", who, label.workspace)
    label.delete()
