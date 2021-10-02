"""Seeddb command."""
import tqdm
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from user.factory import SuperUserFactory, UserFactory
from todo.factory import TodoItemFactory, TodoItemFolderFactory


class Command(BaseCommand):
    """Command."""

    USERS = 5

    def create_users(self):
        """Create users."""
        super_user = SuperUserFactory(
            email='admin@localhost',
            password='password',
        )
        guest_user = UserFactory(
            email='guest@localhost',
            password='password',
        )

        users = super_user, guest_user

        return users

    FOLDERS = 5
    TODOS_PER_FOLDER = 5

    def create_todos(self, users):
        """Create todo item folders and todo items."""
        for user in tqdm.tqdm(users, desc='Todo Item Folders'):
            count = user.todoitemfolder_set.count()
            TodoItemFolderFactory.create_batch(
                self.FOLDERS - count,
                user=user,
            )
            folders = user.todoitemfolder_set.all()
            for folder in tqdm.tqdm(folders, desc='Todo Items'):
                count = folder.todoitem_set.count()
                TodoItemFactory.create_batch(
                    self.TODOS_PER_FOLDER - count,
                    user=user,
                    folder=folder,
                )

    @transaction.atomic
    def handle(self, *args, **options):
        """Handle."""
        users = self.create_users()
        self.create_todos(users)
