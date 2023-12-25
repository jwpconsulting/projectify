"""Test custom code services."""
from django.core.exceptions import PermissionDenied

import pytest

from corporate.services.custom_code import custom_code_create
from user.models import User

pytestmark = pytest.mark.django_db


class TestCustomCodeCreate:
    """Test custom code creation."""

    def test_authorization(self, user: User, superuser: User) -> None:
        """Test that superusers can create codes, but no regular user."""
        seats = 20
        with pytest.raises(PermissionDenied):
            custom_code_create(who=user, seats=seats)
        custom_code_create(who=superuser, seats=seats)

    def test_code_is_unique(self, superuser: User) -> None:
        """Test that codes will not collide."""
        seats = 10
        code1 = custom_code_create(who=superuser, seats=seats, prefix="asd")
        code2 = custom_code_create(who=superuser, seats=seats, prefix="asd")
        assert code1.code != code2.code
