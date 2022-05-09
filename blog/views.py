"""Blog app views."""
from rest_framework import (
    generics,
)

from .models import (
    Post,
)
from .serializers import (
    PostSerializer,
)


class PostListView(generics.ListAPIView):
    """Post List API View."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    """Post Detail API View."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
