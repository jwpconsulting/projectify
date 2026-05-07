# SPDX-FileCopyrightText: 2026 JWP Consulting GK
# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Take Projectify UI component screenshots.

This file was partially created using an sonnet-4.
"""

from pathlib import Path
from typing import Any, Optional, cast

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields.files import FileDescriptor
from django.urls import reverse
from django.utils.html import format_html

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.user.models import User
from projectify.user.services.auth import user_confirm_email
from projectify.user.services.internal import user_create, user_make_token
from projectify.user.services.user import user_update
from projectify.workspace.models import Workspace
from projectify.workspace.services.project import (
    project_create,
    project_delete,
)
from projectify.workspace.services.task import task_create
from projectify.workspace.services.team_member_invite import (
    team_member_invite_create,
)
from projectify.workspace.services.workspace import (
    workspace_create,
    workspace_delete,
)

USER_AVATARS = [
    Path("projectify/test/test-images/cat1.jpg"),
    Path("projectify/test/test-images/cat2.jpg"),
    Path("projectify/test/test-images/cat3.jpg"),
    Path("projectify/test/test-images/cat4.jpg"),
]
USER_NAMES = ["Rebecca Porter", "Joe Swish", "Fran Bauer", "Mina Kidane"]


class Command(BaseCommand):
    """Take screenshots of Projectify UI components."""

    help = "Take a screenshot of the main element on localhost:8000"

    workspace: Optional[Workspace] = None
    owner: Optional[User] = None
    test_users: list[User] = []
    essay_task = None
    in_progress_project = None
    coursework_project = None
    software_project = None

    @transaction.atomic
    def create_test_data(self) -> None:
        """Create test workspace and data."""
        Faker.seed(0)
        fake = Faker()
        users: list[User] = []
        for preferred_name, avatar_path in zip(USER_NAMES, USER_AVATARS):
            user = user_create(
                email=preferred_name.replace(" ", "") + fake.email(),
                password="password",
            )
            token = user_make_token(user=user, kind="confirm_email_address")
            assert user_confirm_email(email=user.email, token=token)
            user.refresh_from_db()

            with avatar_path.open("rb") as fd:
                django_file = cast(
                    FileDescriptor, File(fd, name=str(avatar_path))
                )
                user_update(
                    who=user,
                    user=user,
                    preferred_name=preferred_name,
                    profile_picture=django_file,
                )
            users.append(user)

        self.owner, *self.test_users = users
        self.stdout.write("Created owner")
        self.stdout.write(f"Created {len(self.test_users)} other test users")

        self.workspace = workspace_create(
            title="ACME Corporation",
            description="Test workspace for ACME Corporation",
            owner=self.owner,
        )
        customer = self.workspace.customer
        customer.subscription_status = CustomerSubscriptionStatus.ACTIVE
        customer.seats = 5
        customer.save()

        for user in self.test_users:
            team_member_invite_create(
                workspace=self.workspace, email_or_user=user, who=self.owner
            )
        team_members = self.workspace.teammember_set.all()

        self.software_project = project_create(
            who=self.owner,
            workspace=self.workspace,
            title_description=format_html(
                "<h1>{}</h1><p>{}</p>",
                "Software Development Project",
                "Main software development project",
            ),
        )
        self.in_progress_project = project_create(
            who=self.owner,
            workspace=self.workspace,
            title_description=format_html(
                "<h1>{}</h1><p>{}</p>", "In Progress", "In progress tasks"
            ),
        )
        self.coursework_project = project_create(
            who=self.owner,
            workspace=self.workspace,
            title_description=format_html(
                "<h1>{}</h1><p>{}</p>", "Coursework", "Coursework tasks"
            ),
        )

        # Used in development team solutions page
        task_create(
            who=self.owner,
            project=self.in_progress_project,
            title_description="<p>Beta testing for level 6</p>"
            "<p>Conduct beta testing for level 6 functionality</p>",
            assignee=fake.random_element(elements=team_members),
        )

        tasks_data = [
            (
                "Fix collision engine bug",
                "Investigate and fix the collision engine bug",
            ),
            (
                "Character skin drafts",
                "Create initial drafts for character skins",
            ),
        ]
        for title, description in tasks_data:
            task_create(
                who=self.owner,
                project=self.in_progress_project,
                title_description=format_html(
                    "<p>{}</p><p>{}</p>", title, description
                ),
                assignee=fake.random_element(elements=team_members),
            )

        # Used in academic solutions page
        self.essay_task = task_create(
            who=self.owner,
            project=self.coursework_project,
            title_description="<p>Write essay for assignment</p>"
            "<p>Complete the essay assignment for the course</p>",
            assignee=fake.random_element(elements=team_members),
        )
        task_create(
            who=self.owner,
            project=self.coursework_project,
            title_description="Research methodology review",
            assignee=fake.random_element(elements=team_members),
        )

        task_create(
            who=self.owner,
            project=self.coursework_project,
            title_description="Prepare presentation slides",
            assignee=fake.random_element(elements=team_members),
        )

    def cleanup_test_data(self) -> None:
        """Clean up test users and data."""
        if not self.owner:
            self.stdout.write("Owner was never created")
            return

        for user in self.test_users:
            user.delete()

        if self.workspace:
            for project in self.workspace.project_set.all():
                project_delete(who=self.owner, project=project)
            workspace_delete(who=self.owner, workspace=self.workspace)

        self.owner.delete()

    def remove_debug_toolbar(self, driver: WebDriver) -> None:
        """Remove Django debug toolbar if present."""
        try:
            debug_element = driver.find_element(By.ID, "djDebug")
            driver.execute_script("arguments[0].remove();", debug_element)
        except Exception:
            self.stdout.write("No debug toolbar found")

    def take_screenshot(
        self, driver: WebDriver, base_url: str, output_directory: Path
    ) -> None:
        """Take all screenshots."""
        assert self.owner
        assert self.workspace
        assert self.software_project
        assert self.in_progress_project
        assert self.coursework_project
        assert self.essay_task

        driver.get(f"{base_url}{reverse('users:log-in')}")
        wait = WebDriverWait(driver, 2)
        email_field = wait.until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.clear()
        email_field.send_keys(self.owner.email)
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys("password")
        submit_button = driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )
        submit_button.click()

        # go to project detail page for the software project
        driver.get(
            f"{base_url}{reverse('dashboard:projects:detail', kwargs={'project_uuid': self.software_project.uuid})}"
        )

        self.remove_debug_toolbar(driver)

        # development team solutions tasks
        driver.get(
            f"{base_url}{reverse('dashboard:projects:detail', kwargs={'project_uuid': self.in_progress_project.uuid})}"
        )
        self.remove_debug_toolbar(driver)
        project_main_selector = 'div[role="presentation"] main'
        in_progress_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, project_main_selector)
            )
        )
        in_progress_element.screenshot(
            str(output_directory / "development-teams-tasks.png")
        )

        # project management solutions team member filter
        team_member_filters_selector = "#team-member-filters"
        team_member_filters_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, team_member_filters_selector)
            )
        )
        team_member_filters_element.screenshot(
            str(output_directory / "project-management-team-member.png")
        )

        # project management solutions permissions screen
        driver.get(
            f"{base_url}{reverse('dashboard:workspaces:team-members', kwargs={'workspace_uuid': self.workspace.uuid})}"
        )
        self.remove_debug_toolbar(driver)
        team_members_selector = 'div[role="presentation"] main'
        team_members_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, team_members_selector)
            )
        )
        team_members_element.screenshot(
            str(output_directory / "project-management-permissions.png")
        )

    def add_arguments(self, parser: Any) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--url",
            default="http://localhost:8000",
            help="URL to screenshot (default: http://localhost:8000)",
        )
        parser.add_argument(
            "--output",
            default="screenshot.png",
            help="Output file path (default: screenshot.png)",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the command."""
        del args, options

        url = "http://localhost:8000"
        output_directory = Path("projectify/storefront/static/solutions")
        output_directory.mkdir(parents=True, exist_ok=True)

        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = None

        try:
            self.create_test_data()
            driver = webdriver.Firefox(options=firefox_options)
            driver.set_window_size(1024, 1920)
            self.take_screenshot(
                driver, base_url=url, output_directory=output_directory
            )
        finally:
            self.cleanup_test_data()
            if driver:
                driver.quit()
