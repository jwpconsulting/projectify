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
