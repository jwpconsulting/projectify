"""Blog models."""
from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
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
    from user.models import (  # noqa: F401
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

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        """Create slug if no slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self) -> str:
        """Return the title when accessing __str__."""
        return self.title


class PostImage(BaseModel):
    """Post Image Model."""

    post = models.ForeignKey["Post"](Post, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="post_image/",
    )
