"""User app factories."""
from django.contrib.auth import (
    get_user_model,
)

import factory
from factory import (
    django,
)

from . import (
    models,
)


class UserFactory(django.DjangoModelFactory):
    """User Factory."""

    email = factory.Faker("email")
    is_superuser = False
    is_staff = False
    is_active = True
    full_name = factory.Faker("name")

    @factory.post_generation
    def password(self, created, extracted, *args, **kwargs):
        """Set the password."""
        if not created:
            return
        self.set_password(extracted or "password")

    class Meta:
        """Meta."""

        model = get_user_model()
        django_get_or_create = ("email",)


class SuperUserFactory(UserFactory):
    """Super user factory."""

    is_superuser = True
    is_staff = True
    is_active = True


class UserInviteFactory(django.DjangoModelFactory):
    """UserInvite factory."""

    email = factory.Faker("email")
    user = None

    class Meta:
        """Meta."""

        model = models.UserInvite
