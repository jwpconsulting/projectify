"""Workspace emails."""
from premail.email import (
    TemplateEmail,
)

from . import (
    models,
)


class WorkspaceUserInviteEmail(TemplateEmail[models.WorkspaceUser]):
    """Email that informs users about an invite."""

    model = models.WorkspaceUserInvite
    template_prefix = "workspace/email/workspace_user_invite"

    def get_to_email(self) -> str:
        """Return recipient email."""
        return self.obj.user_invite.email
