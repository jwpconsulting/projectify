# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Functionality for building error serializers."""
import logging
from typing import Any, Type, Union

from drf_spectacular.plumbing import (
    build_array_type,
    build_basic_type,
    build_object_type,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, _SchemaType
from rest_framework import serializers

logger = logging.getLogger(__name__)

SerializerField = Union[
    serializers.ListSerializer[Any],
    serializers.ListField,
    serializers.Field,
    serializers.Serializer,
]

logger = logging.getLogger(__name__)


def field_to_type(field: SerializerField) -> _SchemaType:
    """Map a serializer field to an OpenApi schema type."""
    str_type = build_basic_type(OpenApiTypes.STR)
    assert str_type is not None
    str_array = build_array_type(str_type)
    match field:
        case serializers.ListSerializer() as instance:
            child_serializer = instance.child
            if child_serializer is None:
                raise ValueError(
                    f".child for ListSerializer {instance} was None"
                )

            schema = make_schema(child_serializer)
            return build_array_type(schema)
        case serializers.Serializer() as instance:
            many = getattr(instance, "many", False)
            schema = make_schema(instance)
            if many:
                return build_array_type(schema)
            else:
                return schema
        case serializers.ListField() as instance:
            child_field = instance.child
            if child_field is None:
                raise ValueError(f".child for ListField {instance} was None")
            schema = field_to_type(child_field)
            return build_array_type(schema)
        case serializers.Field() as instance:
            return {"oneOf": [str_type, str_array]}


def make_schema(
    instance: serializers.Serializer,
) -> _SchemaType:
    """Derive a schema for a serializer instance."""
    fields: dict[str, _SchemaType] = {
        name: field_to_type(field)
        for name, field in instance.get_fields().items()
    }
    instance_doc = instance.__class__.__name__
    description = f"Errors for {instance_doc}"
    result = build_object_type(properties=fields, description=description)
    return result


def derive_bad_request_serializer(
    serializer: Type[serializers.Serializer],
) -> OpenApiResponse:
    """Derive an error serializer."""
    if isinstance(serializer, serializers.Serializer):
        instance = serializer
    else:
        instance = serializer()
    schema = make_schema(instance)
    response = OpenApiResponse(response=schema)
    return response
