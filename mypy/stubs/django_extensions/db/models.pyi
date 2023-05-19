from django.db import (
    models,
)

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)

class TitleDescriptionModel(models.Model):

    title: models.CharField[str]
    description: models.TextField[str]

class TimeStampedModel(models.Model):

    created: CreationDateTimeField
    modified: ModificationDateTimeField
