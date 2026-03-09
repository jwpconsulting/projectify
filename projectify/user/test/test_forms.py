# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test user app forms."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from ..forms import SocialAccountSignUpForm

pytestmark = pytest.mark.django_db


class TestSocialAccountSignUpForm:
    """Test SocialAccountSignUpForm."""

    @pytest.fixture(autouse=True)
    def mock_adapter(self) -> Generator[MagicMock, None, None]:
        """Mock get_adapter for all tests."""
        mock = MagicMock()
        email = "test@example.com"
        mock.get_signup_form_initial_data.return_value = {"email": email}
        with patch("projectify.user.forms.get_adapter") as get_adapter:
            get_adapter.return_value = mock
            yield mock

    def test_tos_agreed_required(self) -> None:
        """Test that form is invalid without tos_agreed."""
        mock_sociallogin = MagicMock()
        form = SocialAccountSignUpForm(
            data={"email": "test@example.com", "privacy_policy_agreed": True},
            sociallogin=mock_sociallogin,
        )
        assert not form.is_valid()
        assert "tos_agreed" in form.errors

    def test_privacy_policy_agreed_required(self) -> None:
        """Test that form is invalid without privacy_policy_agreed."""
        mock_sociallogin = MagicMock()
        form = SocialAccountSignUpForm(
            data={"email": "test@example.com", "tos_agreed": True},
            sociallogin=mock_sociallogin,
        )
        assert not form.is_valid()
        assert "privacy_policy_agreed" in form.errors

    def test_clean_email_with_matching_email(self) -> None:
        """Test clean_email when email matches initial data."""
        mock_sociallogin = MagicMock()
        form = SocialAccountSignUpForm(
            data={
                "email": "test@example.com",
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
            sociallogin=mock_sociallogin,
        )
        assert form.is_valid()

    def test_clean_email_with_no_initial_email(
        self, mock_adapter: MagicMock
    ) -> None:
        """Test clean_email when there's no initial email."""
        mock_adapter.get_signup_form_initial_data.return_value = {}
        mock_sociallogin = MagicMock()
        form = SocialAccountSignUpForm(
            data={
                "email": "test@example.com",
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
            sociallogin=mock_sociallogin,
        )
        assert form.is_valid()

    def test_clean_email_with_mismatched_email(
        self, mock_adapter: MagicMock
    ) -> None:
        """Test clean_email when email doesn't match initial data."""
        mock_adapter.get_signup_form_initial_data.return_value = {
            "email": "initial@example.com"
        }
        mock_sociallogin = MagicMock()
        form = SocialAccountSignUpForm(
            data={
                "email": "different@example.com",
                "tos_agreed": True,
                "privacy_policy_agreed": True,
            },
            sociallogin=mock_sociallogin,
        )
        assert not form.is_valid()
        assert "email" in form.errors
