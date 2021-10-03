from django.contrib.auth import get_user_model
from factory import django
import factory


class UserFactory(django.DjangoModelFactory):
    """User Factory."""

    email = factory.Faker("email")
    is_superuser = False
    is_staff = False

    @factory.post_generation
    def password(self, created, extracted, *args, **kwargs):
        """Set the password."""
        if not created:
            return
        self.set_password(extracted or "password")

    class Meta:
        """Meta."""

        model = "user.User"
        django_get_or_create = ("email",)


class SuperUserFactory(UserFactory):
    """Super user factory."""

    is_superuser = True
    is_staff = True
