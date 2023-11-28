from collections.abc import Mapping
from typing import (
    Any,
    Optional,
    Union,
)

class APIException(Exception):
    def __init__(
        self, detail: Optional[str] = None, code: Optional[int] = None
    ) -> None: ...

ErrorMessage = Union[str, Mapping[str, ErrorMessage]]

class ValidationError(APIException):
    def __init__(
        self,
        detail: Optional[ErrorMessage] = None,
        code: Optional[int] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> None: ...
