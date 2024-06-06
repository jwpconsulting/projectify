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
from collections.abc import Callable, Sequence
from typing import Any, Literal, Optional, Union

from drf_spectacular.plumbing import (
    build_array_type,
    build_object_type,
)
from drf_spectacular.utils import OpenApiResponse, _SchemaType
from rest_framework import fields, serializers, status

from projectify.exception_handler import (
    NotFoundSerializer,
    TooManyRequestsSerializer,
)

logger = logging.getLogger(__name__)

SerializerField = Union[
    serializers.ListSerializer[Any],
    serializers.ListField,
    serializers.Field,
    serializers.Serializer,
]


def field_to_type(field: SerializerField) -> _SchemaType:
    """Map a serializer field to an OpenApi schema type."""
    match field:
        case serializers.ListSerializer() as instance:
            child_serializer = instance.child
            if child_serializer is None:
                raise ValueError(
                    f".child for ListSerializer {instance} was None"
                )

            schema = make_schema_nested(child_serializer)
            return build_array_type(schema)
        case serializers.Serializer() as instance:
            many = getattr(instance, "many", False)
            schema = make_schema_nested(instance)
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
            return {"type": "string"}


def make_schema_nested(instance: serializers.Serializer) -> _SchemaType:
    """Derive a schema for a serializer instance."""
    fields: dict[str, _SchemaType] = {
        name: field_to_type(field)
        for name, field in instance.get_fields().items()
    }
    instance_doc = instance.__class__.__name__
    description = f"Errors for {instance_doc}"
    result = build_object_type(properties=fields, description=description)
    return result


def make_schema(instance: serializers.Serializer) -> _SchemaType:
    """Derive a schema for a serializer instance."""
    schema = build_object_type(
        description="Error schema",
        properties={
            "code": {"type": "integer", "enum": [400]},
            "details": make_schema_nested(instance),
            "general": {"type": "array", "items": {"type": "string"}},
            "status": {"type": "string", "enum": ["error"]},
        },
        required=[
            "code",
            "details",
            "general",
            "status",
        ],
    )
    return schema


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
Endpoints = Sequence[tuple[str, str, Method, SchemaAnnotatedCallable]]
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
ResponsesDict = dict[int, "ResponseAnnotation"]
MaybeSerializer = Union[None, Any, dict[int, serializers.Serializer]]

SerializerClassOrInstance = Union[
    type[serializers.Serializer], serializers.Serializer
]


DeriveSchema = object()


def get_request_serializer(
    annotation: RequestAnnotation,
) -> Optional[SerializerClassOrInstance]:
    """Extract a Serializer instance or constructor from request annot."""
    match annotation:
        case None | fields.empty:
            return None
        case type() | serializers.Serializer() as ser_inst:
            return ser_inst
        case _:
            raise ValueError(f"Don't know what to do with {annotation}")


def maybe_annotate_400(
    path: str, d: ResponsesDict, s: Optional[SerializerClassOrInstance]
) -> None:
    """Annotate 404."""
    if d.get(status.HTTP_400_BAD_REQUEST) is not DeriveSchema:
        return
    if s is None:
        raise ValueError(
            f"Trying to create 400 response schema, but no "
            f"request serializer was provided in {path}"
        )
    d[status.HTTP_400_BAD_REQUEST] = derive_bad_request_serializer(s)


ViewMethod = Callable[..., Any]


def maybe_annotate_404(method: ViewMethod, d: ResponsesDict) -> None:
    """Annotate 404."""
    if not has_view_args(method):
        return
    if status.HTTP_404_NOT_FOUND in d:
        return
    d[status.HTTP_404_NOT_FOUND] = NotFoundSerializer


def maybe_annotate_429(d: ResponsesDict) -> None:
    """Annotate 429."""
    if d.get(status.HTTP_429_TOO_MANY_REQUESTS) is not DeriveSchema:
        return
    d[status.HTTP_429_TOO_MANY_REQUESTS] = TooManyRequestsSerializer


def has_view_args(c: ViewMethod) -> bool:
    """Return True if a view function takes UUID or other args."""
    sig = inspect.signature(c)
    params = list(sig.parameters.values())
    match params:
        # APIView with at least one extra arg
        case [
            inspect.Parameter(name="self"),
            inspect.Parameter(name="request"),
            _,
            *_,
        ]:
            return True
        # @api_view is not supported well, since rest_framework decorators
        # don't anntoate __wrapped__
        case _:
            return False


def preprocess_derive_error_schemas(endpoints: Endpoints) -> Endpoints:
    """Process drf-spectactular schema and add missing HTTP error schemas."""
    method_names = ["GET", "POST", "PUT", "DELETE"]
    # These are the functions we want to annotate
    # https://github.com/tfranzel/drf-spectacular/blob/b1a34b05230316ca6c6d6724f2b9bb970a8dbe79/drf_spectacular/utils.py#L549
    endpoints_edit = (
        (path, path_regex, method_name, callback)
        for path, path_regex, method_name, callback in endpoints
        if method_name in method_names
        and callable(callback)
        and hasattr(callback, "cls")
    )
    for _path, _, method_name, callback in endpoints_edit:
        assert hasattr(callback, "cls")
        method = getattr(callback.cls, method_name.lower())
        schema = method.kwargs["schema"]
        # XXX HAXXX
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
        request: RequestAnnotation = request_nonlocals.get("request", None)
        responses: ResponseAnnotation = responses_nonlocals.get(
            "responses", None
        )
        match responses:
            case dict() as responses_dict:
                pass
            case _:
                continue
        request_serializer = get_request_serializer(request)
        maybe_annotate_400(_path, responses_dict, request_serializer)
        maybe_annotate_404(method, responses_dict)
        maybe_annotate_429(responses_dict)

    return endpoints
