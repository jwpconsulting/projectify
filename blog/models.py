"""Blog models."""

from django.conf import (
    settings,
)
from django.db import (
    models,
)
from django.template.defaultfilters import (
    slugify,
)

from django_extensions.db.models import (
    TimeStampedModel,
)


class Post(TimeStampedModel):
    """Post Model."""

    title = models.CharField(max_length=300)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    teaser = models.TextField()
    published = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Create slug if no slug."""
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        """Return the title when accessing __str__."""
        return self.title


class PostImage(TimeStampedModel):
    """Post Image Model."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="post_image/",
    )
