# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""
Seeddb command.

The various --n-* arguments can be used to ensure that the database contains at
least N of each object.

For workspaces that already exist, we don't touch them.

For new workspaces, we add quantities of objects, as specified in the arguments

Assuming that you've configured Projectify to use SQLite, you can
re-create the database with the following shell command:

rm projectify.sqlite; uv run ./manage.py seeddb
"""

from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import timezone
from itertools import groupby
from pathlib import Path
from random import choice, randint, sample
from typing import Any, cast

from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields.files import FileDescriptor
from django.utils.text import slugify

# Faker only exist when you install the uv dependency group "demo" or "dev"
try:
    from faker import Faker
except ImportError as e:
    raise RuntimeError(
        "Could not import faker.\n"
        "Are you running seeddb in the correct environment?"
    ) from e

from projectify.blog.models import Post, PostContent
from projectify.corporate.models import Customer
from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.user.models import User
from projectify.user.services.internal import (
    user_create,
    user_create_superuser,
)
from projectify.workspace.const import TeamMemberRoles
from projectify.workspace.models import Project, Task, TeamMember, Workspace


@dataclass
class WorkspaceDescription:
    """Describes a workspace and its related objects."""

    workspace: Workspace
    team_members: list[TeamMember]
    projects: list[Project]


WORKSPACE_TITLE_MIN_LENGTH = 20
WORKSPACE_TITLE_MAX_LENGTH = 200

PROJECT_TITLE_MIN_LENGTH = 20
PROJECT_TITLE_MAX_LENGTH = 100

TASK_TITLE_MIN_LENGTH = 40
TASK_TITLE_MAX_LENGTH = 250
TASK_DESCRIPTION_SENTENCES = 10

POST_CONTENT_MIN_PARAGRAPHS = 5
POST_CONTENT_MAX_PARAGRAPHS = 15

USER_AVATARS = [
    Path("projectify/test/test-images/cat1.jpg"),
    Path("projectify/test/test-images/cat2.jpg"),
    Path("projectify/test/test-images/cat3.jpg"),
    Path("projectify/test/test-images/cat4.jpg"),
]


class Command(BaseCommand):
    """Command."""

    fake: Faker
    n_users: int
    n_workspaces: int
    n_projects: int
    n_tasks: int
    n_add_users: int
    n_posts: int

    def create_users(self) -> list["User"]:
        """Create users."""
        existing_users = User.objects.count()
        if existing_users == 0:
            superuser = user_create_superuser(
                email="admin@localhost", password="password"
            )
            self.stdout.write("Created superuser")
            guest = user_create(email="guest@localhost", password="password")
            guest.is_active = True
            guest.save()
            self.stdout.write("Created and manually activated normal user")
        else:
            superuser = User.objects.get(email="admin@localhost")
            guest = User.objects.get(email="guest@localhost")
        remaining_users = self.n_users - User.objects.count()
        new_user_descs = [
            User(
                email=self.fake.email(),
                preferred_name=self.fake.name() if randint(0, 1) else None,
                password=make_password(None),
            )
            for _ in range(remaining_users)
        ]
        new_users = User.objects.bulk_create(new_user_descs)
        self.stdout.write(f"Created {len(new_users)} new users")

        # Assign random profile pictures
        users_with_pictures = 0
        add_pictures_to: list[User] = [
            superuser,
            guest,
            *(
                self.fake.random_elements(new_users, unique=True)
                if new_users
                else []
            ),
        ]
        for user in add_pictures_to:
            path = self.fake.random_element(USER_AVATARS)
            with path.open("rb") as fd:
                file = cast(FileDescriptor, File(fd, name=str(path)))
                user.profile_picture = file
                user.save()
            users_with_pictures += 1
        self.stdout.write(
            f"Assigned profile pictures to {users_with_pictures} users"
        )

        return list(User.objects.all())

    def create_tasks(
        self, workspace_descriptions: list[WorkspaceDescription]
    ) -> None:
        """
        Create tasks.

        Takes in a combination of workspaces, projects.
        Creates all tasks at once.
        """
        task_descs = [
            Task(
                title=self.fake.text(
                    randint(TASK_TITLE_MIN_LENGTH, TASK_TITLE_MAX_LENGTH)
                ),
                description=self.fake.paragraph(TASK_DESCRIPTION_SENTENCES),
                project=project,
                due_date=self.fake.date_time(tzinfo=timezone.utc),
                workspace=workspace_description.workspace,
                done=self.fake.date_time(tzinfo=timezone.utc)
                if self.fake.pybool()
                else None,
                assignee=choice(workspace_description.team_members)
                # 2 out of 3 tasks have an assignee
                if randint(0, 2)
                else None,
            )
            for workspace_description in workspace_descriptions
            for project in workspace_description.projects
            # Random task amount per project, at least floor(--n-tasks / 2)
            for _ in range(randint(self.n_tasks // 2, self.n_tasks))
        ]
        tasks = Task.objects.bulk_create(task_descs)
        self.stdout.write(f"Created {len(tasks)} tasks")

    def create_workspaces(self, users: list[User]) -> list[Workspace]:
        """Create workspaces."""
        existing_workspaces = Workspace.objects.count()
        self.stdout.write(
            f"There are already {existing_workspaces} workspaces"
        )
        remaining_workspaces = max(0, self.n_workspaces - existing_workspaces)

        workspace_descs = [
            Workspace(
                title=self.fake.text(
                    randint(
                        WORKSPACE_TITLE_MIN_LENGTH, WORKSPACE_TITLE_MAX_LENGTH
                    )
                ),
                description=self.fake.paragraph(),
            )
            for _ in range(remaining_workspaces)
        ]
        workspaces = Workspace.objects.bulk_create(workspace_descs)
        self.stdout.write(f"Created {len(workspaces)} new workspaces")
        for workspace in workspaces:
            path = self.fake.random_element(USER_AVATARS)
            with path.open("rb") as fd:
                file = cast(FileDescriptor, File(fd, name=str(path)))
                workspace.picture = file
                workspace.save()
        self.stdout.write("Added pictures to workspaces")

        team_member_descs = [
            TeamMember(
                workspace=workspace,
                user=user,
                role=TeamMemberRoles.OWNER
                if user.email == "admin@localhost"
                else TeamMemberRoles.CONTRIBUTOR,
            )
            for workspace in workspaces
            for user in sample(users, self.n_add_users)
        ]
        team_members = TeamMember.objects.bulk_create(team_member_descs)
        self.stdout.write(
            f"Added {len(team_members)} users to "
            f"{len(workspaces)} new workspaces"
        )

        project_descs = [
            Project(
                title=self.fake.text(
                    randint(PROJECT_TITLE_MIN_LENGTH, PROJECT_TITLE_MAX_LENGTH)
                ),
                description=self.fake.paragraph(),
                workspace=workspace,
                due_date=self.fake.date_time(tzinfo=timezone.utc),
            )
            for workspace in workspaces
            for _ in range(self.n_projects)
        ]
        workspaces_projects = Project.objects.bulk_create(project_descs)
        self.stdout.write(f"Created {len(workspaces_projects)} projects")

        # The idea here is that instead of going into each nested object in
        # a for loop, we create them altogether at once.
        # So:
        # Create all workspaces
        # Assign all users to all new workspaces
        # Create all projects for all new workspaces
        # etc.
        workspace_descriptions: list[WorkspaceDescription] = [
            WorkspaceDescription(
                workspace=workspace,
                team_members=list(team_members),
                projects=list(projects),
            )
            for ((workspace, team_members), (_, projects)) in zip(
                groupby(
                    team_members, key=lambda team_member: team_member.workspace
                ),
                groupby(
                    workspaces_projects, key=lambda project: project.workspace
                ),
            )
        ]

        self.create_tasks(workspace_descriptions)
        return workspaces

    def create_corporate_accounts(
        self, seats: int, workspaces: list[Workspace]
    ) -> None:
        """Create corporate accounts."""
        customer_descs = [
            Customer(
                workspace=workspace,
                subscription_status=CustomerSubscriptionStatus.CUSTOM,
                seats=seats,
            )
            for workspace in workspaces
        ]
        customers = Customer.objects.bulk_create(customer_descs)
        self.stdout.write(f"Created customers for {len(customers)} workspaces")

    def create_blog_posts(self) -> None:
        """Create blog posts."""
        existing_posts = Post.objects.count()
        self.stdout.write(f"There are already {existing_posts} blog posts")
        remaining_posts = max(0, self.n_posts - existing_posts)

        post_content_descs = [
            PostContent(
                content="".join(
                    [
                        f"<p>{self.fake.paragraph()}</p>"
                        for _ in range(
                            randint(
                                POST_CONTENT_MIN_PARAGRAPHS,
                                POST_CONTENT_MAX_PARAGRAPHS,
                            )
                        )
                    ]
                )
            )
            for _ in range(remaining_posts)
        ]
        post_contents = PostContent.objects.bulk_create(post_content_descs)
        self.stdout.write(f"Created {len(post_contents)} post contents")

        post_descs = [
            Post(
                title=self.fake.sentence(),
                author=self.fake.name(),
                slug=slugify(self.fake.sentence()),
                body=post_content,
                published=self.fake.date_this_decade(),
            )
            for post_content in post_contents
        ]
        posts = Post.objects.bulk_create(post_descs)
        self.stdout.write(f"Created {len(posts)} blog posts")

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add arguments."""
        parser.add_argument(
            "--n-users",
            type=int,
            default=20,
            help="Ensure N users are created",
        )
        parser.add_argument(
            "--n-workspaces",
            type=int,
            default=5,
            help="Ensure N workspaces are present",
        )
        parser.add_argument(
            "--n-projects",
            type=int,
            default=10,
            help="Ensure N projects are added to a new workspace",
        )
        parser.add_argument(
            "--n-add-users",
            type=int,
            default=15,
            help="Ensure N users are added to new workspaces",
        )
        parser.add_argument(
            "--n-tasks",
            type=int,
            default=20,
            help="Ensure up to N tasks are in new project",
        )
        parser.add_argument(
            "--n-posts",
            type=int,
            default=40,
            help="Ensure N blog posts are present",
        )

    def handle(self, *args: object, **options: Any) -> None:
        """Handle."""
        del args
        self.stdout.write("Running migrations")
        call_command("migrate")
        self.stdout.write("Migrations complete")

        self.fake = Faker()
        self.n_users = options["n_users"]
        self.n_workspaces = options["n_workspaces"]
        self.n_projects = options["n_projects"]
        self.n_tasks = options["n_tasks"]
        self.n_add_users = options["n_add_users"]
        self.n_posts = options["n_posts"]
        if self.n_add_users > self.n_users:
            self.stdout.write(
                f"You are trying to add more users to each workspace "
                f"({self.n_add_users} users) than are "
                f"requested to be created in the first place. "
                f"({self.n_users} users) "
                f"The amount of users created will be increase to "
                f"{self.n_add_users}."
            )
            self.n_users = max(self.n_users, self.n_add_users)

        with transaction.atomic():
            users = self.create_users()
            workspaces = self.create_workspaces(users)
            self.create_corporate_accounts(
                seats=self.n_users, workspaces=workspaces
            )
            self.create_blog_posts()
