from datetime import (
    datetime,
)

from django.db.models import (
    DateTimeField,
)

class CreationDateTimeField(DateTimeField[datetime]): ...
class ModificationDateTimeField(CreationDateTimeField): ...
