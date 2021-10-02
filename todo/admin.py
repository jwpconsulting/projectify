from django.contrib import admin


from .models import (
    TodoItemFolder,
    TodoItem,
)


@admin.register(TodoItemFolder)
class TodoItemFolderAdmin(admin.ModelAdmin):
    """TodoItemFolder Admin."""


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    """TodoItem Admin."""

