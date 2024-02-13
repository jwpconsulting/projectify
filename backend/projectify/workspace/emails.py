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
from projectify.premail.email import (
    TemplateEmail,
)

from . import (
    models,
)


class WorkspaceUserInviteEmail(TemplateEmail[models.WorkspaceUserInvite]):
    """Email that informs users about an invite."""

    model = models.WorkspaceUserInvite
    template_prefix = "workspace/email/workspace_user_invite"

    def get_to_email(self) -> str:
        """Return recipient email."""
        return self.obj.user_invite.email