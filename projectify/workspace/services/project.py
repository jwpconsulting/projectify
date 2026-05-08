# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project services."""

from datetime import datetime
from typing import Optional

from django.db import transaction
from django.utils.timezone import now

from projectify.lib.auth import validate_perm
from projectify.lib.utils import extract_first_paragraph_text
from projectify.user.models import User
from projectify.workspace.models import Project, Workspace


# Create
@transaction.atomic
def project_create(
    *,
    who: User,
    workspace: Workspace,
    title_description: str,
    due_date: Optional[datetime] = None,
) -> Project:
    """Create a project inside a given workspace."""
    validate_perm("workspace.create_project", who, workspace)

    match extract_first_paragraph_text(title_description):
        case str() as title:
            pass
        case None:
            title = title_description

    project = workspace.project_set.create(
        title=title, description=title_description, due_date=due_date
    )
    # 1+1 query?
    return project


# Update
@transaction.atomic
def project_update(
    *,
    who: User,
    project: Project,
    title_description: str,
    due_date: Optional[datetime] = None,
) -> Project:
    """Update a project."""
    validate_perm("workspace.update_project", who, project.workspace)

    match extract_first_paragraph_text(title_description):
        case str() as title:
            pass
        case None:
            title = title_description

    project.title = title
    project.description = title_description

    if due_date and due_date.tzinfo is None:
        raise ValueError(f"tzinfo must be specified, got {due_date}")
    project.due_date = due_date
    project.save()
    return project


# Delete
@transaction.atomic
def project_delete(*, who: User, project: Project) -> None:
    """Delete a project."""
    validate_perm("workspace.delete_project", who, project.workspace)
    project.delete()


# RPC
@transaction.atomic
def project_archive(*, who: User, project: Project, archived: bool) -> Project:
    """Archive a project, or not."""
    validate_perm("workspace.update_project", who, project.workspace)
    if archived:
        project.archived = now()
    else:
        project.archived = None
    project.save()
    return project
