"""Todo factories."""
import factory
from factory import django

from user.factory import UserFactory

from .models import TodoItemFolder, TodoItem


class TodoItemFolderFactory(django.DjangoModelFactory):
    """TodoItemFolder Factory."""

    name = factory.Faker('words')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = TodoItemFolder


class TodoItemFactory(django.DjangoModelFactory):
    """TodoItem Factory."""
    user = factory.SubFactory(UserFactory)
    folder = factory.SubFactory(TodoItemFolderFactory)
    name = factory.Faker('words')
    description = factory.Faker('text')
    done = factory.Faker('boolean')

    class Meta:
        model = TodoItem
