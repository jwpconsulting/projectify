"""Test custom code views."""
from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from corporate.models.custom_code import CustomCode
from corporate.models.customer import Customer
from corporate.services.customer import customer_check_active_for_workspace
from pytest_types import DjangoAssertNumQueries
from workspace.models.workspace import Workspace


@pytest.mark.django_db
class TestCustomCodeRedeem:
    """Test redeeming custom codes."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "corporate:custom-codes:redeem-custom-code",
            args=(str(workspace.uuid),),
        )

    def test_redeeming_invalid_code(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
    ) -> None:
        """Test that nothing bad happens with an invalid code."""
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        with django_assert_num_queries(8):
            response = rest_user_client.post(
                resource_url,
                data={"code": "thiscodedoesnotexist"},
            )
            assert response.status_code == 400, response.data
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )

    def test_redeeming_valid_code(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        custom_code: CustomCode,
        workspace: Workspace,
        unpaid_customer: Customer,
    ) -> None:
        """Test that workspace subscription is actived correctly."""
        assert unpaid_customer.seats != 20
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "trial"
        )
        with django_assert_num_queries(9):
            response = rest_user_client.post(
                resource_url,
                data={"code": custom_code.code},
            )
            assert response.status_code == 204, response.data

        unpaid_customer.refresh_from_db()
        assert (
            customer_check_active_for_workspace(workspace=workspace) == "full"
        )
        # Taken from seats in conftest.py
        assert unpaid_customer.seats == 20
