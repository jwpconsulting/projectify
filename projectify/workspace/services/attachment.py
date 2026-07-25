# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Attachment services."""

import logging
from pathlib import Path
from uuid import uuid4

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from projectify.lib.auth import validate_perm
from projectify.workspace.selectors.team_member import (
    team_member_find_for_workspace,
)

from ..models import Attachment, TeamMember

logger = logging.getLogger(__name__)


def attachment_create(*, who: TeamMember, file: UploadedFile) -> Attachment:
    """
    Create an attachment.

    CAVEAT: Does not perform file content validation.
    """
    validate_perm("workspace.create_attachment", who.user, who.workspace)
    attachment_name = Path(file.name)
    # helloworld.png -> XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.hellowor.png
    upload_name = (
        f"{uuid4()}.{attachment_name.name[:8]}{attachment_name.suffix}"
    )
    team_member = team_member_find_for_workspace(
        user=who.user, workspace=who.workspace
    )
    try:
        with transaction.atomic():
            attachment = Attachment.objects.create(
                name=upload_name,
                size=file.size,
                workspace=who.workspace,
                uploader=team_member,
            )
            attachment.save()

            # Putting .save() last means we roll back and not save any
            # attachment when saving this file to storage fails
            default_storage.save(str(attachment.storage_path), file)
    except Exception as e:
        e.add_note(
            f"Couldn't upload attachment with size {file.size} to "
            f"workspace {who.workspace.uuid}"
        )
        raise e
    return attachment
