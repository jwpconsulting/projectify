# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Premail email templates."""
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)

from django.conf import (
    settings,
)
from django.template import (
    loader,
)

from projectify.context_processors import (
    frontend_url,
)

from .tasks import (
    send_mail,
)

Context = dict[str, Any]

T = TypeVar("T")


class TemplateEmail(Generic[T], metaclass=ABCMeta):
    """Email template."""

    template_prefix: str
    obj: T

    def __init__(self, obj: T):
        """Designate receiver."""
        self.obj = obj

    def get_subject_template_path(self) -> str:
        """Get path of subject template."""
        return f"{self.template_prefix}_subject.txt"

    def get_body_template_path(self) -> str:
        """Get path of body template."""
        return f"{self.template_prefix}_body.txt"

    def get_context(self) -> Context:
        """Get context. To override."""
        return {
            **frontend_url(None),
            "object": self.obj,
        }

    def render_subject(self) -> str:
        """Render subject."""
        subject = loader.render_to_string(
            self.get_subject_template_path(),
            self.get_context(),
        )
        subject = subject.replace("\n", "")
        subject = subject.strip()
        return subject

    def render_body(self) -> str:
        """Render body."""
        return loader.render_to_string(
            self.get_body_template_path(),
            self.get_context(),
        )

    # TODO change to be addressee instead, we want to address the user by their
    # preferred name if they have specified one.
    @abstractmethod
    def get_to_email(self) -> str:
        """Return recipient email. To override."""

    def send(self) -> None:
        """Send email to obj."""
        if settings.EMAIL_EAGER:
            send_mail(
                self.render_subject(),
                self.render_body(),
                self.get_to_email(),
            )
        send_mail.delay(
            self.render_subject(),
            self.render_body(),
            self.get_to_email(),
        )
