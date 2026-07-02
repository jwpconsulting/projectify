# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Attachment selectors."""

from typing import Optional
from uuid import UUID

from projectify.user.models import User

from ..models import WikiPage


def wiki_find_by_workspace_and_page_title(
    *, who: User, ws_uuid: UUID, title: str
) -> Optional[WikiPage]:
    """Find wiki page by title and for user workspace."""
    return WikiPage.objects.filter(
        workspace__uuid=ws_uuid, workspace__users=who, title=title
    ).first()
