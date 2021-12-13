"""Test user emails."""
import pytest

from ..emails import (
    UserEmailConfirmationEmail,
)


@pytest.mark.django_db
class TestUserEmailConfirmationEmail:
    """Test UserEmailConfirmationEmail."""

    def test_send(self, user, mailoutbox):
        """Test send."""
        mail = UserEmailConfirmationEmail(user)
        mail.send().get()
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        assert user.get_email_confirmation_token() in m.body
