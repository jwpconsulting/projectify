"""Label services."""

from projectify.utils import validate_perm
from user.models import User
from workspace.models.label import Label
from workspace.models.workspace import Workspace


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
