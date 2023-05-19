"""Premail views."""
from inspect import (
    getdoc,
)

from django.contrib.auth.mixins import (
    UserPassesTestMixin,
)
from django.views.generic import (
    TemplateView,
)

from .registry import (
    registry,
)


class SuperUserTestMixin(UserPassesTestMixin):
    """Permission mixin that tests for superuser status."""

    def test_func(self):
        """Assert that user is superuser."""
        # XXX
        return self.request.user.is_superuser  # type: ignore


class EmailList(SuperUserTestMixin, TemplateView):
    """List all available emails."""

    template_name = "premail/email_list.html"

    def get_context_data(self, **kwargs):
        """Populate with all available emails."""
        context = super().get_context_data(**kwargs)
        object_list = [
            {
                "doc": getdoc(registry[key]),
                "slug": key,
            }
            for key in registry.keys()
        ]
        context["object_list"] = object_list
        return context


class EmailPreview(SuperUserTestMixin, TemplateView):
    """Preview an email."""

    template_name = "premail/email_detail.html"

    def get_context_data(self, **kwargs):
        """Add email preview data to context."""
        context = super().get_context_data(**kwargs)
        Email = registry[self.kwargs["slug"]]
        email = Email(obj=Email.model.objects.first())
        context["subject"] = email.render_subject()
        context["body"] = email.render_body()
        return context
