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
"""Blog models."""
from typing import (
    TYPE_CHECKING,
    Any,
)

from django.conf import (
    settings,
)
from django.db import (
    models,
)
from django.template.defaultfilters import (
    slugify,
)

from projectify.lib.models import BaseModel

if TYPE_CHECKING:
    from projectify.user.models import (  # noqa: F401
        User,
    )


class Post(BaseModel):
    """Post Model."""

    title = models.CharField(max_length=300)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey["User"](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    teaser = models.TextField()
    published = models.DateTimeField(blank=True, null=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Create slug if no slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return the title when accessing __str__."""
        return self.title


class PostImage(BaseModel):
    """Post Image Model."""

    post = models.ForeignKey["Post"](Post, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="post_image/",
    )
