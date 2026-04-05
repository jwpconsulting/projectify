# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Team member view tests."""

from typing import cast

from django.core.files import File
from django.db.models.fields.files import FileDescriptor
from django.test.client import Client
from django.urls import reverse

import pytest

from projectify.workspace.models import TeamMember
from pytest_types import DjangoAssertNumQueries

pytestmark = pytest.mark.django_db


class TestTeamMemberPicture:
    """Test team_member_picture view."""

    def test_get(
        self,
        team_member: TeamMember,
        unrelated_team_member: TeamMember,
        user_client: Client,
        uploaded_file: File,
        other_uploaded_file: File,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GET."""
        # No picture
        uid = team_member.uuid
        url = reverse("dashboard:team-members:picture", args=(uid,))
        assert user_client.get(url).status_code == 404

        # Add picture
        team_member.user.profile_picture = cast(FileDescriptor, uploaded_file)
        team_member.user.save()
        with django_assert_num_queries(3):
            assert user_client.get(url).status_code == 200

        # Wrong user
        uid = unrelated_team_member.uuid
        unrelated_team_member.user.profile_picture = cast(
            FileDescriptor, other_uploaded_file
        )
        unrelated_team_member.user.save()
        url = reverse("dashboard:team-members:picture", args=(uid,))
        assert user_client.get(url).status_code == 404
