from typing import (
    Optional,
)

from django.db import (
    models,
)

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)

class TitleDescriptionModel(models.Model):
    title: models.CharField[str]
    description: models.TextField[Optional[str]]

class TimeStampedModel(models.Model):
    created: CreationDateTimeField
    modified: ModificationDateTimeField
