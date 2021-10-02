"""Todo Schema."""
import graphene
from graphene_django import DjangoObjectType

from todo import models

class TodoItemFolder(DjangoObjectType):
    class Meta:
        model = models.TodoItemFolder

class TodoItem(DjangoObjectType):

    class Meta:
        model = models.TodoItem


class Query():
    todo_items = graphene.List(TodoItem)
    todo_item_folders = graphene.List(TodoItemFolder)

    def resolve_todo_item_folders(self, info):
        return TodoItemFolder.objects.all()

    def resolve_todo_items(self, info):
        return TodoItem.objects.all()
