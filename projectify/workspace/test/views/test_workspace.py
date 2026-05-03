# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
"""Test workspace CRUD views."""

from collections.abc import Iterable
from datetime import datetime
from typing import cast
from unittest import mock
from uuid import uuid4

from django.core.files import File
from django.db.models.fields.files import FileDescriptor
from django.test.client import Client
from django.urls import reverse

import pytest

from projectify.corporate.models import Coupon, Customer
from projectify.corporate.selectors.customer import (
    customer_check_active_for_workspace,
)
from projectify.corporate.services.stripe import customer_cancel_subscription
from projectify.user.models import User
from projectify.user.services.internal import user_create
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from pytest_types import DjangoAssertNumQueries

from ...const import TeamMemberRoles
from ...models import Task, TeamMember, TeamMemberInvite, Workspace

pytestmark = pytest.mark.django_db


class MockSession:
    """Checkout and billing portal mock session."""

    url = "https://www.example.com"


class TestWorspaceSearchView:
    """Test workspace_search_view features."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:search", args=(workspace.uuid,))

    def test_get(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test GETting the search page without any query."""
        response = user_client.get(resource_url)
        assert response.status_code == 200

    def test_get_unauthorized(
        self, unrelated_user_client: Client, resource_url: str
    ) -> None:
        """Test authorization check."""
        response = unrelated_user_client.get(resource_url)
        assert response.status_code == 404

    def test_get_empty_query(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test authorization check."""
        data = {"query": ""}
        response = user_client.get(resource_url, data)
        assert response.status_code == 200
        assert b"Please enter a search query" in response.content

    def test_get_with_query(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        task: Task,
    ) -> None:
        """Test GETting the search page with a query."""
        data = {"query": task.title}
        response = user_client.get(resource_url, data)
        assert response.status_code == 200
        assert task.title in response.content.decode()

    def test_get_filter_by_team_member(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        task: Task,
        other_task: Task,
    ) -> None:
        """Test filtering by team member and check task count."""
        task.assignee = team_member
        task.save()
        other_task.assignee = other_team_member
        other_task.save()
        data = {"filter_by_team_member": [str(team_member.uuid)]}
        response = user_client.get(resource_url, data)
        assert response.status_code == 200
        assert task.title in response.content.decode()
        assert other_task.title not in response.content.decode()

    def test_get_filter_by_team_member_and_query(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        task: Task,
        other_task: Task,
    ) -> None:
        """Test filtering by team member and query together."""
        task.title = "Important bug fix"
        task.assignee = team_member
        task.save()
        other_task.title = "Feature request"
        other_task.assignee = other_team_member
        other_task.save()
        t_uid = str(team_member.uuid)
        data = {"query": "bug", "filter_by_team_member": [t_uid]}
        response = user_client.get(resource_url, data)
        assert response.status_code == 200
        assert task.title in response.content.decode()
        assert other_task.title not in response.content.decode()

    def test_get_filter_by_unassigned(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        task: Task,
        other_task: Task,
    ) -> None:
        """Test filtering for unassigned tasks."""
        task.assignee = team_member
        task.save()
        data = {"filter_by_team_member": [""]}
        response = user_client.get(resource_url, data)
        assert response.status_code == 200
        assert task.title not in response.content.decode()
        assert other_task.title in response.content.decode()


class TestWorkspacePictureView:
    """Test workspace_picture_view function."""

    def test_authorized_access(
        self,
        user_client: Client,
        team_member: TeamMember,
        uploaded_file: File,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test that authorized team members can access workspace picture."""
        workspace = team_member.workspace
        workspace.picture = cast(FileDescriptor, uploaded_file)
        workspace.save()
        url = reverse("dashboard:workspaces:picture", args=(workspace.uuid,))
        with django_assert_num_queries(3):
            assert user_client.get(url).status_code == 200

    def test_unauthorized_access(
        self,
        user_client: Client,
        unrelated_workspace: Workspace,
        uploaded_file: File,
    ) -> None:
        """Test that non-team members cannot access workspace picture."""
        unrelated_workspace.picture = cast(FileDescriptor, uploaded_file)
        unrelated_workspace.save()
        url = reverse(
            "dashboard:workspaces:picture", args=(unrelated_workspace.uuid,)
        )
        assert user_client.get(url).status_code == 404


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
        [(False, "true", True), (True, "false", False)],
    )
    def test_toggle_project_list(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_max_num_queries: DjangoAssertNumQueries,
        initial_state: bool,
        post_value: str,
        expected_state: bool,
    ) -> None:
        """Test toggling the project list minimized state via HTMX."""
        team_member.minimized_project_list = initial_state
        team_member.save()

        # Gone up from 11 -> 13 due to permission checks in sidemenu
        # XX non-deterministic test
        with django_assert_max_num_queries(13):
            response = user_client.post(
                resource_url, {"project_list_minimized": post_value}
            )
            assert response.status_code == 200

        team_member.refresh_from_db()
        assert team_member.minimized_project_list is expected_state

    def test_get_method_not_allowed(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_workspace_not_found(
        self, user_client: Client, team_member: TeamMember
    ) -> None:
        """Test minimizing project list for non-existent workspace."""
        url = reverse(
            "dashboard:workspaces:minimize-project-list", args=(uuid4(),)
        )
        response = user_client.post(url, {"minimized": "true"})
        assert response.status_code == 404

    def test_invalid_form(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test form validation with invalid data."""
        response = user_client.post(resource_url, {})
        assert response.status_code == 200

    def test_unauthorized_workspace_access(
        self, user_client: Client, unrelated_workspace: Workspace
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
        # Query count went up   from 12 -> 19
        # Query count went up   from 19 -> 20
        # Query count went up   from 20 -> 22
        # Query count went up   from 22 -> 24 due to permission checks in sidemenu
        # Query count went up   from 24 -> 25
        # Query count went down from 25 -> 24
        # Query count went down from 24 -> 22
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
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test inviting and uninviting a new user."""
        count = team_member.workspace.teammemberinvite_set.count()
        response = user_client.post(
            resource_url, {"action": "invite", "email": "mail@bla.com"}
        )
        assert response.status_code == 200
        assert "mail@bla.com" in response.content.decode()
        assert team_member.workspace.teammemberinvite_set.count() == count + 1

        # can't invite a second time
        response = user_client.post(
            resource_url, {"action": "invite", "email": "mail@bla.com"}
        )
        assert response.status_code == 400

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
        data = {"action": "team_member_remove", "team_member": uid}
        # Gone down from 28 -> 25
        # Gone down from 25 -> 23
        # Gone down from 23 -> 22
        with django_assert_num_queries(22):
            response = user_client.post(resource_url, data)
        assert response.status_code == 200
        assert workspace.teammember_set.count() == initial - 1
        assert str(other_team_member) not in response.content.decode()

        # Can't do it a second time
        response = user_client.post(
            resource_url, {"action": "team_member_remove", "team_member": uid}
        )
        assert response.status_code == 400

    def test_redeemed_stale_invites(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        team_member_invite: TeamMemberInvite,
        now: datetime,
    ) -> None:
        """
        Assert that stale (redeemed) invites don't show up.

        Test setup:
        - User A: the user_client user, owns the workspace
        - User B: User A invites them, they join.
        - User C: User A invites them and uninvites them.
        """
        user_b_email = "foobar@localhost"
        user_c_email = team_member_invite.user_invite.email
        workspace = team_member.workspace
        user_b_member_invite = team_member_invite_create(
            workspace=workspace,
            who=team_member.user,
            email_or_user=user_b_email,
        )
        assert isinstance(user_b_member_invite, TeamMemberInvite)
        user_c_user_invite = team_member_invite.user_invite

        response = user_client.get(resource_url)
        assert response.status_code == 200
        assert "foobar@localhost" in response.content.decode()
        assert "Foo Bar" not in response.content.decode()
        assert user_c_email in response.content.decode()

        assert TeamMemberInvite.objects.count() == 2
        assert TeamMemberInvite.objects.filter(redeemed=True).count() == 0

        # Redeem user_invite_b by signing up user_b
        user_b = user_create(
            email=user_b_email, tos_agreed=now, privacy_policy_agreed=now
        )
        user_b.preferred_name = "Foo Bar"
        user_b.save()
        assert TeamMemberInvite.objects.count() == 2
        assert TeamMemberInvite.objects.filter(redeemed=True).count() == 1

        response = user_client.get(resource_url)
        assert response.status_code == 200
        # Redeemed, so it won't show up, neither in
        # members, nor invite table, since we've set a preferred name
        assert "foobar@localhost" not in response.content.decode()
        # User B's preferred name shows up
        assert "Foo Bar" in response.content.decode()
        # This should show up
        assert user_c_email in response.content.decode()

        # Uninvite user C
        data = {"action": "uninvite", "email": user_c_user_invite.email}
        response = user_client.post(resource_url, data=data)
        assert response.status_code == 200
        assert TeamMemberInvite.objects.count() == 1
        assert TeamMemberInvite.objects.filter(redeemed=True).count() == 1

        # User B's email shouldn't show up, but their preferred name should
        assert "foobar@localhost" not in response.content.decode()
        assert "Foo Bar" in response.content.decode()
        # User C's invite is also gone, since we uninvite them
        assert user_c_email not in response.content.decode()


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

        with django_assert_num_queries(13):
            response = user_client.post(
                resource_url,
                {"role": TeamMemberRoles.MAINTAINER, "job_title": "Foo"},
            )
            assert response.status_code == 302

        other_team_member.refresh_from_db()
        assert other_team_member.role == TeamMemberRoles.MAINTAINER
        assert other_team_member.job_title == "Foo"


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
        # Gone up from 12 -> 13 due to permission checks in sidemenu
        # Gone down from 13 -> 12
        with django_assert_num_queries(12):
            response = user_client.get(resource_url)
            assert response.status_code == 200

        content = response.content.decode()
        # XXX Flaky HTML
        assert "<td>Team members and invites" in content
        assert "<td>Projects" not in content
        assert "<td>Tasks" not in content

    def test_get_quota_page_no_subscription(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test getting the quota page."""
        customer_cancel_subscription(customer=team_member.workspace.customer)
        # Gone up from 16 -> 17 due to permission checks in sidemenu
        # Gone down from 17 -> 15
        # Gone down from 15 -> 13
        with django_assert_num_queries(13):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        # These quotas should be listed
        # it's a bit tedious to test for the values since we're not giving back
        # JSON anymore
        content = response.content.decode()
        # Flaky HTML
        assert "<td>Team members and invites" in content
        assert "<td>Projects" in content
        assert "<td>Tasks" in content


class TestWorkspaceSettingsBilling:
    """Test workspace_settings_billing view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:billing", args=(workspace.uuid,))

    @pytest.fixture(autouse=True)
    def mock_stripe_billing_portal(self) -> Iterable[mock.MagicMock]:
        """Mock stripe billing portal session creation."""
        with mock.patch(
            "stripe.billing_portal._session_service.SessionService.create"
        ) as m:
            m.return_value = MockSession()
            yield m

    @pytest.fixture(autouse=True)
    def mock_stripe_checkout(self) -> Iterable[mock.MagicMock]:
        """Mock stripe checkout session creation."""
        with mock.patch(
            "stripe.checkout._session_service.SessionService.create"
        ) as m:
            m.return_value = MockSession()
            yield m

    def test_with_unpaid_customer(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Assert that an unpaid customer can't edit their billing settings."""
        data = {"action": "checkout", "seats": 5}
        with django_assert_num_queries(16):
            response = user_client.post(resource_url, data=data)
            assert response.status_code == 302
        assert response.headers["Location"] == "https://www.example.com"

    def test_with_paying_customer_billing_edit(
        self,
        user_client: Client,
        # paid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test that you can't go checkout as a paying customer."""
        response = user_client.post(
            resource_url, {"action": "checkout", "seats": 5}
        )
        assert response.status_code == 400
        content = response.content.decode()
        assert "already activated a subscription" in content

    def test_wrong_workspace(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        team_member: TeamMember,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test passing in an invalid uuid."""
        resource_url = reverse(
            "dashboard:workspaces:billing",
            args=(str(unrelated_workspace.uuid),),
        )
        data = {"action": "checkout", "seats": "99"}
        with django_assert_num_queries(3):
            response = user_client.post(resource_url, data=data)
            assert response.status_code == 404

    def test_posting_normal_data(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test we can get a redirect when posting valid checkout data."""
        data = {"action": "checkout", "seats": "99"}
        with django_assert_num_queries(16):
            response = user_client.post(resource_url, data=data)
            assert response.status_code == 302, response.content.decode()
        assert response.headers["Location"] == "https://www.example.com"

    def test_paid_customer(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        paid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test that there is an error on paid customer for checkout."""
        data = {"action": "checkout", "seats": 100}
        response = user_client.post(resource_url, data=data)
        assert response.status_code == 400
        assert b"already activated a subscription" in response.content

    def test_checkout_missing_seats(
        self,
        user_client: Client,
        unpaid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test checkout action with missing seats."""
        response = user_client.post(resource_url, {"action": "checkout"})
        assert response.status_code == 400, response.content
        assert b"This field is required" in response.content

    def test_checkout_invalid_seats(
        self,
        user_client: Client,
        unpaid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test checkout action with invalid seats."""
        data = {"action": "checkout", "seats": 0}
        response = user_client.post(resource_url, data)
        assert response.status_code == 400, response.content
        assert b"greater than or equal to 1" in response.content

    def test_get_with_unpaid_customer(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        unpaid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test GET request with unpaid customer shows billing form."""
        # Gone up from 16 -> 17 due to permission checks in sidemenu
        # Gone down from 17 -> 15
        # Gone down from 15 -> 13
        with django_assert_num_queries(13):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert b"Use a coupon code" in response.content

    def test_get_with_paying_customer(
        self,
        user_client: Client,
        django_assert_num_queries: DjangoAssertNumQueries,
        paid_customer: Customer,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test GET request with paying customer shows billing info."""
        # Gone up from 12 -> 13 due to permission checks in sidemenu
        # Gone down from 13 -> 12
        with django_assert_num_queries(12):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert b"You have a paid workspace" in response.content


class TestWorkspaceSettingsBillingCoupon:
    """Test coupon redemption in workspace billing settings."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("dashboard:workspaces:billing", args=(workspace.uuid,))

    def test_redeeming_invalid_code(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        unpaid_customer: Customer,
    ) -> None:
        """Test that nothing bad happens with an invalid coupon code."""
        active = customer_check_active_for_workspace(workspace=workspace)
        assert active == "trial"
        data = {"action": "redeem_coupon", "code": "foo"}
        # Gone up from 21 -> 22 due to permission checks in sidemenu
        # Gone up   from 22 -> 23
        # Gone down from 23 -> 19
        # Gone down from 19 -> 18
        # Gone down from 18 -> 17
        with django_assert_num_queries(17):
            res = user_client.post(resource_url, data=data)
            assert res.status_code == 400
        assert "No coupon is available for this code" in res.content.decode()
        unpaid_customer.refresh_from_db()
        active = customer_check_active_for_workspace(workspace=workspace)
        assert active == "trial"

    def test_redeeming_valid_code(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        coupon: Coupon,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        unpaid_customer: Customer,
    ) -> None:
        """Test that workspace subscription is activated correctly."""
        assert unpaid_customer.seats != 20
        active = customer_check_active_for_workspace(workspace=workspace)
        assert active == "trial"
        data = {"action": "redeem_coupon", "code": coupon.code}
        with django_assert_num_queries(17):
            response = user_client.post(resource_url, data=data)
            assert response.status_code == 302

        unpaid_customer.refresh_from_db()
        active = customer_check_active_for_workspace(workspace=workspace)
        assert active == "full"
        # Should be 20
        assert unpaid_customer.seats == coupon.seats
