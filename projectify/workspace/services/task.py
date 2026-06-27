# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Task services."""

import logging
from datetime import datetime
from typing import Optional

from django.db import transaction
from django.forms import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from projectify.lib.auth import validate_perm
from projectify.user.models import User
from projectify.workspace.utils import extract_first_paragraph_text

from ..models import Project, Task, TeamMember

logger = logging.getLogger(__name__)


@transaction.atomic
def task_create(
    *,
    who: User,
    project: Project,
    title_description: str,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Create a task. This will replace the above task_create method."""
    validate_perm("workspace.create_task", who, project.workspace)
    # XXX Implicit N+1 here
    workspace = project.workspace
    if assignee and assignee.workspace != workspace:
        raise ValidationError(
            {
                "assignee": [
                    _(
                        "The team member to be assigned belongs to a different workspace"
                    )
                ]
            }
        )

    match extract_first_paragraph_text(title_description):
        case str() as title:
            pass
        case None:
            title = title_description

    task = Task.objects.create(
        project=project,
        title=title,
        description=title_description,
        due_date=due_date,
        workspace=workspace,
        assignee=assignee,
    )
    return task


# Update
@transaction.atomic
def task_update(
    *,
    who: User,
    task: Task,
    title_description: str,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Update task."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.description = title_description
    task.due_date = due_date
    task.assignee = assignee

    match extract_first_paragraph_text(title_description):
        case str() as title:
            task.title = title
        # Keep the task title when nothing matches
        case None:
            pass

    task.save()
    return task


@transaction.atomic
def task_mark_done(*, who: User, task: Task, done: bool) -> Task:
    """Mark task as done."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.done = now() if done else None
    task.save()
    return task


# Delete
# TODO atomic
def task_delete(*, task: Task, who: User) -> None:
    """Delete a task."""
    validate_perm("workspace.delete_task", who, task.workspace)
    task.delete()
