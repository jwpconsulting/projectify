# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Workspace selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import Count, Prefetch, Q, QuerySet
from django.db.models.functions import NullIf

from projectify.user.models import User

from ..models.chat_message import ChatMessage
from ..models.label import Label
from ..models.project import Project
from ..models.task import Task
from .labels import labels_annotate_with_colors

TaskDetailQuerySet: QuerySet[Task] = (
    Task.objects.select_related(
        "section__project__workspace",
        "assignee",
        "assignee__user",
    )
    .prefetch_related(
        "subtask_set",
    )
    .prefetch_related(
        Prefetch(
            "labels",
            queryset=labels_annotate_with_colors(Label.objects.all()),
        ),
    )
    .prefetch_related(
        Prefetch(
            "chatmessage_set",
            queryset=ChatMessage.objects.select_related(
                "author",
                "author__user",
            ),
        ),
    )
    .prefetch_related(
        Prefetch(
            "section__project__workspace__project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
    )
    .annotate(
        sub_task_progress=Count(
            "subtask",
            filter=Q(subtask__done=True),
        )
        * 1.0
        / NullIf(Count("subtask"), 0),
    )
)


def task_find_by_task_uuid(
    *, task_uuid: UUID, who: User, qs: Optional[QuerySet[Task]] = None
) -> Optional[Task]:
    """Find a task given a user and uuid."""
    # Special care is needed, one can't write qs or Task.objects since that
    # would cause the given qs to be prematurely evaluated
    qs = Task.objects if qs is None else qs
    try:
        return qs.get(
            section__project__workspace__users=who,
            uuid=task_uuid,
        )
    except Task.DoesNotExist:
        return None
