"""Test premail emails."""
import pytest

from ..emails import (
    SampleEmail,
)


@pytest.mark.django_db
class TestSampleEmail:
    """Test SampleEmail."""

    def test_send(self, user, mailoutbox):
        """Test send."""
        mail = SampleEmail(user)
        mail.send().get()
        assert len(mailoutbox) == 1
