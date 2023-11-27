"""Label services."""

from projectify.utils import validate_perm
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
    label = Label(
        workspace=workspace,
        name=name,
        color=color,
    )
    label.save()
    return label


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
