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
"""Project model selectors."""
from typing import Optional
from uuid import UUID

from django.db.models import (
    Count,
    Prefetch,
    Q,
    QuerySet,
)
from django.db.models.functions import NullIf

from projectify.user.models import User
from projectify.workspace.models.task import Task

from ..models.project import Project

ProjectDetailQuerySet = Project.objects.prefetch_related(
    "section_set",
    Prefetch(
        "section_set__task_set",
        queryset=Task.objects.annotate(
            sub_task_progress=Count(
                "subtask",
                filter=Q(subtask__done=True),
            )
            * 1.0
            / NullIf(Count("subtask"), 0),
        ).order_by("-_order"),
    ),
    "section_set__task_set__assignee",
    "section_set__task_set__assignee__user",
    "section_set__task_set__labels",
    "workspace__label_set",
    "workspace__project_set",
    "workspace__teammember_set",
    "workspace__teammember_set__user",
    "workspace__teammemberinvite_set",
).select_related(
    "workspace",
)


def project_find_by_workspace_uuid(
    *, workspace_uuid: UUID, who: User, archived: Optional[bool] = None
) -> QuerySet[Project]:
    """Find projects for a workspace."""
    qs = Project.objects.filter(
        workspace__users=who, workspace__uuid=workspace_uuid
    )
    if archived is not None:
        qs = qs.filter(archived__isnull=not archived)
    return qs


def project_find_by_project_uuid(
    *,
    project_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[Project]] = None,
    archived: bool = False,
) -> Optional[Project]:
    """Find a workspace by uuid for a given user."""
    qs = Project.objects.all() if qs is None else qs
    qs = qs.filter(archived__isnull=not archived)
    qs = qs.filter(workspace__users=who, uuid=project_uuid)
    try:
        return qs.get()
    except Project.DoesNotExist:
        return None
