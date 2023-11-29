# Taken from
# https://raw.githubusercontent.com/encode/django-rest-framework/3.14.0/rest_framework/exceptions.py
from collections.abc import Mapping, Sequence
from typing import (
    Optional,
    Union,
)

ErrorMessage = Union[str, Mapping[str, ErrorMessage]]
Code = str

class APIException(Exception):
    status_code: int
    default_detail: str
    default_code: str
    detail: ErrorMessage

    def __init__(
        self,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
    ) -> None: ...
    def get_codes(self) -> ErrorMessage: ...
    def get_full_details(self) -> ErrorMessage: ...

class ValidationError(APIException): ...
class ParseError(APIException): ...
class AuthenticationFailed(APIException): ...
class NotAuthenticated(APIException): ...
class PermissionDenied(APIException): ...
class NotFound(APIException): ...

class MethodNotAllowed(APIException):
    def __init__(
        self,
        method: object,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
    ) -> None: ...

AvailableRenderers = Sequence[str]

class NotAcceptable(APIException):
    available_renders: Optional[AvailableRenderers]
    def __init__(
        self,
        method: object,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
        available_renderers: Optional[AvailableRenderers] = None,
    ) -> None: ...

class UnsupportedMediaType(APIException):
    def __init__(
        self,
        media_type: object,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
    ) -> None: ...

class Throttled(APIException):
    extra_detail_singular: str
    extra_detail_plural: str
    default_code: str

    def __init__(
        self,
        wait: Optional[int] = None,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
    ) -> None: ...
