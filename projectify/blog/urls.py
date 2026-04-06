# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog URLs."""

from django.urls import path

from .feeds import LatestPostsFeed
from .views import post_detail, post_list, serve_picture, upload_attachment

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("upload", upload_attachment, name="upload_attachment"),
    path("serve-picture/<str:name>", serve_picture, name="serve_picture"),
    path("<slug:slug>/", post_detail, name="post_detail"),
    path("feed.xml", LatestPostsFeed(), name="feed"),
]
