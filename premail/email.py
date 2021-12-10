"""Premail email templates."""
from django.template import (
    loader,
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
        """Get context."""
        return {"object": self.model.objects.first()}

    def render_subject(self):
        """Render subject."""
        template = loader.get_template(self.get_subject_template_path())
        subject = template.render(self.get_context())
        subject = subject.replace("\n", "")
        subject = subject.strip()
        return subject

    def render_body(self):
        """Render body."""
        template = loader.get_template(self.get_body_template_path())
        return template.render(self.get_context())
