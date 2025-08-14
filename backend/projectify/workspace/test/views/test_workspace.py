# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
"""Test workspace CRUD views."""

import unittest.mock
from typing import cast

from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.core.files import File
from django.db.models.fields.files import FileDescriptor
from django.test.client import Client
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.user.models.user import User
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from pytest_types import DjangoAssertNumQueries, Headers

from ...models.const import TeamMemberRoles
from ...models.project import Project
from ...models.team_member import TeamMember
from ...models.workspace import Workspace

pytestmark = pytest.mark.django_db


# Django view tests


class TestWorkspaceSettings:
    """Test django workspace settings view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:settings", args=(workspace.uuid,))

    def test_get_form(
        self,
        user: User,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test GETting the page."""
        response = user_client.get(resource_url)
        assert response.status_code == 200
        assert workspace.title.encode() in response.content

    def test_update_workspace_and_title(
        self,
        user_client: Client,
        resource_url: str,
        uploaded_file: File,
        workspace: Workspace,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating both title and workspace picture."""
        workspace.picture = cast(FileDescriptor, None)
        workspace.save()
        assert not workspace.picture
        with django_assert_num_queries(12):
            response = user_client.post(
                resource_url,
                {
                    "title": "New Workspace Title",
                    "description": "New workspace description",
                    "picture": uploaded_file,
                },
                follow=True,
            )
            assert response.status_code == 200
            assert response.redirect_chain[-1][0] == reverse(
                "dashboard:workspaces:settings", args=(workspace.uuid,)
            )

        workspace.refresh_from_db()
        assert workspace.title == "New Workspace Title"
        assert workspace.description == "New workspace description"
        assert workspace.picture.url

    def test_clear_workspace_picture(
        self,
        user_client: Client,
        resource_url: str,
        uploaded_file: File,
        workspace: Workspace,
    ) -> None:
        """Test clearing the workspace picture."""
        workspace.picture = cast(FileDescriptor, uploaded_file)
        workspace.save()
        assert workspace.picture

        response = user_client.post(
            resource_url,
            {
                "title": workspace.title,
                "description": workspace.description,
                "picture-clear": "1",
            },
            follow=True,
        )
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse(
            "dashboard:workspaces:settings", args=(workspace.uuid,)
        )

        workspace.refresh_from_db()
        assert not workspace.picture


class TestWorkspaceSettingsTeamMembers:
    """Test team member invite view."""

    @pytest.fixture
    def invite_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:team-members-invite", args=(workspace.uuid,)
        )

    def test_invite_new_user(
        self,
        user_client: Client,
        invite_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test inviting a new user."""
        initial_invite_count = workspace.teammemberinvite_set.count()

        # Justus 2025-07-29 query count went up 10 -> 19 XXX
        # Justus 2025-07-29 query count went up 19 -> 33 XXX
        with django_assert_num_queries(33):
            response = user_client.post(
                invite_url, {"email": "newuser@example.com"}
            )
            assert response.status_code == 200

        assert (
            workspace.teammemberinvite_set.count() == initial_invite_count + 1
        )

    def test_invite_existing_user(
        self,
        user_client: Client,
        invite_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        other_user: User,
    ) -> None:
        """Test inviting an existing user."""
        initial_team_member_count = workspace.teammember_set.count()

        response = user_client.post(invite_url, {"email": other_user.email})

        assert response.status_code == 200
        assert (
            workspace.teammember_set.count() == initial_team_member_count + 1
        )

    def test_invite_already_invited_user(
        self, user_client: Client, invite_url: str, team_member: TeamMember
    ) -> None:
        """Test inviting a user who was already invited."""
        user_client.post(invite_url, {"email": "duplicate@example.com"})

        response = user_client.post(
            invite_url, {"email": "duplicate@example.com"}
        )
        assert response.status_code == 400
        assert b"already been invited" in response.content

    def test_invite_existing_team_member(
        self, user_client: Client, invite_url: str, team_member: TeamMember
    ) -> None:
        """Test inviting someone who is already a team member."""
        response = user_client.post(
            invite_url, {"email": team_member.user.email}
        )
        assert response.status_code == 400
        assert b"already been added" in response.content


# Create
class TestWorkspaceCreate:
    """Test workspace create."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:workspaces:create")

    def test_create(
        self,
        user: User,
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
        team_member = workspace.teammember_set.get()
        assert team_member.user == user
        assert team_member.role == TeamMemberRoles.OWNER

    def test_create_empty_description(
        self, rest_user_client: APIClient, resource_url: str
    ) -> None:
        """Test that we can submit with an empty description."""
        response = rest_user_client.post(resource_url, {"title": "blabla"})
        assert response.status_code == 201


# Read
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
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == [
            {
                "title": workspace.title,
                "uuid": str(workspace.uuid),
            },
        ]


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
        team_member: TeamMember,
        project: Project,
        archived_project: Project,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        # Make sure we have an unredeemed invite
        team_member_invite_create(
            email_or_user="rando@calrissian.org",
            who=team_member.user,
            workspace=workspace,
        )
        # Went up from 5 to 7, since we now return the quota for remaining
        # seats
        # One more for user invites
        with django_assert_num_queries(8):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {
            "title": workspace.title,
            "description": workspace.description,
            "uuid": str(workspace.uuid),
            "picture": None,
            "team_members": [
                unittest.mock.ANY,
                unittest.mock.ANY,
            ],
            "team_member_invites": [
                {"email": "rando@calrissian.org", "created": unittest.mock.ANY}
            ],
            "projects": [
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
                "projects": unittest.mock.ANY,
                "sections": unittest.mock.ANY,
                "team_members_and_invites": {
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
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert that trial limits are annotated correctly."""
        customer_cancel_subscription(customer=workspace.customer)
        with django_assert_num_queries(13):
            response = rest_user_client.get(resource_url)
        assert response.status_code == 200, response.data
        assert response.data == {
            "title": workspace.title,
            "description": workspace.description,
            "uuid": str(workspace.uuid),
            "picture": None,
            "team_members": [
                {
                    "user": {
                        "email": team_member.user.email,
                        "preferred_name": team_member.user.preferred_name,
                        "profile_picture": None,
                    },
                    "uuid": str(team_member.uuid),
                    "job_title": team_member.job_title,
                    "role": "OWNER",
                }
            ],
            "team_member_invites": [],
            "projects": [],
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
                "projects": {
                    "current": 0,
                    "limit": 10,
                    "can_create_more": True,
                },
                "sections": {
                    "current": 0,
                    "limit": 100,
                    "can_create_more": True,
                },
                "team_members_and_invites": {
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
        team_member: TeamMember,
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
        team_member: TeamMember,
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


class TestInviteUserToWorkspace:
    """Test two views, InviteUserToWorkspace and UninviteUserFromWorkspace."""

    @pytest.fixture
    def resource_url(self, team_member: TeamMember) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:invite-team-member",
            # Using the team_member fixture, we create a ws user and ws in
            # one go! Mighty clever I dare say >:)
            args=(team_member.workspace.uuid,),
        )

    @pytest.fixture
    def uninvite_url(self, team_member: TeamMember) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:uninvite-team-member",
            args=(team_member.workspace.uuid,),
        )

    def test_new_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace: Workspace,
        uninvite_url: str,
    ) -> None:
        """Test with a new, unregistered user."""
        count = workspace.teammemberinvite_set.count()
        response = rest_user_client.post(
            resource_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 201, response.data
        assert workspace.teammemberinvite_set.count() == count + 1

        # Then uninvite them
        response = rest_user_client.post(
            uninvite_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 204, response.data
        assert workspace.teammemberinvite_set.count() == count

        # Can't uninvite twice
        response = rest_user_client.post(
            uninvite_url, {"email": "taro@yamamoto.jp"}
        )
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"email": "User with this email was never invited"},
            "general": None,
        }
        assert workspace.teammemberinvite_set.count() == count

    def test_existing_user(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        workspace: Workspace,
        other_user: AbstractUser,
    ) -> None:
        """Test by inviting an existing user."""
        assert workspace.teammemberinvite_set.count() == 0
        response = rest_user_client.post(
            resource_url, {"email": other_user.email}
        )
        assert response.status_code == 201, response.data
        assert workspace.teammemberinvite_set.count() == 0

    def test_existing_team_member(
        self,
        resource_url: str,
        rest_user_client: APIClient,
        team_member: TeamMember,
    ) -> None:
        """Test inviting an existing team member."""
        response = rest_user_client.post(
            resource_url, {"email": team_member.user.email}
        )
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {
                "email": f"User with email {team_member.user.email} has "
                "already been added to this workspace."
            },
            "general": None,
        }

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
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {
                "email": "User with email hello@example.com has already been "
                "invited to this workspace."
            },
            "general": None,
        }

    def test_uninvite_non_existing(
        self, uninvite_url: str, rest_user_client: APIClient
    ) -> None:
        """Assert nothing weird happens when uninviting an invalid email."""
        response = rest_user_client.post(
            uninvite_url, {"email": "hello@example.com"}
        )
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"email": "User with this email was never invited"},
            "general": None,
        }

    def test_uninvite_existing_user(
        self,
        uninvite_url: str,
        rest_user_client: APIClient,
        team_member: TeamMember,
    ) -> None:
        """Assert nothing weird happens when uninviting an existing user."""
        response = rest_user_client.post(
            uninvite_url, {"email": team_member.user.email}
        )
        assert response.status_code == 400, response.data
        assert response.data == {
            "status": "invalid",
            "code": 400,
            "details": {"email": "User with this email was never invited"},
            "general": None,
        }
