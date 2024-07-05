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
