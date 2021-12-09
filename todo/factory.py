"""Todo factories."""
import factory
from factory import (
    django,
)
from user.factory import (
    UserFactory,
)

from .models import (
    TodoItem,
    TodoItemFolder,
)


class TodoItemFolderFactory(django.DjangoModelFactory):
    """TodoItemFolder Factory."""

    name = factory.Faker("bs")
    user = factory.SubFactory(UserFactory)

    class Meta:
        """Meta."""

        model = TodoItemFolder


class TodoItemFactory(django.DjangoModelFactory):
    """TodoItem Factory."""

    user = factory.SubFactory(UserFactory)
    folder = factory.SubFactory(TodoItemFolderFactory)
    name = factory.Faker("bs")
    description = factory.Faker("text")
    done = factory.Faker("boolean")

    class Meta:
        """Meta."""

        model = TodoItem
