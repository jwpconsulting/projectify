# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2023 JWP Consulting GK
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
"""Premail views."""
from inspect import (
    getdoc,
)
from typing import (
    Any,
    Dict,
    cast,
)

from django.contrib.auth.mixins import (
    UserPassesTestMixin,
)
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    TemplateView,
)

from projectify.admin.admin import ProjectifyAdmin
from projectify.user.models.user import User

from .registry import (
    registry,
)


class SuperUserTestMixin(UserPassesTestMixin):
    """Permission mixin that tests for superuser status."""

    request: HttpRequest

    def test_func(self) -> bool:
        """Assert that user is superuser."""
        # XXX the request should have a user here, at least as an optional
        user = cast(User, self.request.user)
        return user.is_superuser


# TODO we might want to figure out how to properly add templated sites to
# django admin instead of having to manually pull in site_header, site_title
# and so on from ProjectifyAdmin


class EmailList(SuperUserTestMixin, TemplateView):
    """List all available emails."""

    template_name = "premail/email_list.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Populate with all available emails."""
        return {
            **super().get_context_data(**kwargs),
            "site_header": ProjectifyAdmin.site_header,
            "site_title": ProjectifyAdmin.site_title,
            "title": _("Emails"),
            "object_list": [
                {
                    "doc": getdoc(registry[key]),
                    "slug": key,
                }
                for key in registry.keys()
            ],
        }


class EmailPreview(SuperUserTestMixin, TemplateView):
    """Preview an email."""

    template_name = "premail/email_detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add email preview data to context."""
        slug: str = self.kwargs["slug"]
        Email = registry[slug]
        email = Email(
            receiver="hello@example.com",
            obj=Email.model.objects.first(),
        )
        return {
            **super().get_context_data(**kwargs),
            "site_header": ProjectifyAdmin.site_header,
            "site_title": ProjectifyAdmin.site_title,
            "title": _("{} preview").format(slug),
            "subject": email.render_subject(),
            "body": email.render_body(),
        }
