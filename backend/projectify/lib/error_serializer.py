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
import inspect
import logging
from collections.abc import Sequence
from typing import Any, Literal, Union

from drf_spectacular.plumbing import (
    build_array_type,
    build_basic_type,
    build_object_type,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, _SchemaType
from rest_framework import fields, serializers

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
    serializer: Union[type[serializers.Serializer], serializers.Serializer],
) -> OpenApiResponse:
    """Derive an error serializer."""
    if isinstance(serializer, serializers.Serializer):
        instance = serializer
    else:
        instance = serializer()
    schema = make_schema(instance)
    response = OpenApiResponse(response=schema)
    return response


# More methods than you ever asked for
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
Method = Literal[
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH",
]
# Has to extend something like this: Callable[..., HttpResponse]
# and add "cls" attribute
SchemaAnnotatedCallable = Any
# path, path_regex, method, callback
Endpoint = Sequence[tuple[str, str, Method, SchemaAnnotatedCallable]]
RequestAnnotation = Union[
    None,
    serializers.Serializer,
    type[serializers.Serializer],
    fields.empty,
]
ResponseAnnotation = Union[
    None,
    OpenApiResponse,
    serializers.Serializer,
    type[serializers.Serializer],
    fields.empty,
    dict[int, "ResponseAnnotation"],
]
MaybeSerializer = Union[None, Any, dict[int, serializers.Serializer]]


def preprocess_bad_request_serializers(endpoints: Endpoint) -> Endpoint:
    """Process drf-spectactular schema and add missing HTTP 400 schemas."""
    method_names = ["POST", "PUT"]
    # These are the functions we want to annotate
    # https://github.com/tfranzel/drf-spectacular/blob/b1a34b05230316ca6c6d6724f2b9bb970a8dbe79/drf_spectacular/utils.py#L549
    endpoints_edit = (
        (path, method_name, callback)
        for path, _, method_name, callback in endpoints
        if method_name in method_names
        and callable(callback)
        and hasattr(callback, "cls")
    )
    for path, method_name, callback in endpoints_edit:
        assert hasattr(callback, "cls")
        method = getattr(callback.cls, method_name.lower())
        schema = method.kwargs["schema"]
        # Unfortunately we can't just call get_response_serializers. It expects
        # a complicated dance with a view and request instance, and will
        # blow up. Instead, we just peek inside and find what extend_schema
        # has been called with
        request_nonlocals, _, _, _ = inspect.getclosurevars(
            schema.get_request_serializer
        )
        responses_nonlocals, _, _, _ = inspect.getclosurevars(
            schema.get_response_serializers
        )
        request: RequestAnnotation = request_nonlocals["request"]
        responses: ResponseAnnotation = responses_nonlocals["responses"]
        match request, responses:
            case (
                None
                | fields.empty,
                None
                | fields.empty
                | OpenApiResponse()
                | serializers.Serializer()
                | dict(),
            ):
                continue
            case (
                type()
                | serializers.Serializer() as ser_inst,
                dict() as responses,
            ):
                http_400_response = responses.get(400)
                if http_400_response is not None:
                    continue
                responses[400] = derive_bad_request_serializer(ser_inst)
            case _:
                raise ValueError(
                    f"Don't know what to do with {path} {method_name}"
                    f"Request: {request}, responses: {responses}"
                )
    return endpoints
