"""Test todo queries."""
import pytest
from unittest.mock import MagicMock

from .. import schema


@pytest.fixture
def info(user):
    """Mock an info object."""
    info = MagicMock()
    info.context.user = user
    return info


@pytest.mark.django_db
class TestQuery:
    """Test Query class."""

    def test_resolve_todo_item_folders(
        self, graphql_query_user, json_loads, todo_item_folder
    ):
        """Test resolve_todo_item_folders."""
        query = """
{
    todoItemFolders(page: 1, size: 1) {
        objectList {
            name
        }
    }
}
"""
        result = json_loads(graphql_query_user(query).content)
        assert result == {
            "data": {
                "todoItemFolders": {"objectList": [{"name": todo_item_folder.name}]}
            }
        }

    def test_resolve_todo_items(self, graphql_query_user, json_loads, todo_item):
        """Test resolve_todo_items."""
        query = """
{
    todoItems(page: 1, size: 1) {
        objectList {
            name
        }
    }
}
"""
        result = json_loads(graphql_query_user(query).content)
        assert result == {
            "data": {"todoItems": {"objectList": [{"name": todo_item.name}]}}
        }
