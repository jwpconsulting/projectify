# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
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
"""
Workspace app rules.

The order of rules follows the ordering of models.
"""
from functools import partial

import rules

from projectify.user.models import User

from .models.const import TeamMemberRoles
from .models.workspace import Workspace
from .selectors.quota import Resource, workspace_quota_for
from .selectors.team_member import team_member_find_for_workspace

ROLE_EQUIVALENCE = {
    TeamMemberRoles.OWNER: {
        TeamMemberRoles.OWNER: True,
        TeamMemberRoles.MAINTAINER: True,
        TeamMemberRoles.CONTRIBUTOR: True,
        TeamMemberRoles.OBSERVER: True,
    },
    TeamMemberRoles.MAINTAINER: {
        TeamMemberRoles.OWNER: False,
        TeamMemberRoles.MAINTAINER: True,
        TeamMemberRoles.CONTRIBUTOR: True,
        TeamMemberRoles.OBSERVER: True,
    },
    TeamMemberRoles.CONTRIBUTOR: {
        TeamMemberRoles.OWNER: False,
        TeamMemberRoles.MAINTAINER: False,
        TeamMemberRoles.CONTRIBUTOR: True,
        TeamMemberRoles.OBSERVER: True,
    },
    TeamMemberRoles.OBSERVER: {
        TeamMemberRoles.OWNER: False,
        TeamMemberRoles.MAINTAINER: False,
        TeamMemberRoles.CONTRIBUTOR: False,
        TeamMemberRoles.OBSERVER: True,
    },
}


def check_permissions_for(
    role: TeamMemberRoles, user: User, workspace: Workspace
) -> bool:
    """Check whether a user has required role for target."""
    team_member = team_member_find_for_workspace(
        workspace=workspace, user=user
    )
    if team_member is None:
        return False
    team_member_role: TeamMemberRoles = TeamMemberRoles[
        team_member.role
    ]
    return ROLE_EQUIVALENCE[team_member_role][role]


# Role predicates
# ---------------
# Observer < Contributor < Maintainer < Owner
is_at_least_observer = rules.predicate(
    partial(check_permissions_for, TeamMemberRoles.OBSERVER)
)
is_at_least_contributor = rules.predicate(
    partial(check_permissions_for, TeamMemberRoles.CONTRIBUTOR)
)
is_at_least_maintainer = rules.predicate(
    partial(check_permissions_for, TeamMemberRoles.MAINTAINER)
)
is_at_least_owner = rules.predicate(
    partial(check_permissions_for, TeamMemberRoles.OWNER)
)


def can_create_more(
    resource: Resource, _user: User, workspace: Workspace
) -> bool:
    """Extract .can_create_more from workspace_quota_for."""
    return workspace_quota_for(
        resource=resource, workspace=workspace
    ).can_create_more


# Quota predicates
# ----------------
# Return True if a chat message can be created for workspace
within_chat_message_quota = rules.predicate(
    partial(can_create_more, "ChatMessage")
)
# Return True if a label can be created for workspace
within_label_quota = rules.predicate(partial(can_create_more, "Label"))
# Return True if a sub task can be created in workspace
within_sub_task_quota = rules.predicate(partial(can_create_more, "SubTask"))
# Return True if a task can be created in workspace
within_task_quota = rules.predicate(partial(can_create_more, "Task"))
# Return True if a task label can be created for a task
within_task_label_quota = rules.predicate(
    partial(can_create_more, "TaskLabel")
)
# Return True if a project can be created in workspace
within_project_quota = rules.predicate(partial(can_create_more, "Project"))
# Return True if a section can be created in a workspace
within_section_quota = rules.predicate(partial(can_create_more, "Section"))
# Return True if a team member can be added to a workspace
# The two following use the same quota
within_team_member_quota = rules.predicate(
    partial(can_create_more, "TeamMemberAndInvite")
)
# Return True if a team member invite can be sent for a workspace
within_team_member_invite_quota = within_team_member_quota


# Workspace
# Anyone should be able to create a workspace
rules.add_perm("workspace.create_workspace", rules.is_active)
rules.add_perm("workspace.read_workspace", is_at_least_observer)
rules.add_perm("workspace.update_workspace", is_at_least_owner)
rules.add_perm("workspace.delete_workspace", is_at_least_owner)

# Team member invite
rules.add_perm(
    "workspace.create_team_member_invite",
    is_at_least_owner & within_team_member_invite_quota,
)
rules.add_perm("workspace.read_team_member_invite", is_at_least_owner)
rules.add_perm("workspace.update_team_member_invite", is_at_least_owner)
rules.add_perm("workspace.delete_team_member_invite", is_at_least_owner)

# Team member
rules.add_perm(
    "workspace.create_team_member",
    is_at_least_owner & within_team_member_quota,
)
rules.add_perm("workspace.read_team_member", is_at_least_observer)
rules.add_perm("workspace.update_team_member", is_at_least_owner)
rules.add_perm("workspace.delete_team_member", is_at_least_owner)

# Project
rules.add_perm(
    "workspace.create_project",
    is_at_least_maintainer & within_project_quota,
)
rules.add_perm("workspace.read_project", is_at_least_observer)
rules.add_perm("workspace.update_project", is_at_least_maintainer)
rules.add_perm("workspace.delete_project", is_at_least_maintainer)

# Section
rules.add_perm(
    "workspace.create_section",
    is_at_least_maintainer & within_section_quota,
)
rules.add_perm("workspace.read_section", is_at_least_observer)
rules.add_perm("workspace.update_section", is_at_least_maintainer)
rules.add_perm("workspace.delete_section", is_at_least_maintainer)

# Task
rules.add_perm(
    "workspace.create_task", is_at_least_contributor & within_task_quota
)
rules.add_perm("workspace.read_task", is_at_least_observer)
rules.add_perm("workspace.update_task", is_at_least_contributor)
rules.add_perm("workspace.delete_task", is_at_least_maintainer)

# Label
rules.add_perm(
    "workspace.create_label", is_at_least_maintainer & within_label_quota
)
rules.add_perm("workspace.read_label", is_at_least_observer)
rules.add_perm("workspace.update_label", is_at_least_maintainer)
rules.add_perm("workspace.delete_label", is_at_least_maintainer)

# Task label
rules.add_perm(
    "workspace.create_task_label",
    is_at_least_contributor & within_task_label_quota,
)
rules.add_perm("workspace.read_task_label", is_at_least_observer)
rules.add_perm("workspace.update_task_label", is_at_least_contributor)
rules.add_perm("workspace.delete_task_label", is_at_least_contributor)


# Sub task
rules.add_perm(
    "workspace.create_sub_task",
    is_at_least_contributor & within_sub_task_quota,
)
rules.add_perm("workspace.read_sub_task", is_at_least_observer)
rules.add_perm("workspace.update_sub_task", is_at_least_contributor)
rules.add_perm("workspace.delete_sub_task", is_at_least_contributor)

# Chat message
rules.add_perm(
    "workspace.create_chat_message",
    is_at_least_contributor & within_chat_message_quota,
)
rules.add_perm("workspace.read_chat_message", is_at_least_observer)
rules.add_perm("workspace.update_chat_message", is_at_least_contributor)
rules.add_perm("workspace.delete_chat_message", is_at_least_maintainer)
