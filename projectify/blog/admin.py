# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024, 2026 JWP Consulting GK
"""Blog admin configuration."""

from typing import Any

from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from projectify.blog.models import (
    Post,
    PostContent,
    RichTextEditor,
    clean_post_text,
)


class PostAdminForm(forms.ModelForm):
    """Custom form for Post admin that includes PostContent field."""

    content = forms.CharField(
        widget=RichTextEditor, help_text=_("Blog post content")
    )

    published = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
        help_text=_("Blog post publish date"),
    )

    class Meta:
        """Meta options."""

        model = Post
        fields = "__all__"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize form and populate content field."""
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            from django.utils import timezone

            self.fields["published"].initial = timezone.now().date()
            return
        if not self.instance.body:
            return
        body = self.instance.body
        # body.content is safe because pre_save()
        # sanitizes it with bleach
        self.fields["content"].initial = body.content

    def clean_content(self) -> str:
        """Sanitize content."""
        # We clean the content on top of cleaning it in
        # RichTextField.pre_save()
        content: str = clean_post_text(self.cleaned_data["content"])
        self.cleaned_data["content"] = content
        return content

    def save(self, commit: bool = True) -> Post:
        """Save Post and associated PostContent."""
        post: Post = super().save(commit=False)
        content_text = self.cleaned_data["content"]

        if not post.body:
            body = PostContent.objects.create(content=content_text)
            post.body = body
        else:
            body = post.body
            body.content = content_text
            body.save()
        post.save()

        return post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    """Blog post admin."""

    form = PostAdminForm
    list_filter = ("title",)
    list_display = ("title", "published", "post_url")
    exclude = ("body",)

    @admin.display(description=_("URL"))
    def post_url(self, instance: Post) -> str:
        """Return link to blog post."""
        url = reverse("blog:detail", kwargs={"slug": instance.slug})
        return mark_safe(f'<a href="{url}" target="_blank">View post</a>')
