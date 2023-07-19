from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
)

from django.db.models import (
    Model,
)

from .fields import *

class BaseSerializer: ...

T = TypeVar("T")
M = TypeVar("M", bound=Model)

Data = Mapping[str, object]
ValidatedData = Mapping[str, object]

class Serializer(BaseSerializer):
    data: Data
    errors: Data
    validated_data: Data

    def __init__(
        self,
        instance: Optional[Any] = None,
        read_only: bool = False,
        many: bool = False,
        source: Optional[str] = None,
    ) -> None: ...
    def update(self, instance: Any, validated_data: ValidatedData) -> Any: ...
    def create(self, validated_data: ValidatedData) -> Any: ...
    def save(self, **kwargs: Any) -> Any: ...
    def is_valid(self, *_: Any, raise_exception: bool = False) -> bool: ...

class ModelSerializer(Generic[M], Serializer):
    def update(self, instance: M, validated_data: ValidatedData) -> M: ...
    def create(self, validated_data: ValidatedData) -> M: ...
    def save(self, **kwargs: Any) -> M: ...
