"""Premail email templates."""
from django.shortcuts import (
    render,
)

from projectify.context_processors import (
    frontend_url,
)


class TemplateEmail:
    """Email template."""

    def get_subject_template_path(self):
        """Get path of subject template."""
        return f"{self.template_prefix}_subject.txt"

    def get_body_template_path(self):
        """Get path of body template."""
        return f"{self.template_prefix}_body.txt"

    def get_context(self):
        """Get context. To override."""
        return {
            **frontend_url(None),
            "object": self.obj,
        }

    def render_subject(self):
        """Render subject."""
        subject = render(
            None,
            self.get_subject_template_path(),
            self.get_context(),
        )
        subject = subject.content.decode()
        subject = subject.replace("\n", "")
        subject = subject.strip()
        return subject

    def render_body(self):
        """Render body."""
        return render(
            None,
            self.get_body_template_path(),
            self.get_context(),
        ).content.decode()
