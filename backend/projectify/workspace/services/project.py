# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Project services."""
from datetime import datetime
from typing import Optional

from django.utils.timezone import (
    now,
)

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import Project
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.signals import (
    send_project_change_signal,
    send_workspace_change_signal,
)


# Create
# TODO atomic
def project_create(
    *,
    who: User,
    workspace: Workspace,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
) -> Project:
    """Create a project inside a given workspace."""
    validate_perm("workspace.create_project", who, workspace)
    project = workspace.project_set.create(
        title=title,
        description=description,
        due_date=due_date,
    )
    send_workspace_change_signal(project)
    return project


# Update
# TODO atomic
def project_update(
    *,
    who: User,
    project: Project,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
) -> Project:
    """Update a project."""
    validate_perm("workspace.update_project", who, project.workspace)
    project.title = title
    project.description = description
    if due_date and due_date.tzinfo is None:
        raise ValueError(f"tzinfo must be specified, got {due_date}")
    project.due_date = due_date
    project.save()
    send_workspace_change_signal(project)
    send_project_change_signal(project)
    return project


# Delete
# TODO atomic
def project_delete(
    *,
    who: User,
    project: Project,
) -> None:
    """Delete a project."""
    validate_perm(
        "workspace.delete_project",
        who,
        project.workspace,
    )
    project.delete()
    send_workspace_change_signal(project)
    send_project_change_signal(project)


# RPC
# TODO atomic
def project_archive(
    *,
    who: User,
    project: Project,
    archived: bool,
) -> Project:
    """Archive a project, or not."""
    validate_perm(
        "workspace.update_project",
        who,
        project.workspace,
    )
    if archived:
        project.archived = now()
    else:
        project.archived = None
    project.save()
    send_workspace_change_signal(project)
    send_project_change_signal(project)
    return project
