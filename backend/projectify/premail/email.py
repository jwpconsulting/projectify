# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Premail email templates."""

import re
from typing import Any, Generic, NewType, TypeVar, Union

from django.conf import settings
from django.template import loader

from projectify.context_processors import frontend_url
from projectify.user.models.user import User

from .tasks import send_mail

Context = dict[str, Any]

T = TypeVar("T")

EmailAddress = NewType("EmailAddress", str)


class TemplateEmail(Generic[T]):
    """Email template."""

    template_prefix: str
    obj: T
    receiver: Union[User, EmailAddress]

    def __init__(self, *, receiver: Union[User, EmailAddress], obj: T):
        """Designate receiver."""
        self.receiver = receiver
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
            "addressee": self.addressee,
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
        return re.sub(
            r"\n\n\n+",
            "\n\n",
            loader.render_to_string(
                self.get_body_template_path(),
                self.get_context(),
            ).strip(),
        )

    def send(self) -> None:
        """Send email to obj."""
        subject = self.render_subject()
        body = self.render_body()
        if settings.EMAIL_EAGER:
            send_mail(subject, body, self.to)
        else:
            send_mail.delay(subject, body, self.to)

    @property
    def addressee(self) -> str:
        """Return displayable name for receiver of this email."""
        match self.receiver:
            case User(email=email, preferred_name=preferred_name):
                return preferred_name or email
            case email:
                return email

    @property
    def to(self) -> str:
        """Return email address email should be sent to."""
        match self.receiver:
            case User(email=email):
                return email
            case email:
                return email
