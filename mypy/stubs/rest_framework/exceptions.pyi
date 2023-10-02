from typing import (
    Any,
    Optional,
    Union,
)

class APIException(Exception):
    def __init__(
        self, detail: Optional[str] = None, code: Optional[int] = None
    ) -> None: ...

class ValidationError(APIException):
    def __init__(
        self,
        detail: Optional[Union[str, dict[str, str]]] = None,
        code: Optional[int] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> None: ...
