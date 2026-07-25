# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Attachment selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import QuerySet

from projectify.user.models import User

from ..models import WikiPage, Workspace

WikiPageDetailQuerySet = WikiPage.objects.select_related(
    "workspace"
).prefetch_related("workspace__project_set", "workspace__teammember_set")


def wiki_find_recent_changes(
    *, who: User, workspace: "Workspace", qs: QuerySet[WikiPage] | None = None
) -> QuerySet[WikiPage]:
    """Find recently modified wiki pages for a workspace, newest first."""
    if qs is None:
        qs = WikiPage.objects
    return qs.filter(workspace=workspace, workspace__users=who).order_by(
        "-modified"
    )


def wiki_find_by_workspace_and_page_title(
    *,
    who: User,
    ws_uuid: UUID,
    title: str,
    qs: QuerySet[WikiPage] | None = None,
) -> Optional[WikiPage]:
    """Find wiki page by title and for user workspace."""
    if qs is None:
        qs = WikiPage.objects
    return qs.filter(
        workspace__uuid=ws_uuid, workspace__users=who, title=title
    ).first()
