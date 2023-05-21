from typing import (
    Generic,
    TypeVar,
)

from django.db import (
    models,
)

from . import (
    Factory,
)

T = TypeVar("T")
M = TypeVar("M", bound=models.Model)

class DjangoModelFactory(Generic[M], Factory[M]): ...
