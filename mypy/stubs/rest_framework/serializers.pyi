# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from collections.abc import Mapping, Sequence
from typing import Any, TypeVar, Union

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Model

from .exceptions import ErrorDetail, ValidationError

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

# Inferred by inspecting rest_framework/serializers.py:as_serializer_error
SerializerErrorField = Union[
    tuple[ErrorDetail],
    list[ErrorDetail],
    list["SerializerErrorField"],
    dict[str, "SerializerErrorField"],
]
SerializerError = dict[str, SerializerErrorField]

def as_serializer_error(
    exc: Union[ValidationError, DjangoValidationError],
) -> SerializerError: ...

T = TypeVar("T")
M = TypeVar("M", bound=Model)

__all__ = ("ValidationError",)
