# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023, 2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Test workspace CRUD views."""
import unittest.mock

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
)
from django.core.files import (
    File,
)
from django.urls import (
    reverse,
)

import pytest
from rest_framework import status
from rest_framework.test import (
    APIClient,
)

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.workspace.services.workspace_user_invite import (
    workspace_user_invite_create,
)
from pytest_types import (
    DjangoAssertNumQueries,
    Headers,
)

from ...models.const import WorkspaceUserRoles
from ...models.workspace import Workspace
from ...models.workspace_board import WorkspaceBoard
from ...models.workspace_user import WorkspaceUser


# Create
@pytest.mark.django_db
class TestWorkspaceCreate:
    """Test workspace create."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspaces:create")

    def test_create(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert that we can create a new workspace."""
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New workspace, who dis?",
                    "description": "Synergize vertical integration in Q4",
                },
            )
            assert response.status_code == 201
        assert Workspace.objects.count() == 1
        workspace = Workspace.objects.get()
        workspace_user = workspace.workspaceuser_set.get()
        assert workspace_user.user == user
        assert workspace_user.role == WorkspaceUserRoles.OWNER

        # Test also that we can submit with empty description
        response = rest_user_client.post(resource_url, {"title": "blabla"})
        assert response.status_code == 201


# Read
@pytest.mark.django_db
class TestUserWorkspaces:
    """Test Workspace list."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspaces:user-workspaces")

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == [
            {
                "created": unittest.mock.ANY,
                "description": workspace.description,
                "modified": unittest.mock.ANY,
                "picture": None,
                "title": workspace.title,
                "uuid": str(workspace.uuid),
            },
        ]


@pytest.mark.django_db
class TestWorkspaceReadUpdate:
    """Test WorkspaceReadUpdate."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:read-update", args=(workspace.uuid,)
        )

    def test_get(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        workspace_board: WorkspaceBoard,
        archived_workspace_board: WorkspaceBoard,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        # Make sure we have an unredeemed invite
        workspace_user_invite_create(
            email_or_user="rando@calrissian.org",
            who=workspace_user.user,
            workspace=workspace,
        )
        # Went up from 5 to 7, since we now return the quota for remaining
        # seats
        # One more for user invites
        with django_assert_num_queries(8):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {
            "created": unittest.mock.ANY,
            "modified": unittest.mock.ANY,
            "title": workspace.title,
            "description": workspace.description,
            "uuid": str(workspace.uuid),
            "picture": None,
            "workspace_users": [
                unittest.mock.ANY,
                unittest.mock.ANY,
            ],
            "workspace_user_invites": [
                {"email": "rando@calrissian.org", "created": unittest.mock.ANY}
            ],
            "workspace_boards": [
                unittest.mock.ANY,
            ],
            "labels": [],
            # TODO
            "quota": {
                "workspace_status": "full",
                "chat_messages": unittest.mock.ANY,
                "labels": unittest.mock.ANY,
                "sub_tasks": unittest.mock.ANY,
                "tasks": unittest.mock.ANY,
                "task_labels": unittest.mock.ANY,
                "workspace_boards": unittest.mock.ANY,
                "sections": unittest.mock.ANY,
                "workspace_users_and_invites": {
                    "current": 3,
                    "limit": 10,
                    "can_create_more": True,
                },
            },
        }

    def test_get_trial(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert that trial limits are annotated correctly."""
        customer_cancel_subscription(customer=workspace.customer)
        with django_assert_num_queries(13):
            response = rest_user_client.get(resource_url)
        assert response.status_code == 200, response.data
        assert response.data == {
            "created": unittest.mock.ANY,
            "modified": unittest.mock.ANY,
            "title": workspace.title,
            "description": workspace.description,
            "uuid": str(workspace.uuid),
            "picture": None,
            "workspace_users": [
                {
                    # Thx internet
                    # https://stackoverflow.com/questions/18064610/ignoring-an-element-from-a-dict-when-asserting-in-pytest/37680581#37680581
                    "created": unittest.mock.ANY,
                    "modified": unittest.mock.ANY,
                    "user": {
                        "email": workspace_user.user.email,
                        "preferred_name": workspace_user.user.preferred_name,
                        "profile_picture": None,
                    },
                    "uuid": str(workspace_user.uuid),
                    "role": "OWNER",
                    "job_title": None,
                }
            ],
            "workspace_user_invites": [],
            "workspace_boards": [],
            "labels": [],
            "quota": {
                "workspace_status": "trial",
                "chat_messages": {
                    "current": 0,
                    "limit": 0,
                    "can_create_more": False,
                },
                "labels": {"current": 0, "limit": 10, "can_create_more": True},
                "sub_tasks": {
                    "current": 0,
                    "limit": 1000,
                    "can_create_more": True,
                },
                "tasks": {
                    "current": 0,
                    "limit": 1000,
                    "can_create_more": True,
                },
                "task_labels": {
                    "current": None,
                    "limit": None,
                    "can_create_more": True,
                },
                "workspace_boards": {
                    "current": 0,
                    "limit": 10,
                    "can_create_more": True,
                },
                "sections": {
                    "current": 0,
                    "limit": 100,
                    "can_create_more": True,
                },
                "workspace_users_and_invites": {
                    "current": 1,
                    "limit": 2,
                    "can_create_more": True,
                },
            },
        }

    def test_updating(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a given workspace with a new title."""
        with django_assert_num_queries(7):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "New title",
                },
            )
        assert response.status_code == status.HTTP_200_OK, response.data
        workspace.refresh_from_db()
        assert workspace.title == "New title"


