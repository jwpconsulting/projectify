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

from ..models import Section, Task, TeamMember

logger = logging.getLogger(__name__)


@transaction.atomic
def task_create(
    *,
    who: User,
    section: Section,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Create a task. This will replace the above task_create method."""
    validate_perm("workspace.create_task", who, section.project.workspace)
    # XXX Implicit N+1 here
    workspace = section.project.workspace
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
    task = Task.objects.create(
        section=section,
        title=title,
        description=description,
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
    title: str,
    description: Optional[str] = None,
    due_date: Optional[datetime] = None,
    assignee: Optional[TeamMember] = None,
) -> Task:
    """Update task."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.title = title
    task.description = description
    task.due_date = due_date
    task.assignee = assignee
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


@transaction.atomic
def task_move_after(*, who: User, task: Task, after: Section) -> Task:
    """Move a task to a new a section."""
    validate_perm("workspace.update_task", who, task.workspace)
    task.section = after
    task.save()
    return task
