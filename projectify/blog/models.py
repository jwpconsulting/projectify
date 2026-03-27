# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023, 2026 JWP Consulting GK
"""Blog models."""

from typing import Any

from django import forms
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

import bleach

from projectify.lib.models import BaseModel
from projectify.lib.settings import get_settings


# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>
class RichTextEditor(forms.Textarea):
    """Rich text editor widget for prose's RichTextField."""

    template_name = "prose/forms/widgets/editor.html"

    class Media:
        """Use vendored in {trix,prose}.{css,js}."""

        css = {
            "all": (
                "trix/trix.css",
                "trix/prose.css",
            ),
        }
        js = (
            "trix/trix.js",
            "trix/prose.js",
        )


class RichTextField(models.TextField):  # type: ignore
    """Vendored in RichTextField from django-prose."""

    def formfield(self, **kwargs: Any) -> forms.Field:
        """Return widget."""
        kwargs = {**kwargs, "widget": RichTextEditor}
        field: forms.Field = super().formfield(**kwargs)
        return field

    def pre_save(self, model_instance: Any, add: Any) -> str:
        """Pre save."""
        settings = get_settings()
        raw_html: str = getattr(model_instance, self.attname)
        if not raw_html:
            return raw_html

        sanitized_html: str = bleach.clean(
            raw_html,
            tags=settings.MARKDOWNIFY["default"]["WHITELIST_TAGS"],
            attributes=settings.MARKDOWNIFY["default"]["WHITELIST_ATTRS"],
        )  # type: ignore[no-untyped-call]
        return sanitized_html


class DocumentContentField(RichTextField):
    """Class copied in from prose/fields.py."""


class AbstractDocument(models.Model):
    """Class copied in from prose/models.py."""

    content = DocumentContentField()

    def get_plain_text_content(self) -> str:
        """Return plain text content."""
        return strip_tags(self.content)

    def __str__(self) -> str:
        """Return string representation."""
        plain_text = self.get_plain_text_content()

        if len(plain_text) < 32:
            return plain_text

        return f"{plain_text[:28]}..."

    class Meta:
        """Make this an abstract class."""

        abstract = True


# SPDX-SnippetEnd


class PostContent(AbstractDocument):
    """Contains the large rich-text content for a post."""

    content = DocumentContentField()


class Post(BaseModel):
    """Blog post."""

    title = models.CharField(verbose_name=_("Blog post title"))
    author = models.CharField(verbose_name=_("Blog post author"))
    slug = models.SlugField(
        verbose_name=_("Blog post slug"), unique=True, max_length=255
    )
    body = models.OneToOneField(
        PostContent, verbose_name=_("Blog post body"), on_delete=models.CASCADE
    )
    published = models.DateTimeField(verbose_name=_("Blog post publish date"))
