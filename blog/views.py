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
