# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Attachment selectors."""

from typing import Optional
from uuid import UUID

from projectify.user.models import User

from ..models import Attachment


def attachment_find_by_workspace_uuid_and_name(
    *, who: User, workspace_uuid: UUID, name: str
) -> Optional[Attachment]:
    """Find attachment for user and workspace."""
    return Attachment.objects.filter(
        workspace__uuid=workspace_uuid, workspace__users=who, name=name
    ).first()
