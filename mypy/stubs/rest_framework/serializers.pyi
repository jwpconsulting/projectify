from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
)

from django.db.models import (
    Model,
)

from .fields import *
from .relations import *

class BaseSerializer:
    def __init__(
        self,
        instance: Optional[object] = None,
        data: Union[object, type[empty]] = empty,
        read_only: bool = False,
        many: bool = False,
        source: Optional[str] = None,
        **kwargs: Any
    ) -> None: ...

T = TypeVar("T")
M = TypeVar("M", bound=Model)

Data = Mapping[str, Any]
ValidatedData = dict[str, Any]

class Serializer(BaseSerializer):
    data: Data
    errors: Data
    validated_data: Data

    def update(self, instance: Any, validated_data: ValidatedData) -> Any: ...
    def create(self, validated_data: ValidatedData) -> Any: ...
    def save(self, **kwargs: Any) -> Any: ...
    def is_valid(self, *_: Any, raise_exception: bool = False) -> bool: ...

class ModelSerializer(Generic[M], Serializer):
    def update(self, instance: M, validated_data: ValidatedData) -> M: ...
    def create(self, validated_data: ValidatedData) -> M: ...
    def save(self, **kwargs: Any) -> M: ...
