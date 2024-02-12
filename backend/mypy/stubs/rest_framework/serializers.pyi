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

from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db.models import (
    Model,
)

from .exceptions import (
    ValidationError,
)
from .fields import *  # noqa: F403
from .fields import Field, empty
from .relations import *  # noqa: F403

# Ensure we don't pass in unserialized UUIDs
SerializerData = Union[None, str, int, "SerializerList", "SerializerDict"]
SerializerDict = Mapping[str, SerializerData]
SerializerList = Sequence[SerializerData]

# But! a model serializer will always give us SerializerData inside a dict
# (such is the nature of a model instance, it has properties inside an object)
# Of course a model's list serializer will yield us a list of
# ModelSerializerData
ModelSerializerData = Union[
    Mapping[str, SerializerData], Sequence[SerializerData]
]

# TODO make me an error dict
Errors = Any

# TODO Make me serialized data
ValidatedData = Any

Context = Mapping[str, Any]

class BaseSerializer:
    context: Context
    initial_data: Optional[SerializerData]
    parent: Optional[Serializer]
    fields: Mapping[str, Union[BaseSerializer, Field]]

    def __init__(
        self,
        instance: Optional[object] = None,
        data: Union[SerializerData, type[empty]] = empty,
        read_only: bool = False,
        many: bool = False,
        source: Optional[str] = None,
        context: Optional[Context] = None,
        **kwargs: Any,
    ) -> None: ...
    def to_internal_value(self, data: Any) -> ValidatedData: ...
    def to_representation(self, instance: object) -> SerializerData: ...
    def run_validation(
        self, data: Union[SerializerData, type[empty]] = empty
    ) -> ValidatedData: ...
    def update(self, instance: Any, validated_data: ValidatedData) -> Any: ...
    def create(self, validated_data: ValidatedData) -> Any: ...
    def save(self, **kwargs: Any) -> Any: ...
    def is_valid(self, *_: Any, raise_exception: bool = False) -> bool: ...

def as_serializer_error(
    exc: Union[ValidationError, DjangoValidationError],
) -> Mapping[str, Any]: ...

T = TypeVar("T")
M = TypeVar("M", bound=Model)

class Serializer(BaseSerializer):
    # XXX not sure if some of these actually belong in the BaseSerializer
    data: SerializerData
    errors: Errors
    validated_data: ValidatedData

class ListSerializer(Generic[M], BaseSerializer):
    child: Optional[ModelSerializer[M]]
    initial_data: Optional[Sequence[SerializerData]]
    instance: Optional[Sequence[M]]

    def __init__(
        self,
        # This will be a deepcopy of self.child, which itself can be None
        child: Optional[ModelSerializer[M]] = None,
        instance: Sequence[M] = [],
        data: SerializerList = [],
        allow_empty: bool = True,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
    ) -> None: ...
    def run_child_validation(self, data: SerializerData) -> SerializerData: ...

class ModelSerializer(Generic[M], Serializer):
    instance: Optional[M]
    data: ModelSerializerData

    def update(self, instance: M, validated_data: ValidatedData) -> M: ...
    def create(self, validated_data: ValidatedData) -> M: ...
    def save(self, **kwargs: Any) -> M: ...

__all__ = ("ValidationError",)
