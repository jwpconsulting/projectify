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
