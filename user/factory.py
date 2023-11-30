"""User app factories."""
from typing import (
    cast,
)

import factory
from factory import (
    django,
)

from . import (
    models,
)


class UserFactory(django.DjangoModelFactory[models.User]):
    """User Factory."""

    email = factory.Faker("email")
    is_superuser = False
    is_staff = False
    is_active = True
    full_name = factory.Faker("name")

    @factory.post_generation
    def password(self, created: bool, extracted: str) -> None:
        """Set the password."""
        if not created:
            return
        user = cast(models.User, self)
        user.set_password(extracted or "password")

    class Meta:
        """Meta."""

        model = models.User
        django_get_or_create = ("email",)
