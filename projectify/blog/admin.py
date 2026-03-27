# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024, 2026 JWP Consulting GK
"""Blog admin configuration."""

from django.contrib import admin

from projectify.blog.models import Post, PostContent


@admin.register(PostContent)
class PostContentAdmin(admin.ModelAdmin[Post]):
    """Blog post content admin."""


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    """Blog post admin."""

    list_filter = ("title",)
    list_display = ("title", "published")
