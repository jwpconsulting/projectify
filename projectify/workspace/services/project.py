# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project services."""

from datetime import datetime
from typing import Optional

from django.utils.timezone import now

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.models import Project
from projectify.workspace.models.workspace import Workspace


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
        title=title, description=description, due_date=due_date
    )
    # 1+1 query?
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
    return project


# Delete
# TODO atomic
def project_delete(*, who: User, project: Project) -> None:
    """Delete a project."""
    validate_perm("workspace.delete_project", who, project.workspace)
    project.delete()


# RPC
# TODO atomic
def project_archive(*, who: User, project: Project, archived: bool) -> Project:
    """Archive a project, or not."""
    validate_perm("workspace.update_project", who, project.workspace)
    if archived:
        project.archived = now()
    else:
        project.archived = None
    project.save()
    return project
