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
"""Blog serializers."""

from rest_framework import (
    serializers,
)

from .models import (
    Post,
    PostImage,
)


class PostSerializer(serializers.ModelSerializer[Post]):
    """Post serializer."""

    class Meta:
        """Meta."""

        model = Post
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "teaser",
            "author",
            "published",
        ]


class PostImageSerializer(serializers.ModelSerializer[PostImage]):
    """PostImage Serializer."""

    class Meta:
        """Meta."""

        model = PostImage
        fields = ["id", "image"]
