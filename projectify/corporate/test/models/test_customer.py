# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Test corporate models."""

import pytest

from projectify.corporate.models import Customer


@pytest.mark.django_db
class TestCustomer:
    """Test customer model."""

    def test_factory(self, unpaid_customer: Customer) -> None:
        """Test factory."""
        assert unpaid_customer.workspace
