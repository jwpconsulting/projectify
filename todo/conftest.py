"""Todo conftest."""
import pytest

from .factory import (
    TodoItemFactory,
    TodoItemFolderFactory,
)


@pytest.fixture
def todo_item_folder(user):
    """Create TodoItemFolder linked to user."""
    return TodoItemFolderFactory(user=user)


@pytest.fixture
def todo_item(user):
    """Create a todo item."""
    return TodoItemFactory(user=user)
