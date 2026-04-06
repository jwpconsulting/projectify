# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023, 2026 JWP Consulting GK
"""Blog models."""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import AbstractDocument, BaseModel

# SPDX-SnippetBegin
# SPDX-License-Identifier: MIT
# SPDX-SnippetCopyrightText: 2022 LOGIC SMPC <paris@withlogic.co>
# SPDX-SnippetEnd


class PostContent(AbstractDocument):
    """Contains the large rich-text content for a post."""


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
    published = models.DateField(verbose_name=_("Blog post publish date"))

    def __str__(self) -> str:
        """Return string representation."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return absolute URL for this post."""
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    class Meta(BaseModel.Meta):
        """Meta options."""

        ordering = ["-published"]
