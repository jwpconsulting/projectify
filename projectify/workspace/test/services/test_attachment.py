# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test attachment services."""

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from projectify.workspace.services.attachment import attachment_create

from ...models import TeamMember

pytestmark = pytest.mark.django_db

# TODO test path traversal here
# TODO test quota here


def test_attachment_create(
    team_member: TeamMember, uploaded_file: SimpleUploadedFile
) -> None:
    """Test that the attachment_create services stores the attachment."""
    attachment = attachment_create(who=team_member, file=uploaded_file)
    assert default_storage.exists(str(attachment.storage_path))
