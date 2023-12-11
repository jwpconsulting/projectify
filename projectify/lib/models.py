"""Projectify base models."""
from django.db.models import Model

from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel, Model):
    """The base model to use for all Projectify models."""

    class Meta(TimeStampedModel.Meta):
        """Make this model abstract."""

        abstract = True
