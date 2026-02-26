# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Premail email templates."""

import re
from typing import Any, Generic, NewType, TypeVar, Union

from django.template import loader
from django.utils.safestring import SafeText, mark_safe

from projectify.context_processors import frontend_url
from projectify.user.models import User

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

    def render_subject(self) -> SafeText:
        """Render subject."""
        subject = loader.render_to_string(
            self.get_subject_template_path(),
            self.get_context(),
        )
        subject = mark_safe(subject.replace("\n", ""))
        subject = mark_safe(subject.strip())
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
        # Put import here to avoid Django populate() reentrancy problem
        from .tasks import send_mail

        subject = self.render_subject()
        body = self.render_body()
        send_mail(subject, body, self.to)

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
