"""Todo Schema."""
import graphene
from graphene_django import DjangoObjectType

from todo import models


class TodoItemFolder(DjangoObjectType):
    """TodoItemFolder."""

    class Meta:
        """Meta."""

        model = models.TodoItemFolder


class TodoItem(DjangoObjectType):
    """TodoItem."""

    class Meta:
        """Meta."""

        model = models.TodoItem


class Query():
    """Query object."""

    todo_items = graphene.List(TodoItem)
    todo_item_folders = graphene.List(TodoItemFolder)

    def resolve_todo_item_folders(self, info):
        return models.TodoItemFolder.objects.all()

    def resolve_todo_items(self, info):
        return models.TodoItem.objects.all()
