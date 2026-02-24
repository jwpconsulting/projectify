# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
"""Test workspace CRUD views."""

from typing import cast
from uuid import uuid4

from django.core.files import File
from django.db.models.fields.files import FileDescriptor
from django.test.client import Client
from django.urls import reverse

import pytest

from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.user.models.user import User
from projectify.workspace.models.label import Label
from pytest_types import DjangoAssertNumQueries

from ...models.const import TeamMemberRoles
from ...models.team_member import TeamMember
from ...models.workspace import Workspace

pytestmark = pytest.mark.django_db


class TestMinimizeLists:
    """Test minimizing various lists."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:minimize-project-list",
            args=(workspace.uuid,),
        )

    @pytest.mark.parametrize(
        "initial_state,post_value,expected_state",
        [
            (False, "true", True),
            (True, "false", False),
        ],
    )
    def test_toggle_project_list(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        initial_state: bool,
        post_value: str,
        expected_state: bool,
    ) -> None:
        """Test toggling the project list minimized state via HTMX."""
        team_member.minimized_project_list = initial_state
        team_member.save()

        with django_assert_num_queries(11):
            response = user_client.post(
                resource_url, {"minimized": post_value}
            )
            assert response.status_code == 200

        team_member.refresh_from_db()
        assert team_member.minimized_project_list is expected_state

    def test_get_method_not_allowed(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_workspace_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test minimizing project list for non-existent workspace."""
        url = reverse(
            "dashboard:workspaces:minimize-project-list", args=(uuid4(),)
        )
        response = user_client.post(url, {"minimized": "true"})
        assert response.status_code == 404

    def test_invalid_form(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test form validation with invalid data."""
        response = user_client.post(resource_url, {})
        assert response.status_code == 200

    def test_unauthorized_workspace_access(
        self,
        user_client: Client,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test that users can't minimize project list for other workspaces."""
        url = reverse(
            "dashboard:workspaces:minimize-project-list",
            args=(unrelated_workspace.uuid,),
        )
        response = user_client.post(url, {"minimized": "true"})
        assert response.status_code == 404


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
        # Query count went up from 12 -> 19
        # Query count went up from 19 -> 20
        # Query count went up from 20 -> 22
        with django_assert_num_queries(22):
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
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:team-members", args=(workspace.uuid,)
        )

    def test_invite_then_uninvite(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test inviting and uninviting a new user."""
        count = team_member.workspace.teammemberinvite_set.count()
        count = team_member.workspace.teammemberinvite_set.count()
        # Justus 2025-07-29 query count went up   10 -> 19 XXX
        # Justus 2025-07-29 query count went up   19 -> 33 XXX
        # Justus 2025-07-29 query count went down 33 -> 32
        # Justus 2025-07-29 query count went up   32 -> 33 XXX
        # Query count went up 33 -> 34
        # Query count went up 34 -> 35 Justus 2026-02-23
        with django_assert_num_queries(35):
            response = user_client.post(
                resource_url, {"action": "invite", "email": "mail@bla.com"}
            )
            assert response.status_code == 200
        assert "mail@bla.com" in response.content.decode()
        assert team_member.workspace.teammemberinvite_set.count() == count + 1

        # can't invite a second time
        with django_assert_num_queries(31):
            response = user_client.post(
                resource_url, {"action": "invite", "email": "mail@bla.com"}
            )
            assert response.status_code == 400
        assert "already invited" in response.content.decode()

        with django_assert_num_queries(26):
            response = user_client.post(
                resource_url, {"action": "uninvite", "email": "mail@bla.com"}
            )
            assert response.status_code == 200
        assert "mail@bla.com" not in response.content.decode()
        assert team_member.workspace.teammemberinvite_set.count() == count

        # Can't do it a second time
        response = user_client.post(
            resource_url, {"action": "uninvite", "email": "mail@bla.com"}
        )
        assert response.status_code == 400

    def test_invite_existing_user(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_user: User,
    ) -> None:
        """Test inviting an existing user."""
        count = team_member.workspace.teammember_set.count()
        response = user_client.post(
            resource_url, {"action": "invite", "email": other_user.email}
        )
        assert response.status_code == 200
        assert team_member.workspace.teammember_set.count() == count + 1

    def test_invite_existing_team_member(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test inviting someone who is already a team member."""
        email = team_member.user.email
        response = user_client.post(
            resource_url, {"action": "invite", "email": email}
        )
        assert response.status_code == 400
        assert "already is a team member" in response.content.decode()

    def test_remove_team_member(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test removing an existing team member."""
        workspace = team_member.workspace
        initial = workspace.teammember_set.count()
        uid = str(other_team_member.uuid)
        with django_assert_num_queries(29):
            response = user_client.post(
                resource_url,
                {"action": "team_member_remove", "team_member": uid},
            )
        assert response.status_code == 200
        assert workspace.teammember_set.count() == initial - 1
        assert str(other_team_member) not in response.content.decode()

        # Can't do it a second time
        response = user_client.post(
            resource_url, {"action": "team_member_remove", "team_member": uid}
        )
        assert response.status_code == 400


class TestWorkspaceSettingsTeamMemberUpdate:
    """Test team member update view."""

    @pytest.fixture
    def resource_url(
        self, workspace: Workspace, other_team_member: TeamMember
    ) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:team-member-update",
            args=(workspace.uuid, other_team_member.uuid),
        )

    def test_get_update_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test getting the team member update form."""
        response = user_client.get(resource_url)
        assert response.status_code == 200

    def test_update_team_member_role(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating role and job title."""
        other_team_member.role = TeamMemberRoles.CONTRIBUTOR
        other_team_member.job_title = "Developer"
        other_team_member.save()

        with django_assert_num_queries(14):
            response = user_client.post(
                resource_url,
                {"role": TeamMemberRoles.MAINTAINER, "job_title": "Foo"},
            )
            assert response.status_code == 302

        other_team_member.refresh_from_db()
        assert other_team_member.role == TeamMemberRoles.MAINTAINER
        assert other_team_member.job_title == "Foo"


class TestWorkspaceSettingsLabels:
    """Test workspace labels settings view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:labels", args=(workspace.uuid,))

    def test_get_labels_list(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test getting the page."""
        assert user_client.get(resource_url).status_code == 200


class TestWorkspaceSettingsCreateLabel:
    """Test workspace create label view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:create-label", args=(workspace.uuid,)
        )

    def test_get_create_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test getting the form."""
        assert user_client.get(resource_url).status_code == 200

    def test_create_label_success(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test creating a new label."""
        initial_label_count = workspace.label_set.count()
        with django_assert_num_queries(20):
            assert (
                user_client.post(
                    resource_url, {"name": "Bug", "color": 1}
                ).status_code
                == 302
            )
        assert workspace.label_set.count() == initial_label_count + 1
        assert workspace.label_set.get(name="Bug").color == 1

    def test_create_label_invalid_form(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test form validation."""
        assert (
            user_client.post(
                resource_url, {"name": "", "color": 1}
            ).status_code
            == 400
        )

    def test_create_label_duplicate_name(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        label: Label,
    ) -> None:
        """Test creating a label with the same name as an existing one."""
        initial_label_count = workspace.label_set.count()
        assert (
            user_client.post(
                resource_url, {"name": label.name, "color": 1}
            ).status_code
            == 400
        )
        assert workspace.label_set.count() == initial_label_count


class TestWorkspaceSettingsEditLabel:
    """Test workspace edit label view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace, label: Label) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:edit-label",
            args=(workspace.uuid, label.uuid),
        )

    def test_get_edit_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test GETting the edit label form."""
        assert user_client.get(resource_url).status_code == 200

    def test_update_label_success(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        label: Label,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully updating a label."""
        with django_assert_num_queries(16):
            response = user_client.post(
                resource_url, {"name": "Updated", "color": 3}
            )
            assert response.status_code == 302
        label.refresh_from_db()
        assert label.name == "Updated"
        assert label.color == 3

    def test_update_label_invalid_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test form validation."""
        assert (
            user_client.post(
                resource_url, {"name": "", "color": 3}
            ).status_code
            == 400
        )

    def test_update_label_duplicate_name(
        self,
        user_client: Client,
        workspace: Workspace,
        team_member: TeamMember,
        label: Label,
        labels: list[Label],
    ) -> None:
        """Test updating a label to have the same name as another existing label."""
        other_label = labels[0]
        original_name = label.name
        url = reverse(
            "dashboard:workspaces:edit-label",
            args=(workspace.uuid, label.uuid),
        )
        response = user_client.post(
            url, {"name": other_label.name, "color": 3}
        )
        assert response.status_code == 400

        label.refresh_from_db()
        assert label.name == original_name  # Should not have changed

    def test_deleting(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Delete the label."""
        initial_label_count = workspace.label_set.count()
        with django_assert_num_queries(8):
            assert user_client.delete(resource_url).status_code == 200
        assert workspace.label_set.count() == initial_label_count - 1

    def test_label_not_found(
        self,
        user_client: Client,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test editing a missing label."""
        url = reverse(
            "dashboard:workspaces:edit-label",
            args=(workspace.uuid, uuid4()),
        )
        assert user_client.get(url).status_code == 404

    def test_workspace_uuid_mismatch(
        self, user_client: Client, team_member: TeamMember, label: Label
    ) -> None:
        """Test editing label with mismatched workspace UUID."""
        url = reverse(
            "dashboard:workspaces:edit-label", args=(uuid4(), label.uuid)
        )
        assert user_client.get(url).status_code == 400

    def test_unauthorized_workspace_access(
        self, user_client: Client, unrelated_label: Label
    ) -> None:
        """Test that users can't edit labels for other workspaces."""
        url = reverse(
            "dashboard:workspaces:edit-label",
            args=(unrelated_label.workspace.uuid, unrelated_label.uuid),
        )
        assert user_client.get(url).status_code == 404


class TestWorkspaceSettingsQuota:
    """Test workspace quota settings view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:quota", args=(workspace.uuid,))

    def test_get_quota_page(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test getting the quota page."""
        with django_assert_num_queries(12):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        # Only Team members and invites is in the list
        content = response.content.decode()
        # XXX Flaky HTML
        assert "<td>Team members and invites" in content
        assert "<td>Projects" not in content
        assert "<td>Sections" not in content
        assert "<td>Tasks" not in content
        assert "<td>Labels" not in content
        assert "<td>Sub tasks" not in content

    def test_get_quota_page_no_subscription(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test getting the quota page."""
        customer_cancel_subscription(customer=team_member.workspace.customer)
        with django_assert_num_queries(17):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        # These quotas should be listed
        # it's a bit tedious to test for the values since we're not giving back
        # JSON anymore
        content = response.content.decode()
        # Flaky HTML
        assert "<td>Team members and invites" in content
        assert "<td>Projects" in content
        assert "<td>Sections" in content
        assert "<td>Tasks" in content
        assert "<td>Labels" in content
        assert "<td>Sub tasks" in content
