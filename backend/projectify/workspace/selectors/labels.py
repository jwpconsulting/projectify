"""Selectors for the workspace app Label model."""

import logging
from typing import Optional
from uuid import UUID

from django.db.models import Prefetch, QuerySet

from projectify.user.models.user import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.project import Project

logger = logging.getLogger(__name__)


LabelDetailQuerySet = Label.objects.select_related(
    "workspace"
).prefetch_related(
    Prefetch(
        "workspace__project_set",
        queryset=Project.objects.filter(archived__isnull=True),
    ),
)


def label_find_by_label_uuid(
    *,
    label_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[Label]] = None,
) -> Optional[Label]:
    """Find a label by uuid for a given user."""
    if qs is None:
        qs = Label.objects.all()
    qs = qs.filter(uuid=label_uuid, workspace__users=who)
    try:
        return qs.get()
    except Label.DoesNotExist:
        logger.warning("No label for for UUID %s", label_uuid)
        return None
