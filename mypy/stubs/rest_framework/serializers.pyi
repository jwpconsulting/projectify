from collections.abc import (
    Mapping,
    Sequence,
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

from .exceptions import (
    ValidationError,
)
from .fields import *
from .relations import *

# Ensure we don't pass in unserialized UUIDs
SerializerData = Union[None, str, int, "SerializerList", "SerializerDict"]
SerializerDict = Mapping[str, SerializerData]
SerializerList = Sequence[SerializerData]

# But! a model serializer will always give us SerializerData inside a dict
# (such is the nature of a model instance, it has properties inside an object)
# Of course a model's list serializer will yield us a list of
# ModelSerializerData
ModelSerializerData = dict[str, SerializerData]

class BaseSerializer:

    context: dict[str, Any]

    def __init__(
        self,
        instance: Optional[object] = None,
        data: Union[SerializerData, type[empty]] = empty,
        read_only: bool = False,
        many: bool = False,
        source: Optional[str] = None,
        **kwargs: Any
    ) -> None: ...

T = TypeVar("T")
M = TypeVar("M", bound=Model)

# TODO make me an error dict
Errors = Any

# TODO Make me serialized data
ValidatedData = Any

class Serializer(BaseSerializer):
    data: SerializerData
    errors: Errors
    validated_data: ValidatedData

    def update(self, instance: Any, validated_data: ValidatedData) -> Any: ...
    def create(self, validated_data: ValidatedData) -> Any: ...
    def save(self, **kwargs: Any) -> Any: ...
    def is_valid(self, *_: Any, raise_exception: bool = False) -> bool: ...

class ModelSerializer(Generic[M], Serializer):
    instance: Optional[M]
    data: ModelSerializerData

    def update(self, instance: M, validated_data: ValidatedData) -> M: ...
    def create(self, validated_data: ValidatedData) -> M: ...
    def save(self, **kwargs: Any) -> M: ...

__all__ = ("ValidationError",)
