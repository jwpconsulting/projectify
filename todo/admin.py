"""Todo admin."""
from django.contrib import (
    admin,
)

from .models import (
    TodoItem,
    TodoItemFolder,
)


@admin.register(TodoItemFolder)
class TodoItemFolderAdmin(admin.ModelAdmin):
    """TodoItemFolder Admin."""


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """TodoItem Admin."""
