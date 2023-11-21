"""Blog admin.py."""
from django.contrib import (
    admin,
)

from .models import (
    Post,
    PostImage,
)

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImage)
