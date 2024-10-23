# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import QuerySet

from projectify.user.models import User
from projectify.workspace.models.section import (
    Section,
)

SectionDetailQuerySet = Section.objects.prefetch_related(
    "task_set",
    "task_set__assignee",
    "task_set__assignee__user",
    "task_set__labels",
    "task_set__subtask_set",
).select_related(
    "project",
    "project__workspace",
)


def section_find_for_user_and_uuid(
    *,
    section_uuid: UUID,
    user: User,
    qs: Optional[QuerySet[Section]] = None,
) -> Optional[Section]:
    """
    Find a section given a UUID and a user.

    Allows specifying optional base queryset.
    """
    if qs is None:
        qs = Section.objects
    try:
        return qs.filter(
            project__workspace__users=user,
            uuid=section_uuid,
        ).get()
    except Section.DoesNotExist:
        return None
