# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Workspace Wiki services."""

from django.utils.translation import gettext_lazy as _

from projectify.lib.auth import validate_perm
from projectify.user.models import User

from ..models import WikiPage, Workspace


def wiki_page_get_or_create_index(
    *, workspace: Workspace, who: User
) -> WikiPage:
    """Get wiki index or create a new one."""
    validate_perm("workspace.read_wiki_page", who, workspace)
    # Assume that the first page is the index
    match WikiPage.objects.filter(
        workspace=workspace, workspace__users=who
    ).first():
        case None:
            return WikiPage.objects.create(
                workspace=workspace, title=_("Index"), content=""
            )
        case WikiPage() as page:
            return page
