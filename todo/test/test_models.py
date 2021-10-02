import pytest


@pytest.mark.django_db
class TestTodoItemFolder:
    """Test TodoItemFolder."""

    def test_factory(self, todo_item_folder, user):
        """Test factory."""
        assert todo_item_folder.user == user


@pytest.mark.django_db
class TestTodoItem:
    """Test TodoItem."""

    def test_factory(self, todo_item, user):
        """Test factory."""
        assert todo_item.user == user
