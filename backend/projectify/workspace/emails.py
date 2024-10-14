# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Workspace emails."""

from django.utils import timezone

from projectify.premail.email import (
    Context,
    EmailAddress,
    TemplateEmail,
)
from projectify.user.models.user import User

from .models.team_member_invite import TeamMemberInvite


class TeamMemberInviteEmail(TemplateEmail[TeamMemberInvite]):
    """Email that informs users about an invite."""

    model = TeamMemberInvite
    template_prefix = "workspace/email/team_member_invite"

    def __init__(
        self, *, receiver: EmailAddress, obj: TeamMemberInvite, who: User
    ):
        """Designate receiver."""
        self.receiver = receiver
        self.obj = obj
        self.who = who

    def get_context(self) -> Context:
        """Add name of inviter, current date."""
        return {
            **super().get_context(),
            "invited_by": self.who.preferred_name or self.who.email,
            "when": timezone.now(),
            "workspace_title": self.obj.workspace.title,
        }
