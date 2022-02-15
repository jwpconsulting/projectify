"""User schema types."""
from django.contrib import (
    auth,
)

import graphene
import graphene_django


class User(graphene_django.DjangoObjectType):
    """User."""

    profile_picture = graphene.String()

    def resolve_profile_picture(self, info):
        """Resolve profile_picture."""
        if self.profile_picture:
            return self.profile_picture.url

    class Meta:
        """Meta."""

        fields = ("email",)
        model = auth.get_user_model()
