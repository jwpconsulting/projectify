# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Blog app views."""
from django.db import models as django_models

from rest_framework import (
    generics,
)

from .models import (
    Post,
)
from .serializers import (
    PostSerializer,
)


class PostListView(
    generics.ListAPIView[Post, django_models.QuerySet[Post], PostSerializer]
):
    """Post List API View."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(
    generics.RetrieveAPIView[
        Post, django_models.QuerySet[Post], PostSerializer
    ]
):
    """Post Detail API View."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