# Delete


# RPC
@pytest.mark.django_db
class TestWorkspacePictureUploadView:
    """Test WorkspacePictureUploadView."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:upload-picture", args=(workspace.uuid,)
        )

    @pytest.fixture
    def headers(self, png_image: File) -> Headers:
        """Return headers."""
        return {
            "HTTP_CONTENT_DISPOSITION": "attachment; filename=test.png",
            "HTTP_CONTENT_LENGTH": len(png_image),
        }

    def test_unauthenticated(
        self,
        rest_client: APIClient,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
    ) -> None:
        """Assert we can't view this while being logged out."""
        response = rest_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 403, response.data

    def test_upload_then_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        headers: Headers,
        uploaded_file: File,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Try uploading and then deleting a picture."""
        response = rest_user_client.post(
            resource_url,
            {"file": uploaded_file},
            format="multipart",
            **headers,
        )
        assert response.status_code == 204, response.data
        workspace.refresh_from_db()
        assert workspace.picture

        response = rest_user_client.post(resource_url)
        assert response.status_code == 204, response.data
        workspace.refresh_from_db()
        assert not workspace.picture


@pytest.mark.django_db
class TestInviteUserToWorkspace:
    """Test two views, InviteUserToWorkspace and UninviteUserFromWorkspace."""

    @pytest.fixture
    def resource_url(self, workspace_user: WorkspaceUser) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:invite-workspace-user",
            # Using the workspace_user fixture, we create a ws user and ws in
            # one go! Mighty clever I dare say >:)
            args=(workspace_user.workspace.uuid,),
        )

    @pytest.fixture
    def uninvite_url(self, workspace_user: WorkspaceUser) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:uninvite-workspace-user",
            args=(workspace_user.workspace.uuid,),
        )

    def test_new_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace: Workspace,
        uninvite_url: str,
    ) -> None:
        """Test with a new, unregistered user."""
        assert workspace.workspaceuserinvite_set.count() == 0
        response = rest_user_client.post(
            resource_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 201, response.data
        assert workspace.workspaceuserinvite_set.count() == 1

        # Then uninvite them
        response = rest_user_client.post(
            uninvite_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 204, response.data
        assert workspace.workspaceuserinvite_set.count() == 0

        # Can't uninvite twice
        response = rest_user_client.post(
            uninvite_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 400, response.data
        assert workspace.workspaceuserinvite_set.count() == 0

    def test_existing_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace: Workspace,
        other_user: AbstractUser,
    ) -> None:
        """Test by inviting an existing user."""
        assert workspace.workspaceuserinvite_set.count() == 0
        response = rest_user_client.post(
            resource_url, {"email": other_user.email}
        )
        assert response.status_code == 201, response.data
        assert workspace.workspaceuserinvite_set.count() == 0

    def test_existing_workspace_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test inviting an existing workspace user."""
        response = rest_user_client.post(
            resource_url, {"email": workspace_user.user.email}
        )
        assert response.status_code == 400, response.data
        assert "already been added" in response.data["email"], response.data

    def test_existing_invitation(
        self, resource_url: str, rest_user_client: APIClient
    ) -> None:
        """Test inviting someone twice."""
        response = rest_user_client.post(
            resource_url, {"email": "hello@example.com"}
        )
        assert response.status_code == 201, response.data
        response = rest_user_client.post(
            resource_url, {"email": "hello@example.com"}
        )
        assert response.status_code == 400, response.data
        assert "already been invited" in response.data["email"], response.data

    def test_uninvite_non_existing(
        self, uninvite_url: str, rest_user_client: APIClient
    ) -> None:
        """Assert nothing weird happens when uninviting an invalid email."""
        response = rest_user_client.post(
            uninvite_url, {"email": "hello@example.com"}
        )
        assert response.status_code == 400, response.data

    def test_uninvite_existing_user(
        self,
        uninvite_url: str,
        rest_user_client: APIClient,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Assert nothing weird happens when uninviting an invalid email."""
        response = rest_user_client.post(
            uninvite_url, {"email": workspace_user.user.email}
        )
        assert response.status_code == 400, response.data
